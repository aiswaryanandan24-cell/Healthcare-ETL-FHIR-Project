# task2.py
# Task 2 - Child Workflow
# Extract: same patient (Katherine Schroeder) and a different condition from OpenEMR
# Transform: find child concept using Hermes terminology server
# Load: create Condition only on Primary Care EHR (patient ID read from data/patient.json)
# Validate: validate the Condition separately

import json
import requests
from pathlib import Path

# Server URLs
OPENEMR_BASE = "https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir"
HERMES_BASE = "http://159.203.121.13:8080/v1/snomed"
PRIMARY_CARE_BASE = "http://159.203.105.138:8080/fhir"

# Profile URLs
CONDITION_PROFILE = "http://example.org/StructureDefinition/my-condition-profile"

# Known IDs from Task 1 (OpenEMR side — stable, won't change)
OPENEMR_PATIENT_ID = "9d035918-b974-4996-b35f-4b913d70f9fd"
TASK1_CONDITION_NAME = "Anemia"

# Data directory
data_dir = Path(__file__).parent / "data"


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


# Step 1: Get Katherine directly from OpenEMR
def get_patient(patient_id):
    """Fetch a single Patient resource from OpenEMR by ID."""
    print(f"\nStep 1: Fetching patient {patient_id} from OpenEMR")

    # GET by ID, not search needed
    response = requests.get(f"{OPENEMR_BASE}/Patient/{patient_id}", headers=get_openemr_headers())
    patient = response.json()

    name = patient.get("name", [{}])[0]
    given = name.get("given", [""])[0]
    family = name.get("family", "")
    print(f"Patient: {given} {family} | ID: {patient.get('id')} | DOB: {patient.get('birthDate')}")

    return patient


# Step 2: Get all conditions for the patient
def get_patient_conditions(patient_id):
    """
    Retrieve all Condition resources for a patient from OpenEMR.
    Returns a list of condition entries from the FHIR Bundle.
    """
    print(f"\nStep 2: Getting conditions for patient {patient_id}")

    response = requests.get(
        f"{OPENEMR_BASE}/Condition",
        headers=get_openemr_headers(),
        params={"patient": patient_id}
    )
    entries = response.json().get("entry", [])
    print(f"Total conditions found: {len(entries)}")

    for i, entry in enumerate(entries):
        r = entry["resource"]
        codings = r.get("code", {}).get("coding", [])
        if codings:
            code = codings[0].get("code", "unknown")
            display = codings[0].get("display", "unknown")
            system = codings[0].get("system", "unknown")
        else:
            code = "no-coding"
            display = r.get("code", {}).get("text", "unknown")
            system = "text-only"
        print(f"  [{i}] ID: {r.get('id')} | Display: {display} | System: {system}")

    return entries


# Search Hermes by text
def search_snomed_by_text(search_term):
    """
    Search Hermes for a SNOMED concept by display name.
    Returns the concept ID and preferred term of the best match.
    """
    print(f"Searching Hermes for: '{search_term}'")
    response = requests.get(
        f"{HERMES_BASE}/search",
        params={"s": search_term, "constraint": "<404684003", "maxHits": 1} # ECL: all descendants of "Clinical finding"
    )
    items = response.json()
    if isinstance(items, dict):
        items = items.get("items", [])
    if not items:
        return None, None
    concept_id = items[0].get("conceptId") or items[0].get("id")
    concept_term = items[0].get("preferredTerm") or items[0].get("term", search_term)
    print(f" Found: {concept_id} | {concept_term}")
    return concept_id, concept_term


