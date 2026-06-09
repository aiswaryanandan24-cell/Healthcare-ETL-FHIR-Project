# task5.py
# Task 5 - HL7 v2 ADT Message Generation
# Extract patient and condition data from OpenEMR FHIR server.
# Get SNOMED CT preferred term from Hermes terminology server.
# Map SNOMED condition to ICD-10 using Hermes terminology server.
# Construct an HL7 v2 ADT message using hl7apy.
# Save the message to a .txt file.

import json
import requests
from pathlib import Path
from datetime import datetime
from hl7apy.core import Message

# Server URLs
OPENEMR_BASE = "https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir"
HERMES_BASE  = "http://159.203.121.13:8080/v1/snomed"

# Known IDs from Task 1
OPENEMR_PATIENT_ID = "9d035918-b974-4996-b35f-4b913d70f9fd"  # Katherine Schroeder
SNOMED_CODE = "271737000"                               # Anemia

# Fallback values if Hermes is unavailable
FALLBACK_SNOMED_DISPLAY = "Anemia"
FALLBACK_ICD_CODE = "D64.9"
FALLBACK_ICD_DISPLAY = "Anemia, unspecified"

# Output directory
output_dir = Path(__file__).parent / "task5_output"
output_dir.mkdir(exist_ok=True)

# Data directory
data_dir = Path(__file__).parent / "data"

# Authentication
def get_access_token():
    """Read Bearer token from saved access_token.json."""
    with open(data_dir / "access_token.json", "r") as f:
        return json.load(f).get("access_token")

def get_openemr_headers():
    return {
        "Authorization": f"Bearer {get_access_token()}",
        "Accept": "application/json"
    }

# Step 1: Extract patient data from OpenEMR
def get_patient(patient_id):
    """
    Fetch patient resource from OpenEMR by ID.
    Extracts name, gender, birth date, and address for use in PID segment.
    """
    print(f"\n Step 1: Extracting patient data from OpenEMR")

    response = requests.get(
        f"{OPENEMR_BASE}/Patient/{patient_id}",
        headers=get_openemr_headers()
    )
    patient = response.json()

    name = patient.get("name", [{}])[0]
    given = name.get("given", ["Unknown"])[0]
    family = name.get("family", "Unknown")
    gender = patient.get("gender", "unknown")
    birthdate = patient.get("birthDate", "unknown")
    address = patient.get("address", [{}])[0]
    city = address.get("city", "")
    state = address.get("state", "")

    print(f" Patient: {given} {family}")
    print(f" ID: {patient_id}")
    print(f" Gender: {gender}")
    print(f" Birthdate: {birthdate}")
    print(f" City: {city} | State: {state}")

    return {
        "id": patient_id,
        "given": given,
        "family": family,
        "gender": "M" if gender == "male" else "F",
        "birthdate": birthdate.replace("-", ""),  # HL7 format: YYYYMMDD
        "city": city,
        "state": state
    }

# Step 2: Get SNOMED CT preferred term from Hermes
def get_preferred_term(snomed_code):
    """
    Get the official SNOMED CT preferred term for a concept from Hermes.
    This is the preferred description as defined in the SNOMED CT terminology
    Falls back to a default if Hermes is unavailable.
    """
    print(f"\n Step 2: Fetching SNOMED CT preferred term for {snomed_code}")

    response = requests.get(f"{HERMES_BASE}/concepts/{snomed_code}/extended")

    if response.status_code != 200:
        print(f" Hermes returned {response.status_code}. Using fallback: {FALLBACK_SNOMED_DISPLAY}")
        return FALLBACK_SNOMED_DISPLAY

    preferred_term = response.json().get("preferredDescription", {}).get("term", FALLBACK_SNOMED_DISPLAY)
    print(f" SNOMED CT preferred term: {preferred_term}")
    return preferred_term


# Step 3: Map SNOMED to ICD-10 via Hermes
def get_icd_mapping(snomed_code):
    """
    Map a SNOMED CT code to ICD-10 using the Hermes terminology server.
    Uses the /refsets endpoint which returns cross-map reference set entries.
    Falls back to a hardcoded ICD-10 code if mapping is unavailable.
    """
    print(f"\n Step 3: Mapping SNOMED {snomed_code} to ICD-10 via Hermes ")

    response = requests.get(f"{HERMES_BASE}/concepts/{snomed_code}/refsets")

    if response.status_code != 200:
        print(f" Hermes refsets endpoint returned {response.status_code}. Using fallback ICD-10.")
        print(f" Fallback: {FALLBACK_ICD_CODE} | {FALLBACK_ICD_DISPLAY}")
        return FALLBACK_ICD_CODE, FALLBACK_ICD_DISPLAY

    items = response.json()
    if isinstance(items, dict):
        items = items.get("items", [])

    if not items:
        print(f" No ICD-10 mapping found in Hermes. Using fallback ICD-10.")
        print(f" Fallback: {FALLBACK_ICD_CODE} | {FALLBACK_ICD_DISPLAY}")
        return FALLBACK_ICD_CODE, FALLBACK_ICD_DISPLAY

    for item in items:
        map_target = item.get("mapTarget", "")
        map_advice = item.get("mapAdvice", "")
        if map_target:
            print(f" ICD-10 code: {map_target}")
            print(f" Map advice: {map_advice}")
            return map_target, map_advice

    print(f" No usable ICD-10 mapping found. Using fallback.")
    print(f" Fallback: {FALLBACK_ICD_CODE} | {FALLBACK_ICD_DISPLAY}")
    return FALLBACK_ICD_CODE, FALLBACK_ICD_DISPLAY


