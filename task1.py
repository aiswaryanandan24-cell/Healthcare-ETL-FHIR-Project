# task1.py
# Task 1 - Parent Workflow
# Extract: patient and condition data from OpenEMR FHIR server
# Transform: find parent concept using Hermes terminology server
# Load: create Patient and Condition on Primary Care EHR FHIR server
# Validate: separately validate Patient and Condition resources

import json
import requests
from pathlib import Path

# Server URLs
# 3 servers involved in this pipeline
OPENEMR_BASE = "https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir"
HERMES_BASE = "http://159.203.121.13:8080/v1/snomed"
PRIMARY_CARE_BASE = "http://159.203.105.138:8080/fhir"

# Profile URLs
PATIENT_PROFILE = "http://example.org/StructureDefinition/my-patient-profile"
CONDITION_PROFILE = "http://example.org/StructureDefinition/my-condition-profile"

# Search parameters
# predefined patient search param
SEARCH_GENDER = "female"
SEARCH_BIRTHDATE_AFTER = "1951-01-01"
SEARCH_LAST_UPDATED_AFTER = "2020-01-01"

# Data directory
data_dir = Path(__file__).parent / "data"
data_dir.mkdir(exist_ok=True)


# Authentication
# read Bearer token and save to access_token.json by access_token.py
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


# Step 1: Search for a patient in OpenEMR
def search_patient():
    """
    Search OpenEMR for patients using multiple FHIR search parameters:
      - gender: female
      - birthdate: after 1951-01-01 (gt prefix)
      - _lastUpdated: after 2020-01-01 (gt prefix)
    """
    url = f"{OPENEMR_BASE}/Patient"
    params = {
        "gender": SEARCH_GENDER,
        "birthdate": f"gt{SEARCH_BIRTHDATE_AFTER}",
        "_lastUpdated": f"gt{SEARCH_LAST_UPDATED_AFTER}"
    }

    print(f"\nStep 1: Searching for patients")
    print(f"Query: GET /Patient?gender={SEARCH_GENDER}&birthdate=gt{SEARCH_BIRTHDATE_AFTER}&_lastUpdated=gt{SEARCH_LAST_UPDATED_AFTER}")
    print(f"Expected response: FHIR Bundle with matching Patient resources.")

    response = requests.get(url=url, headers=get_openemr_headers(), params=params)

    # FHIR respons with a Bundle resource
    data = response.json()
    entries = data.get("entry", [])
    print(f"Total patients found: {len(entries)}, showing first 10.")

    # print a preview of results to verify the search worked
    for i, entry in enumerate(entries[:10]):
        resource = entry["resource"]
        patient_id = resource.get("id")
        #FHIR name is a list; take the first
        name = resource.get("name", [{}])[0]
        given = name.get("given", [""])[0]
        family = name.get("family", "")
        gender_val = resource.get("gender", "unknown")
        dob = resource.get("birthDate", "unknown")
        deceased = resource.get("deceasedBoolean") or resource.get("deceasedDateTime")
        print(f"  [{i}] ID: {patient_id} | Name: {given} {family} | Gender: {gender_val} | DOB: {dob} | Deceased: {deceased}")

    return entries


# Step 2: Get all conditions for a patient
def get_patient_conditions(patient_id):
    """
    Get all Condition resources for a given patient from OpenEMR.
    Returns a list of condition entries from the Bundle.
    """
    url = f"{OPENEMR_BASE}/Condition"
    params = {"patient": patient_id}

    print(f"\nStep 2: Getting conditions for patient {patient_id}")

    response = requests.get(url=url, headers=get_openemr_headers(), params=params)
    data = response.json()
    entries = data.get("entry", [])
    print(f"Total conditions found: {len(entries)}, showing first 20.")

    if not entries:
        print("No conditions found for this patient.")
        return None

    # print summary of each condition for inspection
    for i, entry in enumerate(entries[:20]):
        resource = entry["resource"]
        code_field = resource.get("code", {})
        codings = code_field.get("coding", [])
        if codings:
            display = codings[0].get("display", "unknown")
            system = codings[0].get("system", "unknown")
        else:
            # if condition is text, add free-text label
            display = code_field.get("text", "unknown")
            system = "text-only"
        print(f"  [{i}] Display: {display} | System: {system}")

    return entries