# Step 3: Pick a different disorder (skip Task 1 condition)
def select_condition(condition_entries, skip_display_name):
    """
    Select the first valid disorder from the condition list that also has
    a child concept in Hermes.
    Skips findings, situations, and the condition already used in Task 1.
    Strips (disorder) suffix before Hermes text search for better matching.
    """
    print(f"\nStep 3: Selecting a different disorder (skipping '{skip_display_name}')")

    for entry in condition_entries:
        resource = entry["resource"]
        codings = resource.get("code", {}).get("coding", [])
        text = resource.get("code", {}).get("text", "")
        display = text

        # filter 1: skip findings and situations
        if "finding" in display.lower() or "situation" in display.lower():
            continue
        # filter 2: skip task 1 condition
        if skip_display_name.lower() in display.lower():
            continue
        # filter 3: only proceed if label includes disorder
        if "(disorder)" not in display.lower():
            continue

        # SNOMED-coded condition
        for coding in codings:
            system = coding.get("system", "")
            code = coding.get("code", "")
            disp = coding.get("display", "")
            if "snomed" in system.lower() and code:
                child_id, child_term = get_child_concept(code)
                if child_id:
                    print(f"Selected condition: {disp} (SNOMED: {code})")
                    return code, disp

        # Text-only — strip (disorder) before searching Hermes
        search_term = display.replace("(disorder)", "").strip()
        concept_id, concept_term = search_snomed_by_text(search_term)
        if concept_id:
            child_id, child_term = get_child_concept(str(concept_id))
            if child_id:
                print(f"Selected condition: {concept_term} (SNOMED: {concept_id})")
                return str(concept_id), concept_term

    return None, None


# Step 4: Find a child concept in Hermes
def get_child_concept(snomed_code):
    """
    Find a direct child concept for a SNOMED code using Hermes ECL search.
    The ECL operator '<!' means 'direct children of'.
    Returns (child_id, child_term) or (None, None) if no children exist.
    """
    print(f"\nStep 4: Looking up child concept for SNOMED {snomed_code}")

    response = requests.get(
        f"{HERMES_BASE}/search",
        params={"constraint": f"<!{snomed_code}", "maxHits": 1} # ECL
    )
    items = response.json()
    if isinstance(items, dict):
        items = items.get("items", [])

    if not items:
        print(f" No children found for SNOMED {snomed_code}. Skipping.")
        return None, None

    child_id = items[0].get("conceptId") or items[0].get("id")
    child_term = items[0].get("preferredTerm") or items[0].get("term", "unknown")
    print(f"Child concept ID:   {child_id}")
    print(f"Child concept term: {child_term}")
    return child_id, child_term


# Step 5: Create Condition on Primary Care EHR
def create_condition_on_primary_care(primary_care_patient_id, child_concept_id, child_term):
    """
    Create a Condition resource on the Primary Care EHR via POST.
    The server assigns the ID — we capture it from the response and save
    the full server response to data/condition_t2.json for reference.
    """
    condition_payload = {
        "resourceType": "Condition",
        "meta": {"profile": [CONDITION_PROFILE]},
        "text": {
            "status": "generated",
            "div": f'<div xmlns="http://www.w3.org/1999/xhtml">Condition: {child_term} (SNOMED: {child_concept_id})</div>'
        },
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active"
                }
            ]
        },
        "verificationStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    "code": "confirmed"
                }
            ]
        },
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                        "code": "problem-list-item",
                        "display": "Problem List Item"
                    }
                ]
            }
        ],
        "severity": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "6736007",
                    "display": "Moderate"
                }
            ]
        },
        "code": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": str(child_concept_id),
                    "display": child_term
                }
            ],
            "text": child_term
        },
        "bodySite": [
            {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "38266002",
                        "display": "Entire body as a whole"
                    }
                ]
            }
        ],
        "subject": {"reference": f"Patient/{primary_care_patient_id}"},
        "onsetDateTime": "2024-01-01T00:00:00+00:00"
    }

    print(f"\nStep 5: Creating Condition on Primary Care EHR via POST")
    print(f"Using child concept: {child_concept_id} | {child_term}")
    print(f"Linked to Patient ID: {primary_care_patient_id}")

    response = requests.post(
        url=f"{PRIMARY_CARE_BASE}/Condition",
        headers=get_primary_care_headers(),
        json=condition_payload
    )
    created = response.json()
    condition_id = created.get("id")
    print(f"Condition created successfully. Primary Care Condition ID: {condition_id}")

    # Save the server response to condition_t2.json for reference
    with open(data_dir / "condition_t2.json", "w") as f:
        json.dump(created, f, indent=4)
    print(f"Server response saved to data/condition_t2.json (ID: {condition_id})")

    return condition_id, condition_payload