# Step 4: Build HL7 v2 ADT message using hl7apy
def build_adt_message(patient, snomed_display, icd_code, icd_display):
    """
    Construct an HL7 v2 ADT^A01 (Admit) message using hl7apy.
    Includes MSH, PID, PV1, and DG1 segments.
    Uses the SNOMED CT preferred term in the DG1 segment description.
    """
    print(f"\n Step 4: Building HL7 v2 ADT^A01 message ")

    now = datetime.now().strftime("%Y%m%d%H%M%S")

    msg = Message("ADT_A01", version="2.5")

    # MSH - Message Header
    msg.msh.msh_3 = "OpenEMR"           # Sending application
    msg.msh.msh_4 = "IU_Health"         # Sending facility
    msg.msh.msh_5 = "PrimaryCareEHR"    # Receiving application
    msg.msh.msh_6 = "PrimaryCare"       # Receiving facility
    msg.msh.msh_7 = now                 # Message datetime
    msg.msh.msh_9 = "ADT^A01"           # Message type
    msg.msh.msh_10 = "MSG00001"          # Message control ID
    msg.msh.msh_11 = "P"                 # Processing ID (P = Production)

    # PID - Patient Identification
    msg.pid.pid_3 = patient["id"]
    msg.pid.pid_5 = f"{patient['family']}^{patient['given']}"
    msg.pid.pid_7 = patient["birthdate"]
    msg.pid.pid_8 = patient["gender"]
    msg.pid.pid_11 = f"^^{patient['city']}^{patient['state']}"

    # PV1 - Patient Visit
    msg.pv1.pv1_2 = "I"                # Patient class (I = Inpatient)
    msg.pv1.pv1_3 = "ICU^101^A"        # Assigned patient location
    msg.pv1.pv1_44 = now                # Admit datetime

    # DG1 - Diagnosis
    # Uses ICD-10 code for the standard coding system field,
    # and includes the SNOMED CT preferred term as the description
    msg.dg1.dg1_1 = "1"
    msg.dg1.dg1_3 = f"{icd_code}^{snomed_display}^I10"
    msg.dg1.dg1_5 = now
    msg.dg1.dg1_6 = "A"               # Diagnosis type (A = Admitting)

    print(f" MSH: Sending OpenEMR to PrimaryCareEHR")
    print(f" PID: {patient['given']} {patient['family']} | DOB: {patient['birthdate']} | Gender: {patient['gender']}")
    print(f" PV1: Inpatient admission")
    print(f" DG1: {icd_code} | {snomed_display} (SNOMED preferred term)")

    return msg.to_er7()

# Step 5: Save HL7 message to file
def save_adt_message(hl7_message):
    output_path = output_dir / "task5_adt.txt"
    with open(output_path, "w") as f:
        # Replace \r with \r\n so each segment appears on its own line
        # Standard HL7 v2 uses \r as segment separator, but \r\n improves readability
        readable = hl7_message.replace("\r", "\r\n")
        f.write(readable)
    print(f"\n Step 5: Saving HL7 message ")
    print(f" Saved to: {output_path}")
    return output_path

# Main
if __name__ == "__main__":

    # EXTRACT
    # Step 1: Extract patient data from OpenEMR
    patient = get_patient(OPENEMR_PATIENT_ID)

    # TRANSFORM
    # Step 2: Fetch SNOMED CT preferred term from Hermes
    snomed_display = get_preferred_term(SNOMED_CODE)

    # Step 3: Map SNOMED to ICD-10 via Hermes
    icd_code, icd_display = get_icd_mapping(SNOMED_CODE)

    # Step 4: Build HL7 v2 ADT message
    hl7_message = build_adt_message(patient, snomed_display, icd_code, icd_display)

    # LOAD
    # Step 5: Save to file
    output_path = save_adt_message(hl7_message)

    # SUMMARY
    print("TASK 5 SUMMARY")

    print(f"\nEXTRACTION (from OpenEMR FHIR server):")
    print(f" Patient: {patient['given']} {patient['family']} (ID: {OPENEMR_PATIENT_ID})")
    print(f" Condition: SNOMED {SNOMED_CODE}")

    print(f"\nTRANSFORMATION (via Hermes SNOMED terminology server):")
    print(f" SNOMED code: {SNOMED_CODE}")
    print(f" SNOMED preferred term: {snomed_display}")
    print(f" ICD-10 code: {icd_code} | Map advice: {icd_display}")

    print(f"\nHL7 v2 MESSAGE:")
    print(f" Type: ADT^A01 (Admit)")
    print(f" Segments: MSH, PID, PV1, DG1")
    print(f" Saved to: {output_path}")

    print(f"\nHL7 MESSAGE CONTENT:")
    for segment in hl7_message.split("\r"):
        if segment.strip():
            print(f"  {segment}")
