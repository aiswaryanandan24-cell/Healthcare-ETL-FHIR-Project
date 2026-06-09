---
layout: default
title: About / Presentation
---

<style>
h2 { color:#22c55e !important; font-size:34px; font-weight:800; margin-top:40px; }
h3 { color:#22c55e !important; font-size:26px; font-weight:700; }

/* ── HEADER ── */
.immersive-header-container {
  background: linear-gradient(135deg, #020c1b 0%, #0a2a5e 60%, #0d3d6b 100%);
  color: #fff;
  margin-left: -30px; margin-right: -30px;
  padding: 2.5rem 1.5rem 2rem;
  border-radius: 0 0 24px 24px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5);
  margin-bottom: 3rem;
  position: relative; overflow: hidden;
}
.header-content-wrapper { max-width: 900px; margin: 0 auto; text-align: center; }
.header-badge { display:inline-block; background:rgba(0,180,255,0.15); border:1px solid rgba(0,180,255,0.4); color:#7dd3fc; font-size:0.78rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; padding:0.3rem 1rem; border-radius:100px; margin-bottom:1rem; }
.glow-text { color:#fff; text-shadow:0 0 30px rgba(0,150,255,0.8); font-size:2.2rem; font-weight:800; margin:0.4rem 0 0.6rem; line-height:1.12; }
.header-subtitle { color:#93c5fd; font-size:0.88rem; margin-bottom:1.6rem; }
.dark-nav { background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); padding:0.6rem 1.2rem; border-radius:100px; display:inline-block; font-size:0.82rem; color:#9ca3af; }
.dark-nav strong { color:#fff; margin-right:6px; }
.dark-nav a { color:#4db8ff !important; text-decoration:none; padding:0 5px; transition:all 0.2s; }
.dark-nav a:hover { color:#fff !important; text-shadow:0 0 10px #4db8ff; }

/* ── TASK HEADERS ── */
.task-hdr { display:flex; align-items:center; gap:1rem; padding:0.85rem 1.2rem; border-radius:8px; margin:1.5rem 0 1rem; }
.t-teal { background:#e0f2f0; border-left:4px solid #0077cc; }
.t-purple { background:#f3f0ff; border-left:4px solid #7c3aed; }
.t-coral { background:#fff1f0; border-left:4px solid #e02020; }
.task-label { font-family:monospace; font-size:0.7rem; font-weight:700; background:#0077cc; color:#fff; padding:3px 10px; border-radius:4px; white-space:nowrap; }
.t-purple .task-label { background:#7c3aed; }
.t-coral .task-label { background:#e02020; }
.task-title { font-size:0.88rem; font-weight:600; color:#1e293b; }

/* ── TERMINAL BLOCKS ── */
.terminal {
  background: #0f172a;
  border-radius: 10px;
  overflow: hidden;
  margin: 1rem 0;
  border: 1px solid #1e293b;
}
.terminal::before {
  content: "Terminal Output";
  display: block;
  background: #1e293b;
  color: #22c55e;
  padding: 10px 18px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.terminal-pre {
  display: block !important;
  margin: 0 !important;
  padding: 1.2rem 1.4rem !important;
  color: #e2e8f0 !important;
  background: #0f172a !important;
  font-family: Consolas, Monaco, 'Courier New', monospace !important;
  font-size: 0.82rem !important;
  line-height: 1.75 !important;
  white-space: pre !important;
  overflow-x: auto !important;
  overflow-y: visible !important;
  max-height: none !important;
  height: auto !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  word-break: normal !important;
}

/* ── HL7 BLOCK ── */
.hl7-block { background:#0c1a2e; border:1px solid rgba(0,180,255,0.25); border-radius:10px; overflow:hidden; margin:1rem 0; }
.hl7-block pre { margin:0; padding:1rem 1.2rem; color:#7dd3fc; font-family:monospace; font-size:0.8rem; line-height:1.85; overflow-x:auto; }

/* ── RESULT BAR ── */
.result-bar { display:flex; flex-wrap:wrap; gap:0.6rem; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:0.9rem 1.1rem; margin:1rem 0; }
.rb-item { display:flex; flex-direction:column; gap:2px; }
.rb-label { font-size:0.6rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#94a3b8; }
.rb-val { font-family:monospace; font-size:0.75rem; color:#1e293b; background:#e2e8f0; padding:2px 8px; border-radius:4px; }
.rb-val.ok { background:#dcfce7; color:#166534; font-weight:700; }
</style>

<div class="immersive-header-container">
  <div class="header-content-wrapper">
    <div class="header-badge">About the Project</div>
    <h1 class="glow-text">About &amp; Presentation</h1>
    <p class="header-subtitle">INFO-B581 &middot; Spring 2026 &middot; Healthcare Data Interoperability ETL Pipeline</p>
    <nav class="dark-nav">
      <strong>Navigate:</strong>
      <a href="index.html">Home</a> |
      <a href="etl_pipeline.html">ETL Pipeline</a> |
      <a href="insights.html">Insights</a> |
      <a href="team_contributions.html">Team Contributions</a> |
      <a href="about.html" style="color:#ffffff!important;text-shadow:0 0 10px #4db8ff;text-decoration:none;">About / Presentation</a>
    </nav>
  </div>
</div>

---

## About the Team

Our three-member team project for INFO-B581 (Spring 2026) developed a Python-based healthcare ETL pipeline showcasing FHIR interoperability, SNOMED CT mapping, validation, and HL7 v2 messaging using realistic clinical training data.

| Member | Role |
|---|---|
| Zhenan Yin | ETL Lead - Tasks 1, 2, 3, GitHub setup, team coordination |
| Aiswarya Perumbilly | Website &amp; Content Lead - Task 4, website design, presentation |
| Kelli Davis | Interoperability Lead - Task 5, HL7 messaging, terminology mapping, testing |

---

## Introduction

Healthcare systems often struggle to exchange data due to incompatible formats, standards, and protocols, so our project created an end-to-end healthcare ETL workflow that transfers, standardizes, and validates patient data across interoperable systems using modern healthcare standards.

1. **Data Extraction** - Retrieved Patients, Conditions, Observations, and Procedures from OpenEMR.
2. **Terminology Transformation** - Used Hermes SNOMED CT for parent/child concept mapping.
3. **Resource Loading** - Created standardized resources in the Primary Care FHIR server.
4. **Validation** - Verified Patient and Condition resources using $validate.
5. **Interoperability Output** - Generated HL7 v2 ADT message for legacy systems.
6. **Project Outcome** - Demonstrated automated healthcare ETL using Python.

### What is a FHIR API?

- FHIR (Fast Healthcare Interoperability Resources) is the standard used in our project to exchange healthcare data electronically through simple REST APIs and JSON between OpenEMR and the Primary Care FHIR server.
- We used key FHIR resources such as Patient, Condition, Observation, and Procedure to transfer, standardize, and validate clinical data securely across systems.

### Our Pipeline at a Glance

**Patient followed throughout:** Katherine Schroeder  &middot; DOB 1951-10-26

![about3.png](assets/about3.png)


![about1.png](assets/about1.png)

---

## Task 1 - Patient + Parent Condition

<div class="task-hdr t-teal">
  <span class="task-label">Task 1</span>
  <span class="task-title">Extract &rarr; Transform (IS-A Parent) &rarr; Load &rarr; Validate</span>
</div>


**EXTRACT:** 
- Searched OpenEMR patients using FHIR search parameters:
  `gender=female&birthdate=gt1951-01-01&_lastUpdated=gt2020-01-01`.
- Retrieved patient conditions and selected valid disorder: Anemia.
- Identified SNOMED CT code: 271737000.

**TRANSFORM:** 
- Queried Hermes terminology server for parent SNOMED concept.
- Found parent concept: Disorder of cellular component of blood-414022008(SNOMED CT concept ID).
- Mapped the diagnosis (Anemia) to its broader SNOMED CT parent concept for ETL transformation.

**LOAD:** 
- A new Patient and Parent Condition were created in the Primary Care FHIR server and successfully validated using `$validate`.

### Terminal Output

<div class="terminal">
<pre class="terminal-pre">
Step 1: GET /Patient?gender=female&birthdate=gt1951-01-01&_lastUpdated=gt2020-01-01
Total patients found: 5118
  [0] 9d035918-b974-4996-b35f-4b913d70f9fd | Katherine Schroeder | DOB: 1951-10-26
Step 2: Conditions for patient - 132 total
  [3] Anemia (disorder) selected
  Hermes → Found: 271737000 | Anemia
Step 3: Parent lookup for SNOMED 271737000
  Direct parent concept ID: 414022008
  Parent preferred term: Disorder of cellular component of blood
Step 4: Patient created → Primary Care Patient ID: {ID}
Step 5: Condition created → Primary Care Condition ID: {ID}
Validation Patient   → POST /Patient/$validate   → 200 PASSED
Validation Condition → POST /Condition/$validate → 200 PASSED
</pre>
</div>

- The system searched OpenEMR, selected **Katherine Schroeder**, identified her **Anemia** condition, and used Hermes to find the parent SNOMED concept.
- After that, a new **Patient** and **Condition** were created in the Primary Care FHIR server, and both resources passed validation successfully (**HTTP 200**).
  
<div class="result-bar">
  <div class="rb-item">
    <span class="rb-label">Source SNOMED</span>
    <span class="rb-val">271737000 - Anemia</span>
  </div>
  <div class="rb-item">
    <span class="rb-label">Parent SNOMED</span>
    <span class="rb-val">414022008 - Disorder of cellular component of blood</span>
  </div>
  <div class="rb-item">
    <span class="rb-label">Patient ID</span>
    <span class="rb-val ok">{ID}</span>
  </div>
  <div class="rb-item">
    <span class="rb-label">Condition ID</span>
    <span class="rb-val ok">{ID}</span>
  </div>
  <div class="rb-item">
    <span class="rb-label">Validation</span>
    <span class="rb-val ok">HTTP 200 PASSED</span>
  </div>
</div>

---

## Task 2 - Create Child Condition

<div class="task-hdr t-teal">
  <span class="task-label">Task 2</span>
  <span class="task-title">Extract &rarr; Transform (ECL Child) &rarr; Load &rarr; Validate</span>
</div>

**EXTRACT:** 
- Retrieved Katherine Schroeder’s Condition records from OpenEMR.
- Selected a valid clinical diagnosis: Essential hypertension (SNOMED CT: 59621000).

**TRANSFORM:** 
- Queried Hermes using child concept (ECL) lookup.
- Mapped to a more specific child concept: 1201005 - Benign essential hypertension.

**LOAD:** 
- Created a new Condition resource on the Target FHIR server.
- Successfully validated the resource using `$validate`.

### Terminal Output

<div class="terminal">
<pre class="terminal-pre">
Step 3: Selecting disorder (skipping 'Anemia')
  Found: 59621000 | Essential hypertension
Step 4: Child concept for SNOMED 59621000
  Child concept ID:   1201005
  Child concept term: Benign essential hypertension
Step 5: Condition ID {ID} - linked to Patient {ID}
Validation → HTTP 200 PASSED 
</pre>
</div>

- The system selected Essential hypertension as the next valid diagnosis.
- Hermes was used to find a more specific child concept, returning **1201005 - Benign essential hypertension.**
- A new Condition resource was created for Patient and passed validation successfully (**HTTP 200**).

<div class="result-bar">
  <div class="rb-item"><span class="rb-label">Source SNOMED</span><span class="rb-val">59621000 - Essential hypertension</span></div>
  <div class="rb-item"><span class="rb-label">ECL Query</span><span class="rb-val">&lt;!59621000</span></div>
  <div class="rb-item"><span class="rb-label">Child SNOMED</span><span class="rb-val">1201005 - Benign essential hypertension</span></div>
  <div class="rb-item"><span class="rb-label">Condition ID</span><span class="rb-val ok">{ID}</span></div>
  <div class="rb-item"><span class="rb-label">Validation</span><span class="rb-val ok">HTTP 200 PASSED</span></div>
</div>

---

## Task 3 - Blood Pressure Observation


<div class="task-hdr t-teal">
  <span class="task-label">Task 3</span>
  <span class="task-title">Extract (check OpenEMR) &rarr; Transform (JSON Source) &rarr; Load</span>
</div>


**EXTRACT:** 
- Retrieved Katherine Schroeder’s Blood Pressure record from OpenEMR.
- Since FHIR values were missing, used source vitals 124/73 mmHg.
  
**TRANSFORM:** 
- Loaded the prepared JSON Observation file (`observation_task3.json`).
- Updated the subject reference to target patient record.

**LOAD:** 
- Created a new Blood Pressure Observation on the Target FHIR server.
- Successfully saved the output locally.

### Terminal Output

<div class="terminal">
<pre class="terminal-pre">
GET /Observation?patient=9d035918...&amp;category=vital-signs&amp;code=85354-9
Blood Pressure Observations found: 1

BP record found but values are absent (dataAbsentReason: unknown).
OpenEMR FHIR API does not expose actual vitals values.

Loaded BP Observation from data/observation_task3.json
Systolic  (LOINC 8480-6): 124 mmHg
Diastolic (LOINC 8462-4):  73 mmHg

Observation updated successfully.
Primary Care Observation ID: {ID}
</pre>
</div>

- The system confirmed that **Blood Pressure Observation** existed in OpenEMR.
- Since the values were unavailable in the API response, the JSON document was used.
- A new Observation resource was created successfully in the Primary Care FHIR server.

<div class="result-bar">
  <div class="rb-item"><span class="rb-label">LOINC</span><span class="rb-val">85354-9 - Blood pressure panel</span></div>
  <div class="rb-item"><span class="rb-label">OpenEMR Status</span><span class="rb-val">1 found - values absent</span></div>
  <div class="rb-item"><span class="rb-label">Values Used</span><span class="rb-val">124 / 73 mmHg</span></div>
  <div class="rb-item"><span class="rb-label">JSON Source</span><span class="rb-val">observation_task3.json</span></div>
  <div class="rb-item"><span class="rb-label">Observation ID</span><span class="rb-val ok">{ID}</span></div>
</div>

---

## Task 4 - Procedure

**EXTRACT:** 
- Checked Procedure records for Katherine Schroeder in OpenEMR.
- No existing Procedure resources were found for this patient.

**TRANSFORM:** 
- Prepared a Procedure JSON template based on the patient’s Anemia history.
- Selected Intravenous blood transfusion of packed cells as a clinically relevant procedure.
  
**LOAD:** 
- Posted a new Procedure resource on the Target FHIR server linked to the patient.
- Confirmed successful creation and stored the generated Procedure ID.


### Terminal Output

<div class="terminal">
<pre class="terminal-pre">
GET /Procedure?patient=9d035918-b974-4996-b35f-4b913d70f9fd
Procedures found in OpenEMR: 0

No Procedures found in OpenEMR.
A new clinically relevant procedure will be created from the JSON document.

Loaded Procedure from data/procedure_task4.json
Procedure: Intravenous blood transfusion of packed cells (SNOMED: 180207008)

Procedure created → Primary Care Procedure ID: ID
Status: completed | Performed: 2010-12-17
</pre>
</div>


<div class="result-bar">
  <div class="rb-item"><span class="rb-label">Procedures in OpenEMR</span><span class="rb-val">0 found</span></div>
  <div class="rb-item"><span class="rb-label">JSON Source</span><span class="rb-val">procedure_task4.json</span></div>
  <div class="rb-item"><span class="rb-label">Procedure</span><span class="rb-val">Blood transfusion of packed cells</span></div>
  <div class="rb-item"><span class="rb-label">SNOMED</span><span class="rb-val">180207008</span></div>
  <div class="rb-item"><span class="rb-label">Procedure ID</span><span class="rb-val ok">{ID}</span></div>
</div>

---

## Task 5 - HL7 v2 ADT Message Generation

**EXTRACT:** 
- Retrieved Katherine Schroeder’s demographic details and diagnosis Anemia (SNOMED 271737000) from OpenEMR for message creation.  

**TRANSFORM:** 
- Used Hermes to map SNOMED CT 271737000 to ICD-10 D64.9 and converted the patient data into an HL7 v2 **ADT^A01** message with MSH, PID, PV1, and DG1 segments.  

**LOAD:** 
- Exported the completed HL7 message successfully as **task5_adt.txt**.
- Enabled compatibility with legacy healthcare systems using HL7 format.

<div class="task-hdr t-coral">
  <span class="task-label">Task 5</span>
  <span class="task-title">Extract &rarr; Transform (SNOMED &rarr; ICD-10) &rarr; Build HL7 &rarr; Export</span>
</div>

### Generated HL7 Message

<div class="hl7-block">
<pre>
MSH|^~\&|OpenEMR|IU_Health|PrimaryCareEHR|PrimaryCare|20260413155439||ADT^A01|MSG00001|P|2.5
PID|||9d035918-b974-4996-b35f-4b913d70f9fd||Schroeder^Katherine||19511026|F|||^^Leominster^Massachusetts
PV1||I|ICU^101^A|||||||||||||||||||||||||||||||||||||||||20260413155439
DG1|1||D64.9^Anemia^I10||20260413155439|A
</pre>
</div>

### Segment Breakdown

| Segment | Purpose | Key Values |
|---|---|---|
| MSH | Message header | Sender OpenEMR, receiver PrimaryCareEHR, message type **ADT^A01** |
| PID | Patient identification | Name, DOB, gender, and address |
| PV1 | Patient visit | Inpatient status (I) and assigned ICU room ICU^101^A |
| DG1 | Diagnosis | ICD-10 code (auto mapped) **D64.9** and Anemia |

### Why This Supports Legacy Interoperability

- Converts modern FHIR patient data into **HL7 v2** format used by older hospital systems.
- Helps systems like lab, radiology, and billing communicate without using FHIR directly.
- ICD-10 code **D64.9** was mapped automatically from SNOMED using Hermes.
- Reduces manual coding errors and improves data exchange.
- Final message was saved as **task5_adt.txt**.

<div class="result-bar">
  <div class="rb-item"><span class="rb-label">SNOMED</span><span class="rb-val">271737000 - Anemia</span></div>
  <div class="rb-item"><span class="rb-label">ICD-10 mapped</span><span class="rb-val">D64.9 (Hermes mapping)</span></div>
  <div class="rb-item"><span class="rb-label">HL7 type</span><span class="rb-val">ADT^A01 v2.5</span></div>
  <div class="rb-item"><span class="rb-label">Segments</span><span class="rb-val">MSH · PID · PV1 · DG1</span></div>
  <div class="rb-item"><span class="rb-label">Output</span><span class="rb-val ok">task5_adt.txt ✓</span></div>
</div>

---

## Complete Results Summary

| Task   | Resource         | Key Values                                                                 | Status              |
|--------|------------------|----------------------------------------------------------------------------|---------------------|
| Task 1 | Patient          | Katherine Schroeder · DOB 1951-10-26                                      | Validated HTTP 200  |
| Task 1 | Parent Condition | SNOMED 414022008 - Disorder of cellular component of blood                | Validated HTTP 200  |
| Task 2 | Child Condition  | SNOMED 1201005 - Benign essential hypertension                            | Validated HTTP 200  |
| Task 3 | BP Observation   | 124/73 mmHg · LOINC 85354-9                                               | Created             |
| Task 4 | Procedure        | SNOMED 180207008 - Intravenous blood transfusion of packed cells · 2010-12-17 | Created         |
| Task 5 | HL7 v2.5 ADT     | ICD-10 D64.9 ← SNOMED 271737000 (Anemia)                                  | Exported            |

---

## Key Insights & Best Practices Applied

- Real healthcare data can be complex and inconsistent, so filtering valid conditions is important.
- SNOMED CT parent and child mappings improved diagnosis accuracy.
- Standard FHIR APIs enabled data extraction, creation, and exchange.
- Missing values were handled using fallback logic.
- FHIR resources and HL7 v2 messages demonstrated interoperability.

---

## Challenges &amp; Resolutions

| Challenge | Resolution |
|---|---|
| OAuth2 token expiry | Reloaded token before running scripts |
| Many invalid conditions | Filtered only valid disorder terms |
| Missing required fields | Added missing fields during transformation |
| BP values absent in API | Loaded actual vitals (124/73 mmHg) from JSON |
| HL7 message readability issues | Saved each segment on a new line |

---

## Conclusion - Value for a Healthcare Organization

This project demonstrates how a healthcare organization can safely transfer patient data into a new system while improving interoperability and data quality.

- **Standard terminology** keeps diagnoses consistent across systems.
- **Automatic ICD-10 mapping** reduces manual coding work and errors.
- **Validation checks** improve data quality before loading records.
- **HL7 v2 output** helps older systems continue to communicate.
- **Sequential IDs** confirm resources were created successfully.

This ETL pipeline creates a repeatable and reliable process for healthcare data exchange - a foundation for ongoing clinical data interoperability.


