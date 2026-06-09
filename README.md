# Healthcare Interoperability Pipeline with FHIR & HL7  


This project demonstrates an end-to-end healthcare data integration workflow using **FHIR APIs**, **SNOMED CT terminology services**, and **HL7 v2 messaging**.
The solution extracts patient data from an OpenEMR source system, transforms clinical information using terminology mapping, and loads standardized resources into a target Primary Care EHR server.

In addition, the project generates an HL7 v2 ADT message to showcase legacy interoperability support.


---

# Core Workflow

The project uses one patient case (**Katherine Schroeder**) across five technical tasks.

## Task 1 - Parent Condition ETL

- Search patient using FHIR parameters  
- Retrieve valid diagnosis from OpenEMR  
- Find broader **SNOMED CT parent concept**  
- Create Patient + Parent Condition in target server  
- Validate resources using `$validate`

## Task 2 - Child Condition ETL

- Reuse patient created in Task 1  
- Retrieve another valid diagnosis  
- Find more specific **SNOMED CT child concept**  
- Create Child Condition resource  
- Validate Condition resource

## Task 3 - Observation ETL

- Check source system for Blood Pressure record  
- Source values missing in FHIR response  
- Load prepared standardized BP JSON document  
- Create Observation in target server

## Task 4 - Procedure ETL

- Search source system for Procedure history  
- If unavailable, generate clinically relevant Procedure  
- Create Procedure resource on target server  

## Task 5 - HL7 ADT Message Generation

- Retrieve Patient + Encounter + Diagnosis data  
- Convert terminology to ICD-10 where needed  
- Generate HL7 v2 ADT^A01 message using Python  

---

# Technology Stack

| Category | Tools |
|---|---|
| Programming | Python |
| APIs | HL7 FHIR REST APIs |
| Terminology | SNOMED CT, ICD-10 |
| Messaging | HL7 v2 |
| Libraries | requests, hl7apy |
| Frontend | GitHub Pages / Jekyll |

---

# Repository Layout

# Repository Structure

```text
FA25_B581_Final_Project_OpenEMR_Group-2/
│
├── assets/                     # Images and website visuals
├── auth/                       # OAuth scripts
│   ├── access_token.py
│   ├── authorization_code.py
│   └── refresh_token.py
│
├── data/                       # JSON templates / generated resources
│   ├── patient.json
│   ├── condition_t1.json
│   ├── condition_t2.json
│   ├── observation_task3.json
│   └── procedure_task4.json
│
├── src/
│   ├── __init__.py
│   └── registration.py
│
├── task3_output/
│   └── bp_observation.json
│
├── task4_output/
│   └── procedure.json
│
├── task5_output/
│   └── task5_adt.txt
│
├── task1.py
├── task2.py
├── task3.py
├── task4.py
├── task5.py
│
├── README.md
├── requirements.txt
├── _config.yml
├── index.md
├── etl_pipeline.md
├── insights.md
├── about.md
└── team_contributions.md

```

## Prerequisites

- Python 3.8
- Access to:
  - OpenEMR FHIR server
  - Primary Care EHR FHIR server
  - Hermes terminology server
- A valid OAuth access token for OpenEMR, placed at `data/access_token.json`:

```json
{
  "access_token": "YOUR_OAUTH_ACCESS_TOKEN_HERE"
}
```
---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.iu.edu/yin10/FinalProject.git
cd FinalProject
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# or
.venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your access token

Place your `access_token.json` file inside the `data/` directory. This file is excluded from version control via `.gitignore`.

---
## Running the Scripts

### Authorization Flow

Before any script can query the FHIR server, the app must complete an OAuth 2.0 authorization flow:

1. The app requests authorization to access patient data.
2. The authorization server returns an **authorization code** - an intermediate credential that does not grant access on its own.
3. The authorization code is exchanged for an **access token**.
4. The app uses the access token to securely query the FHIR server and retrieve or post patient data.

This workflow ensures both interoperability and data privacy.

---

## Running the ETL Scripts

### Task 1 - Parent Term Condition

Retrieves Katherine Schroeder's condition from OpenEMR, finds the **parent** SNOMED CT concept via the Hermes terminology server, and creates both a Patient and Condition resource on the Primary Care EHR FHIR server.

```bash
task1.py
```

### Task 2 - Child Term Condition

Uses the same patient and condition, finds a **child** SNOMED CT concept, and posts the Condition to the Primary Care EHR FHIR server.

```bash
task2.py
```

### Task 3 - Blood Pressure Observation

Creates a Blood Pressure Observation resource for the patient on the Primary Care EHR FHIR server. Checks OpenEMR first; creates one if it does not exist.

```bash
task3.py
```

### Task 4 - Procedure

Retrieves or creates a Procedure (Intravenous blood transfusion of packed cells) resource for the patient and loads it into the Primary Care EHR FHIR server.

```bash
task4.py
```

### Task 5 - HL7 v2 Message Generation

Extracts patient and condition data from OpenEMR, automatically maps the SNOMED CT condition to an **ICD-10** code, and generates a simplified HL7 v2 ADT message (MSH, PID, PV1, DG1 segments). The message is saved to `data/hl7_message.txt`.

```bash
task5.py
```

---

## API Endpoints

| Server | Base URL |
|---|---|
| OpenEMR FHIR Server | `https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir/` |
| Hermes Terminology Server | `http://159.203.121.13:8080/v1/snomed/` |
| Primary Care EHR FHIR Server | `http://159.203.105.138:8080/fhir/` |
| Primary Care Website | `https://dentalinformatics.online/B581` |

---

## Dependencies

All required packages are listed in `requirements.txt`:

```
requests
hl7apy
python-dotenv
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## Notes & Security

- **Do not push API tokens, passwords, or access credentials** to this repository. Store them in a `.env` file - this is already listed in `.gitignore`.
- The `data/` directory contains generated output files such as HL7 `.txt` messages.
- FHIR resource validation is demonstrated **separately** and is not part of the automated ETL flow. See the project website for validation examples.
- All resources include a `meta` field with the appropriate profile URL for validation purposes.

---

# Repository Access

The complete source code and project assets are maintained in the GitHub Enterprise repository below.

**Repository URL:**  
https://github.iu.edu/yin10/FinalProject

## Repository Includes

- Python scripts for Tasks 1–5  
- ETL workflows for Patient, Condition, Observation, Procedure, and HL7 messaging  
- JSON templates and generated output files (excluding credentials)  
- GitHub Pages website content and assets  
- Dependency file (`requirements.txt`)  
- `.gitignore` configuration  
- Project documentation (`README.md`)

---

**Project Website:** https://pages.github.iu.edu/yin10/FinalProject/index.html

---
## Team

| Name | Role |
|---|---|
| Zhenan Yin | Team Lead |
| Aiswarya Perumbilly | ETL & Website Lead |
| Kelli Davis | HL7 & Documentation Lead |
