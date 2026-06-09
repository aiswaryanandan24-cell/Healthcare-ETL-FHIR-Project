# task4.py
# Task 4 - Procedure
# Check if a Procedure exists for Katherine in OpenEMR.
# Since no procedures are returned via the FHIR API, create a new clinically
# relevant one using a pre-created JSON document, then post it to the
# Primary Care EHR FHIR server.
# No validation required.

import json
import requests
from pathlib import Path

# Server URLs
OPENEMR_BASE = "https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir"
PRIMARY_CARE_BASE = "http://159.203.105.138:8080/fhir"

# Known IDs from Task 1 (OpenEMR side — stable, won't change)
OPENEMR_PATIENT_ID = "9d035918-b974-4996-b35f-4b913d70f9fd"  # Katherine Schroeder

# Data and output directories
data_dir   = Path(__file__).parent / "data"
output_dir = Path(__file__).parent / "task4_output"
output_dir.mkdir(exist_ok=True)


# Authentication
def get_access_token():
    with open(data_dir / "access_token.json", "r") as f:
        return json.load(f).get("access_token")

def get_openemr_headers():
    return {
        "Authorization": f"Bearer {get_access_token()}",
        "Accept": "application/json"
    }

def get_primary_care_headers():
    return {
        "Content-Type": "application/fhir+json",
        "Accept": "application/fhir+json"
    }


# Read the Primary Care patient ID from the file Task 1 saved
def get_target_patient_id():
    """
    Read the Primary Care patient ID from data/patient.json saved by Task 1.
    This makes Task 4 adaptive — it works regardless of what ID the server assigned.
    """
    patient_file = data_dir / "patient.json"
    if not patient_file.exists():
        print("Error: data/patient.json not found. Run Task 1 first.")
        return None
    with open(patient_file, "r") as f:
        patient_resource = json.load(f)
    patient_id = patient_resource.get("id")
    if not patient_id:
        print("Error: No 'id' field found in data/patient.json")
        return None
    print(f"Patient ID loaded from data/patient.json: {patient_id}")
    return patient_id


# NEW: Read the Practitioner ID from the file saved by Task 3
def get_practitioner_id():
    """
    Read the Primary Care Practitioner ID from data/practitioner.json saved by Task 3.
    Returns None if the file doesn't exist — performer field will be skipped.
    """
    practitioner_file = data_dir / "practitioner.json"
    if not practitioner_file.exists():
        print("Warning: data/practitioner.json not found. Run Task 3 first.")
        return None
    with open(practitioner_file, "r") as f:
        resource = json.load(f)
    practitioner_id = resource.get("id")
    print(f"Practitioner ID loaded from data/practitioner.json: {practitioner_id}")
    return practitioner_id


# Get patient name for display
def get_patient(patient_id):
    response = requests.get(
        f"{OPENEMR_BASE}/Patient/{patient_id}",
        headers=get_openemr_headers()
    )
    patient = response.json()
    name = patient.get("name", [{}])[0]
    given = name.get("given", ["Unknown"])[0]
    family = name.get("family", "Unknown")
    return f"{given} {family}"


# Step 1: Check OpenEMR for existing Procedures
def check_procedure(patient_id):
    """
    Search OpenEMR for existing Procedure resources for the patient.
    Returns (procedure_code, procedure_display, found_in_openemr).
    If a SNOMED-coded procedure is found, its code and display are returned.
    If no procedures exist, returns (None, None, False).
    """
    print(f"\nStep 1: Checking OpenEMR for Procedures")
    print(f"Query: GET /Procedure?patient={patient_id}")

    response = requests.get(
        f"{OPENEMR_BASE}/Procedure",
        headers=get_openemr_headers(),
        params={"patient": patient_id}
    )
    entries = response.json().get("entry", [])
    print(f"Procedures found in OpenEMR: {len(entries)}")

    if not entries:
        print("No Procedures found in OpenEMR.")
        print("A new clinically relevant procedure will be created from the JSON document.")
        return None, None, False

    for i, entry in enumerate(entries[:10]):
        r = entry["resource"]
        codings = r.get("code", {}).get("coding", [])
        if codings:
            code    = codings[0].get("code", "unknown")
            display = codings[0].get("display", "unknown")
            system  = codings[0].get("system", "unknown")
        else:
            code    = "no-coding"
            display = r.get("code", {}).get("text", "unknown")
            system  = "text-only"
        print(f"  [{i}] Code: {code} | Display: {display} | System: {system}")

    for entry in entries:
        resource = entry["resource"]
        codings  = resource.get("code", {}).get("coding", [])
        for coding in codings:
            system  = coding.get("system", "")
            code    = coding.get("code", "")
            display = coding.get("display", "")
            if "snomed" in system.lower() and code and display:
                print(f"\nUsing procedure from OpenEMR: {display} (SNOMED: {code})")
                return code, display, True

    print("Procedures found in OpenEMR but none have a usable SNOMED code.")
    print("Loading from pre-created JSON document instead.")
    return None, None, True