# Search Hermes by text (condition in text)
def search_snomed_by_text(search_term):
    """
    Search the Hermes terminology server for a SNOMED concept by name.
    Returns the concept ID and preferred term of the best match.
    """
    print(f"  Searching Hermes for SNOMED concept: '{search_term}'")
    response = requests.get(
        f"{HERMES_BASE}/search",
        # ECL: "< 404684003" = all clinical findings
        params={"s": search_term, "constraint": "<404684003", "maxHits": 1}
    )
    data = response.json()
    items = data if isinstance(data, list) else data.get("items", [])

    if not items:
        return None, None

    # get concept ID and preferred term from the top result
    concept_id = items[0].get("conceptId") or items[0].get("id")
    preferred_term = items[0].get("preferredTerm") or items[0].get("term", search_term)
    print(f"  Found: {concept_id} | {preferred_term}")
    return concept_id, preferred_term


# Step 3: Find the parent term for a SNOMED concept via Hermes
def get_parent_concept(snomed_code):
    """
    Look up the parent term for a SNOMED CT concept using Hermes.
    Uses the IS-A relationship (116680003) to find the direct parent.
    Returns the parent concept ID and its preferred term.
    """
    print(f"\nStep 3: Looking up parent term for SNOMED code {snomed_code}")

    # the extended endpoint return concept data include all relationships
    response = requests.get(f"{HERMES_BASE}/concepts/{snomed_code}/extended")
    data = response.json()

    # directParentRelationships is a dict keyed by relationship type ID
    # 116680003 is the SNOMED CT IS-A relationship
    direct_parents = data.get("directParentRelationships", {}).get("116680003", [])
    parent_id = direct_parents[0]
    print(f"Direct parent concept ID: {parent_id}")

    # get preferred term
    parent_response = requests.get(f"{HERMES_BASE}/concepts/{parent_id}/extended")
    parent_data = parent_response.json()
    preferred_term = parent_data.get("preferredDescription", {}).get("term", "unknown")
    print(f"Parent preferred term: {preferred_term}")

    return parent_id, preferred_term


# Step 4: Create a Patient on the Primary Care EHR server
def create_patient_on_primary_care(openemr_patient_resource):
    """
    Create a Patient resource on the Primary Care EHR FHIR server via POST.
    The server assigns the ID — we capture it from the response and save
    the full server response to data/patient.json for downstream tasks.
    """
    name = openemr_patient_resource.get("name", [{}])[0]
    given = name.get("given", ["Unknown"])
    family = name.get("family", "Unknown")
    gender = openemr_patient_resource.get("gender", "unknown")
    birth_date = openemr_patient_resource.get("birthDate", "1900-01-01")
    identifier_value = openemr_patient_resource.get("id", "unknown")

    deceased_boolean = openemr_patient_resource.get("deceasedBoolean", False)
    deceased_datetime = openemr_patient_resource.get("deceasedDateTime")
    is_deceased = bool(deceased_datetime) or bool(deceased_boolean)
    is_active = not is_deceased

    address = openemr_patient_resource.get("address", [{}])[0]
    address_block = {"use": address.get("use", "home"), "type": address.get("type", "both")}

    for field in ["line", "city", "state", "postalCode"]:
        val = address.get(field)
        if val:
            address_block[field] = val

    text = address.get("text")
    if not text:
        parts = []
        if address.get("line"):
            parts.extend(address["line"] if isinstance(address["line"], list) else [address["line"]])
        if address.get("city"):
            parts.append(address["city"])
        if address.get("state"):
            parts.append(address["state"])
        if address.get("postalCode"):
            parts.append(address["postalCode"])
        text = ", ".join(parts) if parts else "Unknown"
    address_block["text"] = text
    address_block["district"] = address.get("district") or "Unknown"

    # build the complete FHIR patient payload
    patient_payload = {
        "resourceType": "Patient",
        "meta": {"profile": [PATIENT_PROFILE]},
        "text": {
            "status": "generated",
            "div": f'<div xmlns="http://www.w3.org/1999/xhtml">Patient: {given[0]} {family}, Gender: {gender}, DOB: {birth_date}</div>'
        },
        "identifier": [
            {
                "use": "usual",
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "MR"
                        }
                    ]
                },
                "system": "urn:oid:1.2.36.146.595.217.0.1",
                "value": identifier_value
            }
        ],
        "active": is_active,
        "name": [{"use": "official", "family": family, "given": given}],
        "gender": gender,
        "birthDate": birth_date,
        "deceasedBoolean": is_deceased,
        "address": [address_block]
    }

    print(f"\nStep 4: Creating Patient on Primary Care EHR via POST")
    print(f"Patient: {given[0]} {family} | Active: {is_active} | Deceased: {is_deceased}")

    # post to Primary Care Server
    response = requests.post(
        url=f"{PRIMARY_CARE_BASE}/Patient",
        headers=get_primary_care_headers(),
        json=patient_payload
    )
    created = response.json()
    patient_id = created.get("id") # assign new patient ID
    print(f"Patient created successfully. Primary Care Patient ID: {patient_id}")

    # Save the server response (which contains the real assigned ID) to patient.json
    # Tasks 2, 3, and 4 will read this file to find the patient ID
    with open(data_dir / "patient.json", "w") as f:
        json.dump(created, f, indent=4)
    print(f"Server response saved to data/patient.json (ID: {patient_id})")

    return patient_id, patient_payload


