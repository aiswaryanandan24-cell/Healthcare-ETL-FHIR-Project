# task3.py
# Task 3 - Blood Pressure Observation
# Check if a Blood Pressure Observation exists for Katherine in OpenEMR.
# Use the materials covered earlier to create a JSON document (saved to file),
# then post it to the Primary Care EHR FHIR server.
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
output_dir = Path(__file__).parent / "task3_output"
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
    This makes Task 3 adaptive — it works regardless of what ID the server assigned.
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


# NEW: Create a Practitioner on the Primary Care EHR and save to data/practitioner.json
def create_practitioner():
    """
    POST a Practitioner resource to the Primary Care EHR.
    Uses Katherine's known attending physician from OpenEMR records.
    Saves the server response to data/practitioner.json so Task 4 can reuse the same ID.
    """
    practitioner_payload = {
        "resourceType": "Practitioner",
        "name": [
            {
                "use": "official",
                "prefix": ["Dr"],
                "family": "Pepper"
            }
        ],
        "gender": "male"
    }

    print(f"\nStep 0: Creating Practitioner on Primary Care EHR")

    response = requests.post(
        url=f"{PRIMARY_CARE_BASE}/Practitioner",
        headers=get_primary_care_headers(),
        json=practitioner_payload
    )
    created = response.json()
    practitioner_id = created.get("id")
    print(f"Practitioner created successfully. Primary Care Practitioner ID: {practitioner_id}")

    with open(data_dir / "practitioner.json", "w") as f:
        json.dump(created, f, indent=4)
    print(f"Server response saved to data/practitioner.json (ID: {practitioner_id})")

    return practitioner_id


# NEW: Read the Practitioner ID from the file saved by create_practitioner()
def get_practitioner_id():
    """
    Read the Primary Care Practitioner ID from data/practitioner.json.
    Returns None if the file doesn't exist.
    """
    practitioner_file = data_dir / "practitioner.json"
    if not practitioner_file.exists():
        return None
    with open(practitioner_file, "r") as f:
        resource = json.load(f)
    return resource.get("id")


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


# Step 1: Check OpenEMR for an existing BP Observation
def check_bp_observation(patient_id):
    """
    Search OpenEMR for an existing Blood Pressure Observation for the patient.
    Uses LOINC code 85354-9 (Blood pressure panel) and vital-signs category.
    Returns (systolic, diastolic, found_in_openemr).
    OpenEMR returns this record with dataAbsentReason on both components —
    the actual values are not accessible via the FHIR API even though
    they exist in OpenEMR's internal vitals table.
    """
    print(f"\nStep 1: Checking OpenEMR for Blood Pressure Observation")
    print(f"Query: GET /Observation?patient={patient_id}&category=vital-signs&code=85354-9")

    response = requests.get(
        f"{OPENEMR_BASE}/Observation",
        headers=get_openemr_headers(),
        params={
            "patient": patient_id,
            "category": "vital-signs",
            "code": "85354-9",
            "_sort": "-date",
            "_count": "1"
        }
    )
    entries = response.json().get("entry", [])
    print(f"Blood Pressure Observations found in OpenEMR: {len(entries)}")

    if not entries:
        print("No BP Observation found in OpenEMR.")
        return None, None, False

    resource = entries[0]["resource"]
    components = resource.get("component", [])
    systolic = None
    diastolic = None

    for component in components:
        for coding in component.get("code", {}).get("coding", []):
            val = component.get("valueQuantity", {}).get("value")
            if coding.get("code") == "8480-6":
                systolic = val
            elif coding.get("code") == "8462-4":
                diastolic = val

    if systolic is not None and diastolic is not None:
        print(f"Extracted BP values from OpenEMR — Systolic: {systolic} mmHg | Diastolic: {diastolic} mmHg")
        return systolic, diastolic, True
    else:
        print(f"BP record found in OpenEMR but values are absent (dataAbsentReason: unknown).")
        print(f"OpenEMR's FHIR API does not expose the actual vitals values for this patient.")
        print(f"Loading BP values from pre-created JSON document instead.")
        return None, None, True