# Step 6: Validate the Condition
def validate_resource(resource_type, resource_payload):
    """
    Validate a FHIR resource using the $validate endpoint on the Primary Care server.
    Returns the number of errors found.
    """
    url = f"{PRIMARY_CARE_BASE}/{resource_type}/$validate"
    print(f"\n--- Validating {resource_type} ---")
    print(f"Endpoint: POST {url}")
    print(f"Profile:  {resource_payload.get('meta', {}).get('profile', ['unknown'])[0]}")

    response = requests.post(url=url, headers=get_primary_care_headers(), json=resource_payload)
    print(f"Validation response status: {response.status_code}")

    issues = response.json().get("issue", [])
    errors   = [i for i in issues if i.get("severity") == "error"]
    warnings = [i for i in issues if i.get("severity") == "warning"]

    if not errors:
        print(f" {resource_type} validation PASSED — conforms to profile.")
    else:
        print(f" {resource_type} validation FAILED — {len(errors)} error(s) found.")
        for issue in errors:
            print(f"  [error] {issue.get('diagnostics', 'no details')}")

    for issue in warnings:
        print(f"  [warning] {issue.get('diagnostics', 'no details')}")

    return len(errors)


# Main
if __name__ == "__main__":

    print("TASK 2 - CHILD WORKFLOW")

    # Load Primary Care patient ID from Task 1 output
    primary_care_patient_id = get_target_patient_id()
    if not primary_care_patient_id:
        exit(1)

    # EXTRACT

    # Step 1: Fetch Katherine directly by known OpenEMR ID
    patient = get_patient(OPENEMR_PATIENT_ID)

    # Step 2: Get all her conditions from OpenEMR
    conditions = get_patient_conditions(OPENEMR_PATIENT_ID)

    # Step 3: Pick a different disorder, skip Anemia from Task 1
    snomed_code, condition_display = select_condition(conditions, skip_display_name=TASK1_CONDITION_NAME)

    if not snomed_code:
        print("\n[ERROR] No suitable condition with children found. Token may be expired.")
        print("Run: python auth/refresh_token.py")
        exit(1)

    # TRANSFORM

    # Step 4: Find a child concept in Hermes
    child_id, child_term = get_child_concept(snomed_code)

    # LOAD

    # Step 5: Create Condition on Primary Care EHR via POST (server assigns ID)
    primary_care_condition_id, condition_payload = create_condition_on_primary_care(
        primary_care_patient_id, child_id, child_term
    )

    # VALIDATE

    condition_errors = validate_resource("Condition", condition_payload)

    # SUMMARY
    print("\nTASK 2 SUMMARY")

    patient_name = patient.get("name", [{}])[0]
    print(f"\nEXTRACTION (from OpenEMR FHIR server):")
    print(f"  Patient: {patient_name.get('given', [''])[0]} {patient_name.get('family', '')} (ID: {OPENEMR_PATIENT_ID})")
    print(f"  Condition: {condition_display}")
    print(f"  SNOMED code: {snomed_code}")

    print(f"\nTRANSFORMATION (via Hermes SNOMED terminology server):")
    print(f"  Original code: {snomed_code} ({condition_display})")
    print(f"  Child concept: {child_id} ({child_term})")
    print(f"  Relationship:  IS-A (116680003) — parent maps down to child")

    print(f"\nLOADING (to Primary Care EHR FHIR server):")
    print(f"  Patient ID: {primary_care_patient_id} (read from data/patient.json)")
    print(f"  Condition created: ID {primary_care_condition_id}")
    print(f"  Condition saved to: data/condition_t2.json")
    print(f"  Condition uses child concept: {child_id} ({child_term})")

    print(f"\nVALIDATION (separate step, not part of ETL):")
    print(f"  Condition profile: {CONDITION_PROFILE}")
    print(f"  Method: POST /$validate with meta.profile on each resource")
    condition_status = "PASSED" if condition_errors == 0 else f"FAILED ({condition_errors} error(s))"
    print(f"  Condition validation: {condition_status}")