# Step 5: Create a Condition using the parent concept
def create_condition_on_primary_care(primary_care_patient_id, parent_concept_id, parent_term):
    """
    Create a Condition resource on the Primary Care EHR FHIR server via POST.
    The server assigns the ID — we capture it from the response and save
    the full server response to data/condition_t1.json for reference.
    """
    condition_payload = {
        "resourceType": "Condition",
        "meta": {"profile": [CONDITION_PROFILE]},
        "text": {
            "status": "generated",
            "div": f'<div xmlns="http://www.w3.org/1999/xhtml">Condition: {parent_term} (SNOMED: {parent_concept_id})</div>'
        },
        "clinicalStatus": {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
        },
        "verificationStatus": {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed"}]
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
            "coding": [{"system": "http://snomed.info/sct", "code": "6736007", "display": "Moderate"}]
        },
        # Parent SNOMED Concept, the transformed resutls
        "code": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": str(parent_concept_id),
                    "display": parent_term
                }
            ],
            "text": parent_term
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
        # link the condition back to the patient just created
        "subject": {"reference": f"Patient/{primary_care_patient_id}"},
        "onsetDateTime": "2024-01-01T00:00:00+00:00"
    }

    print(f"\nStep 5: Creating Condition on Primary Care EHR via POST")
    print(f"Using parent concept: {parent_concept_id} | {parent_term}")
    print(f"Linked to Patient ID: {primary_care_patient_id}")

    response = requests.post(
        url=f"{PRIMARY_CARE_BASE}/Condition",
        headers=get_primary_care_headers(),
        json=condition_payload
    )
    created = response.json()
    condition_id = created.get("id")
    print(f"Condition created successfully. Primary Care Condition ID: {condition_id}")

    # Save the server response to condition_t1.json for reference
    with open(data_dir / "condition_t1.json", "w") as f:
        json.dump(created, f, indent=4)
    print(f"Server response saved to data/condition_t1.json (ID: {condition_id})")

    return condition_id, condition_payload


# Step 6: Validate Patient and Condition separately
def validate_resource(resource_type, resource_payload):
    """
    Validate a FHIR resource against its profile using the $validate operation.
    Returns (status_code, response_data).
    """

    # $validate is a POST endpoint that check the resource and return outcomes
    url = f"{PRIMARY_CARE_BASE}/{resource_type}/$validate"
    print(f"\nValidating {resource_type}")
    print(f"Endpoint: POST {url}")
    print(f"Profile:  {resource_payload.get('meta', {}).get('profile', ['unknown'])[0]}")

    response = requests.post(url=url, headers=get_primary_care_headers(), json=resource_payload)
    print(f"Validation response status: {response.status_code}")

    data = response.json()
    issues = data.get("issue", [])
    for issue in issues:
        severity = issue.get("severity")
        if severity in ("error", "warning"):
            print(f"  [{severity}] {issue.get('diagnostics', 'no details')}")

    return response.status_code, data