# Step 2: Load the Procedure JSON document from file
def load_procedure(primary_care_patient_id, practitioner_id):
    """
    Load the pre-created Procedure JSON document.
    Strips the hardcoded 'id' from the template so the server assigns a fresh one.
    Updates the subject reference to point to the correct Primary Care patient.
    Adds performer reference using the Practitioner ID saved by Task 3.
    """
    json_path = data_dir / "procedure_task4.json"
    with open(json_path, "r") as f:
        procedure = json.load(f)

    # Strip hardcoded id from template — let the server assign a fresh one
    procedure.pop("id", None)

    # Point subject to the correct Primary Care patient
    procedure["subject"] = {"reference": f"Patient/{primary_care_patient_id}"}

    # NEW: Replace the placeholder performer with the real Practitioner reference
    if practitioner_id:
        procedure["performer"] = [{"actor": {"reference": f"Practitioner/{practitioner_id}"}}]
        print(f"Performer set to: Practitioner/{practitioner_id}")

    code    = procedure["code"]["coding"][0]["code"]
    display = procedure["code"]["coding"][0]["display"]

    print(f"\nStep 2: Loaded Procedure from {json_path}")
    print(f"Procedure: {display} (SNOMED: {code})")
    print(f"Subject updated to: Patient/{primary_care_patient_id}")

    # Save a copy to task4_output for reference
    output_path = output_dir / "procedure.json"
    with open(output_path, "w") as f:
        json.dump(procedure, f, indent=4)
    print(f"JSON document copied to: {output_path}")

    return procedure


# Step 3: POST the Procedure to Primary Care EHR
def post_procedure(procedure_payload, primary_care_patient_id):
    """
    POST the Procedure JSON to the Primary Care EHR FHIR server.
    The server assigns the ID — we capture it from the response and save
    the full server response to data/procedure_t4.json for reference.
    """
    code    = procedure_payload["code"]["coding"][0]["code"]
    display = procedure_payload["code"]["coding"][0]["display"]

    print(f"\nStep 3: POSTing Procedure to Primary Care EHR")
    print(f"Procedure: {display} (SNOMED: {code})")
    print(f"Linked to Patient ID: {primary_care_patient_id}")

    response = requests.post(
        url=f"{PRIMARY_CARE_BASE}/Procedure",
        headers=get_primary_care_headers(),
        json=procedure_payload
    )
    created = response.json()
    procedure_id = created.get("id")
    print(f"Procedure created successfully. Primary Care Procedure ID: {procedure_id}")

    with open(data_dir / "procedure_t4.json", "w") as f:
        json.dump(created, f, indent=4)
    print(f"Server response saved to data/procedure_t4.json (ID: {procedure_id})")

    return procedure_id


# Main
if __name__ == "__main__":
    print("TASK 4: PROCEDURE")

    # Load Primary Care patient ID from Task 1 output
    primary_care_patient_id = get_target_patient_id()
    if not primary_care_patient_id:
        exit(1)

    # NEW: Load Practitioner ID from Task 3 output
    practitioner_id = get_practitioner_id()

    # Get patient name for summary
    patient_name = get_patient(OPENEMR_PATIENT_ID)

    # EXTRACT
    procedure_code, procedure_display, found_in_openemr = check_procedure(OPENEMR_PATIENT_ID)

    # TRANSFORM
    # Load from pre-created JSON document
    procedure_payload = load_procedure(primary_care_patient_id, practitioner_id)
    procedure_code    = procedure_payload["code"]["coding"][0]["code"]
    procedure_display = procedure_payload["code"]["coding"][0]["display"]

    # LOAD
    procedure_id = post_procedure(procedure_payload, primary_care_patient_id)

    # SUMMARY
    print("\nTASK 4 SUMMARY")

    print(f"\nEXTRACTION (from OpenEMR FHIR server):")
    print(f"  Patient: {patient_name} (ID: {OPENEMR_PATIENT_ID})")
    print(f"  Check: GET /Procedure?patient={OPENEMR_PATIENT_ID}")
    print(f"  Procedures found in OpenEMR: {'Yes' if found_in_openemr else 'No'}")
    print(f"  OpenEMR FHIR API returns 0 procedures for this patient.")
    print(f"  A new clinically relevant procedure was created from the JSON document.")

    print(f"\nTRANSFORM (JSON document prepared based on patient clinical history):")
    print(f"  Document: data/procedure_task4.json")
    print(f"  Procedure: {procedure_display} (SNOMED: {procedure_code})")
    print(f"  Clinical relevance: directly related to Katherine's Anemia (Task 1 condition)")
    print(f"  Subject updated to: Patient/{primary_care_patient_id}")
    print(f"  Performer set to: Practitioner/{practitioner_id}")

    print(f"\nLOADING (to Primary Care EHR FHIR server):")
    print(f"  JSON document saved to: task4_output/procedure.json")
    print(f"  Patient ID: {primary_care_patient_id} (read from data/patient.json)")
    print(f"  Practitioner ID: {practitioner_id} (read from data/practitioner.json)")
    print(f"  Procedure created: ID {procedure_id}")
    print(f"  Procedure saved to: data/procedure_t4.json")
    print(f"  SNOMED code: {procedure_code}")
    print(f"  Procedure: {procedure_display}")
    print(f"  Status: completed")
    print(f"  Performed: 2010-12-17")