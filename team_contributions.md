---
layout: default
title: Team Contributions
---

<style>
h2 { color:#22c55e !important; font-size:34px; font-weight:800; margin-top:40px; }
h3 { color:#22c55e !important; font-size:26px; font-weight:700; }
.immersive-header-container {
  background: linear-gradient(135deg, #020c1b 0%, #0a2a5e 60%, #0d3d6b 100%);
  color: #fff;
  margin-left: -30px; margin-right: -30px;
  padding: 2.5rem 1.5rem 2rem;
  border-radius: 0 0 24px 24px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5);
  margin-bottom: 3rem;
}
.header-content-wrapper { max-width: 920px; margin: 0 auto; text-align: center; }
.header-badge { display: inline-block; background: rgba(0,180,255,0.15); border: 1px solid rgba(0,180,255,0.4); color: #7dd3fc; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; padding: 0.3rem 1rem; border-radius: 100px; margin-bottom: 1rem; }
.glow-text { color: #fff; text-shadow: 0 0 30px rgba(0,150,255,0.8); margin: 0.5rem 0 0.6rem; font-size: 2.2rem; font-weight: 800; }
.header-subtitle { color: #93c5fd; font-size: 0.95rem; margin-bottom: 1.4rem; }
.dark-nav { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15); padding: 0.7rem 1.2rem; border-radius: 50px; color: #ccc; display: inline-block; backdrop-filter: blur(8px); font-size: 0.9rem; }
.dark-nav strong { color: #fff; margin-right: 6px; }
.dark-nav a { color: #4db8ff !important; text-decoration: none; padding: 0 5px; transition: all 0.25s; }
.dark-nav a:hover { color: #fff !important; text-shadow: 0 0 10px #4db8ff; }

/* ===== TEAM GRID ===== */
.team-grid { display: flex; flex-direction: column; gap: 2.5rem; margin: 2rem 0; }
.team-card { background: #fff; border-radius: 16px; padding: 2.2rem; box-shadow: 0 6px 28px rgba(0,0,0,0.09); transition: box-shadow 0.3s; }
.team-card:hover { box-shadow: 0 14px 40px rgba(0,0,0,0.14); }
.card-blue   { border-top: 5px solid #2563eb; }
.card-green  { border-top: 5px solid #059669; }
.card-purple { border-top: 5px solid #7c3aed; }
.member-header { display: flex; align-items: center; gap: 1.5rem; margin-bottom: 1.5rem; padding-bottom: 1.2rem; border-bottom: 2px solid #f1f5f9; }
.avatar-circle { width: 76px; height: 76px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; flex-shrink: 0; }
.avatar-blue   { background: #dbeafe; border: 3px solid #2563eb; }
.avatar-green  { background: #d1fae5; border: 3px solid #059669; }
.avatar-purple { background: #ede9fe; border: 3px solid #7c3aed; }
.member-info h2 { margin: 0; color: #1e293b; font-size: 1.3rem; }
.role-badge { display: inline-block; font-size: 0.78rem; font-weight: 700; padding: 0.25rem 0.8rem; border-radius: 100px; margin-top: 0.4rem; letter-spacing: 0.04em; }
.badge-blue   { background: #dbeafe; color: #1e40af; }
.badge-green  { background: #d1fae5; color: #065f46; }
.badge-purple { background: #ede9fe; color: #5b21b6; }
.team-card h3 { color: #0077cc; font-size: 0.92rem; margin: 1.2rem 0 0.6rem; text-transform: uppercase; letter-spacing: 0.06em; }
.team-card ul { margin: 0; padding-left: 1.4rem; }
.team-card li { font-size: 0.87rem; margin-bottom: 0.45rem; color: #334155; line-height: 1.55; }
.team-card li code { background: #f1f5f9; padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.8rem; }
.team-card blockquote { background: #f8fafc; border-left: 4px solid #0077cc; padding: 1rem 1.3rem; margin: 1.2rem 0 0; font-style: italic; color: #475569; border-radius: 0 10px 10px 0; font-size: 0.87rem; line-height: 1.65; }
.card-blue   blockquote { border-color: #2563eb; }
.card-green  blockquote { border-color: #059669; }
.card-purple blockquote { border-color: #7c3aed; }

/* ===== DELIVERABLES ===== */
.deliverables-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px,1fr)); gap: 0.6rem; margin: 0.8rem 0; }
.deliverable { background: #f1f5f9; border-radius: 8px; padding: 0.5rem 0.9rem; font-size: 0.82rem; color: #334155; font-weight: 500; }

/* ===== RESULTS PILLS ===== */
.results-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.8rem 0; }
.result-pill { display: inline-block; font-size: 0.78rem; font-weight: 600; padding: 0.3rem 0.8rem; border-radius: 100px; }
.pill-blue   { background: #dbeafe; color: #1e40af; }
.pill-green  { background: #d1fae5; color: #065f46; }
.pill-purple { background: #ede9fe; color: #5b21b6; }

/* ===== SUMMARY TABLE ===== */
.summary-table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; box-shadow: 0 2px 12px rgba(0,0,0,0.08); border-radius: 12px; overflow: hidden; }
.summary-table th { background: #0a2a5e; color: #fff; padding: 0.9rem 1rem; text-align: left; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.06em; }
.summary-table td { padding: 0.85rem 1rem; font-size: 0.85rem; border-bottom: 1px solid #e2e8f0; }
.summary-table tr:nth-child(even) { background: #f8fafc; }
.summary-table tr:hover { background: #eff6ff; }

/* ===== SHARED GRID ===== */
.shared-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap: 1.2rem; margin: 1.5rem 0; }
.shared-card { background: #f8fafc; border-radius: 12px; padding: 1.4rem; border-left: 4px solid #7c3aed; transition: transform 0.2s; }
.shared-card:hover { transform: translateY(-3px); }
.shared-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
.shared-card h4 { margin: 0 0 0.5rem; color: #1e293b; font-size: 0.92rem; }
.shared-card p  { margin: 0; font-size: 0.84rem; color: #475569; line-height: 1.55; }

/* ===== LESSONS GRID ===== */
.lessons-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px,1fr)); gap: 1.5rem; margin: 1.5rem 0; }
.lesson-section { background: #fff; border-radius: 12px; padding: 1.6rem; box-shadow: 0 2px 12px rgba(0,0,0,0.07); border-top: 4px solid #0077cc; }
.lesson-section h4 { margin: 0 0 0.9rem; color: #1e293b; font-size: 0.95rem; }
.lesson-section ul { margin: 0; padding-left: 1.3rem; }
.lesson-section li { font-size: 0.86rem; margin-bottom: 0.45rem; color: #334155; line-height: 1.5; }
.lesson-section code { background: #e2e8f0; padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.82rem; }
</style>

<div class="immersive-header-container">
  <div class="header-content-wrapper">
    <div class="header-badge">Our Team</div>
    <h1 class="glow-text">Team Contributions</h1>
    <p class="header-subtitle">Roles, responsibilities, and reflections from all three members</p>
    <nav class="dark-nav">
      <strong>Navigate:</strong>
      <a href="index.html">Home</a> |
      <a href="etl_pipeline.html">ETL Pipeline</a> |
      <a href="insights.html">Insights</a> |
      <a href="team_contributions.html" style="color:#ffffff!important;text-shadow:0 0 10px #4db8ff;text-decoration:none;">Team Contributions</a> |
      <a href="about.html">About / Presentation</a>
    </nav>
  </div>
</div>

## Team Roles & Responsibilities

Our three-member team built a complete ETL pipeline integrating **OpenEMR FHIR**, **Hermes SNOMED CT**, the **Primary Care EHR FHIR server**, and **HL7 v2 message generation**. Coding tasks were split across two developers; documentation and website were owned by one dedicated member.

## Detailed Team Contributions Summary

| Team Member             | Role | Primary Tasks | Technical Contributions | Key Deliverables | Skills / Learning Outcomes |
|-------------------------|------|---------------|-------------------------|------------------|----------------------------|
| **Zhenan Yin**          | ETL Lead & Team Coordinator | Task 1, Task 2, Task 3, GitHub Repository Setup, Team Coordination | Developed ETL workflows for Patient, Parent Condition, Child Condition, and BP Observation resources. Integrated OpenEMR with Primary Care FHIR server and coordinated repository workflows. | Patient resource, Parent Condition resource, Child Condition resource, BP Observation resource, GitHub project repository, coordinated final project integration. | Learned hands-on FHIR API development, ETL workflow orchestration, healthcare interoperability standards, and leadership in collaborative technical projects. |
| **Aiswarya Perumbilly** | Procedure & Website Lead | Task 4, Website Design, Content Writing, UI Development | Developed Procedure workflow and designed the full GitHub Pages project website. Created layouts, navigation, visuals, tables, and technical web content. | Procedure resource, complete project website, website styling, page layouts, project summaries, technical explanations, final presentation-ready web content. | Improved healthcare website development, technical communication, project presentation skills, and translating complex workflows into simple user-friendly content. |
| **Kelli Davis**         | HL7 & Documentation Lead | Task 5, Documentation, Testing, Validation Support, Mapping | Developed HL7 v2 ADT workflow and assisted SNOMED CT to ICD-10 terminology mapping. Supported documentation, testing, validation review, and final quality assurance. | HL7 v2 ADT message file, project documentation, terminology mapping support, testing reports, validation review, quality assurance support. | Learned HL7 interoperability standards, healthcare documentation practices, terminology mapping workflows, and software quality assurance methods. |

---

## Shared Team Contributions

<div class="shared-grid">
  <div class="shared-card">
    <h4>Project Planning</h4>
    <p>All members jointly discussed project scope, divided tasks equally, and tracked deadlines.</p>
  </div>
  <div class="shared-card">
    <h4>Code Review</h4>
    <p>The website author reviewed all five scripts to ensure documentation accurately matches the implementation - catching inconsistencies before publishing.</p>
  </div>
  <div class="shared-card">
    <h4>Presentation</h4>
    <p>Any two members present directly from the GitHub Pages website, walking through the pipeline live with a demonstration of all five tasks.</p>
  </div>
  <div class="shared-card">
    <h4>Debugging</h4>
    <p>Pipeline issues - expired tokens, missing profile fields, Hermes response variations, dataAbsentReason edge cases - were discussed and resolved as a group.</p>
  </div>
</div>

---

## Collective Lessons Learned

<div class="lessons-grid">
  <div class="lesson-section">
    <h4>Technical Skills</h4>
    <ul>
      <li>FHIR R4 resource structure and REST API interactions</li>
      <li>SNOMED CT IS-A hierarchy and ECL child search operators</li>
      <li>OAuth2 Bearer Token authentication and secure credential management</li>
      <li>Python ETL pipeline design with defensive fallback logic</li>
      <li>HL7 v2.5 segment structure and FHIR→HL7 field mapping</li>
      <li>FHIR profile validation with custom <code>StructureDefinition</code> profiles</li>
      <li>GitHub Pages + Jekyll website deployment with <code>_config.yml</code></li>
    </ul>
  </div>
  <div class="lesson-section">
    <h4>Collaboration Skills</h4>
    <ul>
      <li>Clear task ownership prevents blockers and duplicated effort</li>
      <li>Documentation written <em>alongside</em> code is more accurate than writing it after</li>
      <li>Real data always has edge cases that synthetic test data misses</li>
      <li>Descriptive Git commit messages help teammates track progress without asking</li>
      <li>Regular check-ins between coding members keeps integration smooth</li>
    </ul>
  </div>
</div>

---