# Main
if __name__ == "__main__":
    print("TASK 1 - PARENT WORKFLOW")
    print("ETL Pipeline: OpenEMR, Hermes, Primary Care EHR")

    # EXTRACT

    # Step 1: Search OpenEMR with multiple filters
    patients = search_patient()

    selected_patient = None
    patient_id = None
    snomed_code = None
    condition_display = None

    # Iterate through the results to find one that meets all our criteria
    for patient_entry in patients:
        candidate = patient_entry["resource"]

        if candidate.get("deceasedBoolean") or candidate.get("deceasedDateTime"):
            continue

        candidate_id = candidate["id"]
        candidate_name = candidate.get("name", [{}])[0]
        print(f"\nTrying patient: {candidate_name.get('given', [''])[0]} {candidate_name.get('family', '')} (ID: {candidate_id})")

        # Step 2: Check if this patient has any conditions
        conds = get_patient_conditions(candidate_id)
        if not conds:
            continue

        found_snomed_code = None
        found_display = None
        found_condition = None

        for entry in conds:
            resource = entry["resource"]
            code_field = resource.get("code", {})
            codings = code_field.get("coding", [])
            text = code_field.get("text", "")

            # PATH A: condition has a SNOMED coding directly
            for coding in codings:
                system = coding.get("system", "")
                display = coding.get("display", "")
                code = coding.get("code", "")
                if "snomed" in system.lower() and code:
                    if "situation" in display.lower() or "finding" in display.lower():
                        continue
                    found_snomed_code = code
                    found_display = display
                    found_condition = resource
                    break

            if found_snomed_code:
                break

            # PATH B: condition is text-only (no SNOMED coding in OpenEMR)
            # If the text label contains "(disorder)" we can search Hermes by name
            if not codings and text and "(disorder)" in text.lower():
                looked_up_id, looked_up_term = search_snomed_by_text(text)
                if looked_up_id:
                    found_snomed_code = str(looked_up_id)
                    found_display = looked_up_term
                    found_condition = resource
                    break

        # If we found a usable condition, lock in this patient and stop searching
        if found_snomed_code and found_condition:
            selected_patient = candidate
            patient_id = candidate_id
            snomed_code = found_snomed_code
            condition_display = found_display
            print(f"Selected condition: {condition_display} (SNOMED: {snomed_code})")
            break

    if not selected_patient or not snomed_code:
        print("\n[ERROR] No suitable patient with a disorder condition found.")
        print("Tip: Token may be expired. Run: python auth/refresh_token.py")
        exit(1)

    # TRANSFORM

    # Step 3: Look up parent concept in Hermes
    parent_id, parent_term = get_parent_concept(snomed_code)

    # LOAD

    # Step 4: Create Patient on Primary Care EHR via POST (server assigns ID)
    primary_care_patient_id, patient_payload = create_patient_on_primary_care(selected_patient)

    # Step 5: Create Condition using parent concept via POST (server assigns ID)
    primary_care_condition_id, condition_payload = create_condition_on_primary_care(
        primary_care_patient_id, parent_id, parent_term
    )

    # VALIDATE

    # Step 6: Validate separately (not part of ETL)
    patient_status_code, patient_data = validate_resource("Patient", patient_payload)
    patient_errors = len([i for i in patient_data.get("issue", []) if i.get("severity") == "error"])

    condition_status_code, condition_data = validate_resource("Condition", condition_payload)
    condition_errors = len([i for i in condition_data.get("issue", []) if i.get("severity") == "error"])

    # SUMMARY
    print("\nTASK 1 SUMMARY")

    patient_name = selected_patient.get("name", [{}])[0]
    print(f"\nEXTRACTION (from OpenEMR FHIR server):")
    print(f"  Search query: GET /Patient?gender={SEARCH_GENDER}&birthdate=gt{SEARCH_BIRTHDATE_AFTER}&_lastUpdated=gt{SEARCH_LAST_UPDATED_AFTER}")
    print(f"  Patient: {patient_name.get('given', [''])[0]} {patient_name.get('family', '')} (ID: {patient_id})")
    print(f"  Condition: {condition_display}")
    print(f"  SNOMED code: {snomed_code}")

    print(f"\nTRANSFORMATION (via Hermes SNOMED terminology server):")
    print(f"  Original code: {snomed_code} ({condition_display})")
    print(f"  Parent concept: {parent_id} ({parent_term})")
    print(f"  Relationship: IS-A (116680003), child maps up to parent")

    print(f"\nLOADING (to Primary Care EHR FHIR server):")
    print(f"  Patient created: ID {primary_care_patient_id}")
    print(f"  Patient saved to: data/patient.json")
    print(f"  Condition created: ID {primary_care_condition_id}")
    print(f"  Condition saved to: data/condition_t1.json")
    print(f"  Condition uses parent concept: {parent_id} ({parent_term})")

    print(f"\nVALIDATION (separate step, not part of ETL):")
    print(f"  Patient profile: {PATIENT_PROFILE}")
    print(f"  Condition profile: {CONDITION_PROFILE}")
    print(f"  Method: POST /$validate with meta.profile on each resource")
    print(f"  Patient validation: {'PASSED' if patient_errors == 0 else f'FAILED ({patient_errors} error(s))'}")
    print(f"  Condition validation: {'PASSED' if condition_errors == 0 else f'FAILED ({condition_errors} error(s))'}")