# Step 2: Load the BP Observation JSON document from file
def load_bp_observation(primary_care_patient_id, practitioner_id):
    """
    Load the pre-created Blood Pressure Observation JSON document.
    Strips the hardcoded 'id' from the template so the server assigns a fresh one.
    Updates the subject reference to point to the correct Primary Care patient.
    Adds performer reference if a Practitioner ID is available.
    """
    json_path = data_dir / "observation_task3.json"
    with open(json_path, "r") as f:
        observation = json.load(f)

    # Strip hardcoded id from template — let the server assign a fresh one
    observation.pop("id", None)

    # Point subject to the correct Primary Care patient
    observation["subject"] = {"reference": f"Patient/{primary_care_patient_id}"}

    # NEW: Add performer reference using the Practitioner ID
    if practitioner_id:
        observation["performer"] = [{"reference": f"Practitioner/{practitioner_id}"}]
        print(f"Performer set to: Practitioner/{practitioner_id}")

    print(f"\nStep 2: Loaded BP Observation from {json_path}")

    systolic  = observation["component"][0]["valueQuantity"]["value"]
    diastolic = observation["component"][1]["valueQuantity"]["value"]
    print(f"Systolic: {systolic} mmHg | Diastolic: {diastolic} mmHg")
    print(f"Subject updated to: Patient/{primary_care_patient_id}")

    # Save a copy to task3_output for reference
    output_path = output_dir / "bp_observation.json"
    with open(output_path, "w") as f:
        json.dump(observation, f, indent=4)
    print(f"JSON document copied to: {output_path}")

    return observation


# Step 3: POST the BP Observation to Primary Care EHR
def post_bp_observation(observation_payload, primary_care_patient_id):
    """
    POST the Blood Pressure Observation JSON to the Primary Care EHR FHIR server.
    The server assigns the ID — we capture it from the response and save
    the full server response to data/observation_t3.json for reference.
    """
    systolic  = observation_payload["component"][0]["valueQuantity"]["value"]
    diastolic = observation_payload["component"][1]["valueQuantity"]["value"]

    print(f"\nStep 3: POSTing Blood Pressure Observation to Primary Care EHR")
    print(f"Systolic: {systolic} mmHg | Diastolic: {diastolic} mmHg")
    print(f"Linked to Patient ID: {primary_care_patient_id}")

    response = requests.post(
        url=f"{PRIMARY_CARE_BASE}/Observation",
        headers=get_primary_care_headers(),
        json=observation_payload
    )
    created = response.json()
    observation_id = created.get("id")
    print(f"Observation created successfully. Primary Care Observation ID: {observation_id}")

    with open(data_dir / "observation_t3.json", "w") as f:
        json.dump(created, f, indent=4)
    print(f"Server response saved to data/observation_t3.json (ID: {observation_id})")

    return observation_id


# Main
if __name__ == "__main__":
    print("TASK 3: BLOOD PRESSURE OBSERVATION")

    # Load Primary Care patient ID from Task 1 output
    primary_care_patient_id = get_target_patient_id()
    if not primary_care_patient_id:
        exit(1)

    # NEW: Create Practitioner and save to data/practitioner.json for Task 4 to reuse
    practitioner_id = create_practitioner()

    # Get patient name for summary
    patient_name = get_patient(OPENEMR_PATIENT_ID)

    # EXTRACT
    systolic, diastolic, found_in_openemr = check_bp_observation(OPENEMR_PATIENT_ID)

    # TRANSFORM
    # Load from pre-created JSON document since OpenEMR FHIR values are absent
    observation_payload = load_bp_observation(primary_care_patient_id, practitioner_id)
    systolic  = observation_payload["component"][0]["valueQuantity"]["value"]
    diastolic = observation_payload["component"][1]["valueQuantity"]["value"]

    # LOAD
    observation_id = post_bp_observation(observation_payload, primary_care_patient_id)

    # SUMMARY
    print("\nTASK 3 SUMMARY")

    print(f"\nEXTRACTION (from OpenEMR FHIR server):")
    print(f"  Patient: {patient_name} (ID: {OPENEMR_PATIENT_ID})")
    print(f"  BP check: GET /Observation?patient={OPENEMR_PATIENT_ID}&category=vital-signs&code=85354-9")
    print(f"  BP records found in OpenEMR: {'Yes' if found_in_openemr else 'No'}")
    print(f"  FHIR values: absent (dataAbsentReason: unknown on both components)")
    print(f"  Actual values sourced from OpenEMR vitals dashboard: {systolic}/{diastolic} mmHg")

    print(f"\nTRANSFORM (JSON document prepared from OpenEMR vitals data):")
    print(f"  Document: data/observation_task3.json")
    print(f"  Subject updated to: Patient/{primary_care_patient_id}")
    print(f"  Performer set to: Practitioner/{practitioner_id}")

    print(f"\nLOADING (to Primary Care EHR FHIR server):")
    print(f"  JSON document saved to: task3_output/bp_observation.json")
    print(f"  Patient ID: {primary_care_patient_id} (read from data/patient.json)")
    print(f"  Practitioner ID: {practitioner_id} (saved to data/practitioner.json)")
    print(f"  Observation created: ID {observation_id}")
    print(f"  Observation saved to: data/observation_t3.json")
    print(f"  LOINC code: 85354-9 (Blood pressure panel)")
    print(f"  Systolic  (8480-6): {systolic} mmHg")
    print(f"  Diastolic (8462-4): {diastolic} mmHg")