
<style>
h2 { color:#22c55e !important; font-size:34px; font-weight:800; margin-top:40px; }
h3 { color:#22c55e !important; font-size:26px; font-weight:700; }
.immersive-header-container {
  background: linear-gradient(135deg, #020c1b 0%, #0a2a5e 60%, #0d3d6b 100%);
  color: #fff;
  margin-left: -30px;
  margin-right: -30px;
  padding: 2.5rem 1.5rem 2rem;
  border-radius: 0 0 24px 24px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5);
  margin-bottom: 3rem;
}
.header-content-wrapper { max-width: 920px; margin: 0 auto; text-align: center; }
.header-badge {
  display: inline-block;
  background: rgba(0,180,255,0.15);
  border: 1px solid rgba(0,180,255,0.4);
  color: #7dd3fc; font-size: 0.78rem; font-weight: 700;
  letter-spacing: 0.12em; text-transform: uppercase;
  padding: 0.3rem 1rem; border-radius: 100px; margin-bottom: 1rem;
}
.glow-text {
  color: #fff; text-shadow: 0 0 30px rgba(0,150,255,0.8);
  margin: 0.5rem 0 0.6rem; font-size: 2.2rem; font-weight: 800;
}
.header-subtitle { color: #93c5fd; font-size: 0.95rem; margin-bottom: 1.4rem; }
.dark-nav {
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15);
  padding: 0.7rem 1.2rem; border-radius: 50px; color: #ccc;
  display: inline-block; backdrop-filter: blur(8px); font-size: 0.9rem;
}
.dark-nav strong { color: #fff; margin-right: 6px; }
.dark-nav a { color: #4db8ff !important; text-decoration: none; padding: 0 5px; transition: all 0.25s; }
.dark-nav a:hover { color: #fff !important; text-shadow: 0 0 10px #4db8ff; }
.overview-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem; margin: 2rem 0;
}
.ov-card {
  background: #ffffff; border-radius: 12px; padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1); border-left: 4px solid #22c55e;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.ov-card:hover { transform: translateY(-5px); box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
.ov-card h3 { margin-top: 0; margin-bottom: 1rem; color: #22c55e !important; }
.ov-card p { font-size: 0.87rem; color: #374151; line-height: 1.65; margin: 0; }
</style>

<div class="immersive-header-container">
  <div class="header-content-wrapper">
    <div class="header-badge">INFO-B581 · Spring 2026 · Final Project</div>
    <h1 class="glow-text">Healthcare ETL Pipeline for FHIR Data</h1>
    <p class="header-subtitle">A Python-driven Extract–Transform–Load pipeline connecting OpenEMR, the Hermes SNOMED CT terminology server, and a Primary Care EHR, producing validated FHIR resources and a standards-compliant HL7 v2.5 ADT message.</p>
    <nav class="dark-nav">
      <strong>Navigate:</strong>
      <a href="index.html" style="color:#ffffff!important;text-shadow:0 0 10px #4db8ff;text-decoration:none;">Home</a> |
      <a href="etl_pipeline.html">ETL Pipeline</a> |
      <a href="insights.html">Insights</a> |
      <a href="team_contributions.html">Team Contributions</a> |
      <a href="about.html">About / Presentation</a>
    </nav>
  </div>
</div>

---

## Project Overview

![index1.png](assets/index1.png)

- Builds a healthcare ETL pipeline to transfer patient data between systems.
- Extracts healthcare data from OpenEMR using FHIR APIs.
- Transforms clinical terminology using Hermes SNOMED CT mappings.
- Loads validated resources into the Primary Care FHIR Server.
- Demonstrates secure, standardized, and interoperable healthcare data exchange.

<div class="overview-grid">

  <div class="ov-card">
    <h3>Goal</h3>
    <p>
      Design a reproducible Python-based ETL workflow that extracts healthcare data using FHIR APIs, transforms clinical concepts with SNOMED CT mappings, loads standardized resources into a target FHIR server, validates data using $validate, and demonstrates interoperability through HL7 v2 message generation.
    </p>
  </div>

  <div class="ov-card">
    <h3>Technologies</h3>
    <p>
      <strong>Python 3</strong> – ETL scripting &amp; automation<br>
      <strong>Requests Library</strong> – API communication<br>
      <strong>PyCharm</strong> – Development environment<br>
      <strong>Postman</strong> – API testing &amp; validation<br>
      <strong>FHIR R4 REST APIs</strong> – Healthcare data exchange<br>
      <strong>SNOMED CT</strong> – Clinical terminology mapping<br>
      <strong>HL7apy</strong> – HL7 v2 message generation<br>
      <strong>Git &amp; GitHub</strong> – Version control<br>
      <strong>GitHub Pages</strong> – Project website hosting
    </p>
  </div>

  <div class="ov-card">
    <h3>Data Sources</h3>
    <p>
      <strong>Source System – OpenEMR FHIR API Server</strong><br>
      Provides live healthcare resources including Patients, Conditions, Observations, and Procedures.<br><br>
      <strong>Terminology Source – Hermes SNOMED CT Server</strong><br>
      Used for parent/child concept lookup, preferred terms, and ICD mapping.<br><br>
      <strong>Target System – Primary Care FHIR Server</strong><br>
      Stores transformed, validated healthcare resources.
    </p>
  </div>

  <div class="ov-card">
    <h3>Outcomes</h3>
    <p>
      <strong>Task 1 &amp; 2:</strong> Created Patient and Condition resources using SNOMED mappings.<br><br>
      <strong>Task 3:</strong> Generated Blood Pressure Observation using LOINC coding.<br><br>
      <strong>Task 4 &amp; 5:</strong> Created Procedure resource and generated HL7 v2 ADT message.
    </p>
  </div>

</div>

---

## ETL Pipeline at a Glance

![ETL Pipeline Overview](assets/indeximage.png)

1. **Data Extraction** – Retrieved Patients, Conditions, Observations, and Procedures from OpenEMR.
2. **Terminology Transformation** – Used Hermes SNOMED CT for parent/child concept mapping.
3. **Resource Loading** – Created standardized resources in the Primary Care FHIR server.
4. **Validate** – Verified Patient and Condition resources using $validate.
5. **Interoperability Output** – Generated HL7 v2 ADT message for legacy systems.
6. **Project Outcome** – Demonstrated automated healthcare ETL using Python.

---

## Summary of Deliverables

- **ETL Pipeline** – Python ETL workflow
- **FHIR Integration** – Retrieved Patient, Condition, Observation, Procedure
- **Terminology Mapping** – SNOMED CT parent/child mappings
- **Resource Creation** – Standardized FHIR resources
- **HL7 Output** – HL7 v2 ADT message
- **Validation** – FHIR $validate
- **Project Website** – Documentation + workflow

---

## Quick Links

- [ETL Pipeline Documentation](etl_pipeline.html)
- [Insights](insights.html)
- [Team](team_contributions.html)
- [About](about.html)

---
