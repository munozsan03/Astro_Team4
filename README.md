# TrinityRx - Team 4
<img width="2000" height="500" alt="TrinityRx Logo" src="https://github.com/user-attachments/assets/88bed5d6-4a0f-4755-a999-70bacd940e78" />

## Biomarker-Driven Therapeutic Evaluation Dashboard for Long-Duration Spaceflight

Teammates:
Santiago Munoz, Vy Tran, Giovanni Victorio

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Hackathon](https://img.shields.io/badge/Torchlight-Hackathon-orange)

## Problem Background:

Long-term human spaceflight can expose astronauts to extreme conditions such as microgravity, radiation, and confined environments which can disrupt multiple biological systems. 

<p align="center">
  <img src="https://cdn.mos.cms.futurecdn.net/UnAJpoG9pf5UHEHx8xdGsS-1920-80.jpg.webp" width="700">
</p>


These disruptions can lead to increased risk of:


-  Bone Density Loss, [Seen from this Nature Journal article](https://www.nature.com/articles/s41526-023-00256-5)

-  Muscle Atrophy, [Seen from this Cells Journal article](https://www.mdpi.com/2073-4409/13/24/2120)
  
-  Neurobiological Degeneration, [Seen from this Nature Journal article](https://www.nature.com/articles/s41598-021-88938-6)


Terrestrial solutions to these risks include drug therapeutics that require clinical trials for safety and efficacy to be approved for human use. Evaluating therapeutic performance during long-duration spaceflight remains challenging due to the absence of validated clinical frameworks in microgravity environments.

---

## Clinical Motivation 


Traditional clinical development relies on phased therapeutic evaluation frameworks to assess both safety and efficacy before approval for human use.

- **Phase I Clinical Trials** primarily evaluate physiological safety, toxicity, tolerability, and adverse biological responses.
- **Phase II Clinical Trials** focus on therapeutic efficacy and measurable biological improvement within targeted disease pathways.

However, these validation pipelines have not been adapted for long-duration human spaceflight environments.

Microgravity-associated physiological adaptation may alter biomarker trajectories, inflammatory signaling, musculoskeletal remodeling, neurobiological function, and systemic therapeutic response in ways that differ substantially from terrestrial clinical populations.

This creates a major translational gap for future astronaut healthcare and therapeutic deployment during deep-space missions.

---

## Hackathon Track

This project primarily aligns with **Track 2: Individualized Risk Profiling**, while also incorporating core principles from **Track 3: Communication & Visualization**.

Our platform combines biomarker-driven physiological risk assessment with clinically interpretable visualization tools designed to support transparent and astronaut-readable therapeutic evaluation.

--- 


## Approach 


Our prototype integrates biomarker-driven safety, efficacy, and resilience analysis into a unified visualization platform for long-duration spaceflight applications.

Using longitudinal astronaut multi-omics datasets, the dashboard evaluates physiological changes associated with musculoskeletal degeneration, cardiovascular stress, immune dysregulation, and neurobiological adaptation throughout mission duration.

The framework is organized into three primary analytical categories:

| Category | Objective |
|---|---|
| **Safety Monitoring** | Evaluates biomarkers associated with adverse physiological responses and potential therapeutic toxicity |
| **Efficacy Analysis** | Evaluates biomarkers associated with therapeutic effectiveness and preservation of physiological function |
| **Resilience Modeling** | Evaluates adaptive response, recovery trajectory, and inter-crew physiological variability based on biomarker comparisons |

The current prototype focuses on representative modules for bone density loss prevention, cardiotoxicity safety monitoring, and neurobiological resilience analysis while establishing a scalable framework for future biomarker integration.

---

## Prototype Visuals

The dashboard prototype visualizes astronaut health risks using biomarker-based safety, efficacy, and resilience scoring. These visuals are intended to demonstrate how mission biomarker data could support future therapeutic monitoring during long-duration spaceflight.

<table align="center" cellspacing="20">
<tr>

<td align="center">
<img src="https://github.com/user-attachments/assets/c0bf30dd-9afa-4a03-affb-c15126971507" width="280"><br>
<em>Bone Density Loss Prevention</em>
</td>

<td align="center">
<img src="https://github.com/user-attachments/assets/65c401e4-0749-4c12-83db-366393623a68" width="280"><br>
<em>Cardiotoxicity Safety</em>
</td>

<td align="center">
<img src="https://github.com/user-attachments/assets/ebc17d9c-d145-4cd4-97be-951a09f2475a" width="280"><br>
<em>Neurobiological Resilience</em>
</td>

</tr>
</table>


---

## Current Prototype Biomarker Panel

The current prototype focuses on three representative modules: one efficacy module, one safety module, and one resilience module.


| Module | Category | Tests / Samples | Key Biomarkers |
|--------|----------|-----------------|----------------|
| **Bone Density Loss Prevention** | Efficacy | Blood Serum CMP, Plasma Proteomics, Urine Inflammation Panel, Plasma Metabolomics | BGLAP, SPARC, SPP1, SOST, Calcium, Alkaline Phosphatase, RANK, RANKL, BMP7, WNT16, FGF23, Ergocalciferol, Cortisol |
| **Cardiotoxicity** | Safety | Cardiac Cytokine Array, Plasma Proteomics | CRP, Fibrinogen, Haptoglobin, Alpha-2-Macroglobulin, PF4, L-Selectin, Fetuin-A, SAP, VWF, SERPINE1 |
| **Neurobiological Resilience** | Resilience | Plasma Proteomics, Urine Inflammation Panel, Plasma Metabolomics | BDNF, GFAP, S100B, NRGN, CLU, APOE, NGF, CXCL10, Kynurenine:Tryptophan Ratio, 5-HIAA, N-Acetylaspartic Acid, Cortisol |

---


## Full Biomarker Framework

The table below represents the idealized full biomarker panel for future expansion of the prototype. It includes additional safety, efficacy, and resilience categories that could be incorporated as more datasets and validation methods become available.

<details>
<summary><strong>View Full Biomarker Framework</strong></summary>


| Risk | Category | Tests / Samples | Measured Biomarkers |
|------|----------|-----------------|---------------------|
| **Neurodegeneration** | Efficacy | Plasma Proteomics, Urine Inflammation Panel, Plasma Metabolomics, EVP Proteomics | **Proteomics:** BDNF, APP, SNCA, CLU, APOE, S100B, VGF, NRGN, L1CAM, CNTN1, IGF1, MDK, CHGB, SCG5, PRNP · **Urine Panel:** BDNF, GFAP, NGF, MIF, IL-6, TNF, IFN-γ, CXCL10, TGF-β1/3, VSNL1 · **Metabolomics:** Kynurenine, Tryptophan, Kynurenic Acid, Xanthurenic Acid, N-Acetylaspartic Acid, 5-HIAA, Homovanillic Acid, Cortisol, Nicotinamide |
| **Muscle Atrophy** | Efficacy | Blood Serum (CMP), Plasma Proteomics, EVP Proteomics, Plasma Metabolomics, Urine Inflammation Panel | **Proteomics:** FST, PYGM, PYGB, ENO3, MYH9/10/11/14, MYL1/3/4/6/9, ACTA1, ACTB, IGF1, NAMPT, MB · **CMP:** Creatinine, BUN:Creatinine Ratio, Albumin · **Metabolomics:** 3-Methylhistidine, Creatine, Creatinine, Leucine, Isoleucine, Valine, Glutamine, Carnitine, Acetylcarnitine, Taurine · **Urine Panel:** IL-6, TGF-β1/3, OSM, LIF, VEGFA, MMP9, TIMP1, TIMP2 |
| **Bone Density Loss** | Efficacy | Blood Serum (CMP), Plasma Proteomics, Urine Inflammation Panel, Plasma Metabolomics, Stool Metagenomics | **Proteomics:** BGLAP, SPARC, SPP1, SOST, POSTN, BGN, DCN, LUM, OGN, MGP, COL1A1/1A2, COMP, CILP/CILP2, FBN1/2, SFRP2/4, ADIPOQ · **CMP:** Calcium, Alkaline Phosphatase · **Urine Panel:** TNFRSF11A (RANK), TNFSF11 (RANKL), BMP7, BMP10, WNT16, WNT7A, GDF2, FGF23, SPP1, IL-6, IL-17A, IL-1β, TGF-β1 · **Metabolomics:** Ergocalciferol (Vit D2), Cortisol, Corticosterone, Proline, Glycine, Lysine, Arginine, Citric Acid |
| **Hepatotoxicity** | Safety | CMP Panel | ALT, AST, ALP, Total Bilirubin, Albumin |
| **Nephrotoxicity** | Safety | CMP Panel | BUN (urea nitrogen), Creatinine, eGFR (African American + non-African American), BUN:Creatinine Ratio |
| **Electrolyte / Metabolic Safety** | Safety | CMP Panel | Glucose, Sodium, Potassium, CO₂ (bicarbonate proxy), Chloride, Calcium, Total Protein, Albumin:Globulin Ratio |
| **Cardiotoxicity** | Safety | Cardiac Cytokine Array (Eve), Plasma Proteomics | **Cardiac Array:** CRP, Fibrinogen, Haptoglobin, Alpha-2-Macroglobulin, AGP, PF4, L-Selectin, Fetuin-A, SAP · **Proteomics:** VWF, SERPINE1 (PAI-1), PF4 |
| **Immunotoxicity / Cytokine Storm** | Safety | Urine Inflammation Panel, Immune Cytokine Arrays (Eve + Alamar) | **Urine Panel:** IL-6, IL-8 (CXCL8), IL-10, TNF-α, IFN-γ, IL-1β, IL-17A, IL-12, IL-4, IL-5, IL-13, IL-23, IL-27 · **Immune Arrays:** IFN-α2, IFN-γ, IL-10, IL-12p40/p70, IL-13, IL-15, IL-16, IL-17A, G-CSF, GM-CSF, Eotaxin, Fractalkine, GROα, Activin A/B, 40+ additional cytokines/chemokines |
| **Hematotoxicity** | Safety | CBC (Quest Diagnostics) | WBC Count, RBC Count, Hemoglobin, Hematocrit, MCV, MCH, MCHC, RDW, Platelet Count, MPV, Absolute Neutrophils, Absolute Lymphocytes, Absolute Monocytes, Absolute Eosinophils, Absolute Basophils, Neutrophil %, Lymphocyte %, Monocyte %, Eosinophil %, Basophil %, Neutrophil:Lymphocyte Ratio (derivable) |
| **Adaptive Immune Safety** | Safety | PBMC VDJ Profiles, snRNA-seq, snATAC-seq | T/B Cell Clonal Diversity and Expansion (VDJ), PBMC Cell-type Transcriptomes by Cell Type (snRNA-seq), Chromatin Accessibility at Immune Loci (snATAC-seq) |
| **Oxidative Stress** | Safety | Plasma Metabolomics | Cysteineglutathione Disulfide, Malondialdehyde, Ascorbic Acid (Vit C), Dehydroascorbic Acid, Lipoic Acid, Ergothioneine |
| **Coagulation** | Safety | Cardiac Cytokine Array (Eve), Plasma Proteomics, EVP Proteomics | Fibrinogen, VWF, SERPINE1 (PAI-1), PF4, F2, F5, F8, F9, F11, F12, F13A1, PROS1, SERPINC1 (antithrombin III), KLKB1, SERPIND1 (heparin cofactor II) |
| **Acute Phase / Complement** | Safety | Cardiac Cytokine Array (Eve), Plasma Proteomics, EVP Proteomics | **Acute Phase:** CRP, Haptoglobin, Alpha-2-Macroglobulin, AGP, SAA1, SAA2, SAA2-SAA4, LBP, Fetuin-A · **Complement:** C1QA, C1QB, C1QC, C1R, C1S, C2, C3, C4A, C4B, C5, C6, C7, C8A/B/G, C9, CFH, CFI, CFP, SERPING1 |
| **Physiological Resilience** | Resilience | Blood Serum (CMP), CBC, Plasma Proteomics, Plasma Metabolomics, Urine Inflammation Panel | **Cross-crew comparison of magnitude and trajectory of change relative to crew mean — Proteomics:** IGF1, Albumin · **CMP:** Creatinine, Albumin, Calcium · **CBC:** Hemoglobin, Hematocrit, Neutrophil:Lymphocyte Ratio · **Metabolomics:** Cortisol, Carnitine, Glutamine, Leucine, Isoleucine, Valine · **Urine Panel:** IL-6, TGF-β1 |
| **Immune Resilience** | Resilience | Immune Cytokine Arrays (Eve + Alamar), Urine Inflammation Panel, PBMC VDJ Profiles, snRNA-seq | **Cross-crew comparison of immune homeostasis vs. dysregulation across timepoints — Cytokine Arrays:** IL-6, IL-10, IFN-γ, TNF-α, IL-17A, IL-4, IL-13 · **VDJ:** T/B cell clonal diversity index per astronaut · **snRNA-seq:** CD4:CD8 ratio, NK cell proportion, regulatory T cell frequency |
| **Neurological Resilience** | Resilience | Plasma Proteomics, Urine Inflammation Panel, Plasma Metabolomics | **Cross-crew comparison of neuro-inflammatory shift and recovery trajectory — Proteomics:** BDNF, GFAP, S100B, NRGN, CLU, APOE · **Urine Panel:** BDNF, GFAP, NGF, CXCL10 · **Metabolomics:** Kynurenine:Tryptophan Ratio, 5-HIAA, N-Acetylaspartic Acid, Cortisol, Nicotinamide |
| **Microbiome Resilience** | Resilience | Stool Metagenomics, Skin Metagenomics | **Cross-crew comparison of diversity loss and post-flight recovery rate — Taxonomy:** Alpha diversity (Shannon index), Firmicutes:Bacteroidetes ratio, Lactobacillaceae abundance · **Functional (KEGG):** Butyrate synthesis pathway CPM, short-chain fatty acid biosynthesis · **Beta diversity:** Bray-Curtis dissimilarity from each astronaut's own preflight baseline |
| **Musculoskeletal Resilience** | Resilience | Blood Serum (CMP), Plasma Proteomics, EVP Proteomics, Plasma Metabolomics | **Cross-crew comparison of muscle and bone marker trajectories — Proteomics:** FST, IGF1, NAMPT, BGLAP, SOST, SPP1, COL1A1/1A2, COMP · **CMP:** Creatinine, BUN:Creatinine Ratio, Calcium, Alkaline Phosphatase · **Metabolomics:** 3-Methylhistidine, Creatine, BCAAs (Leu/Ile/Val), Ergocalciferol (Vit D2), Cortisol |
</details>

---

## Accessing the Dashboard

There are 2 ways to access or run the Astro_team4 Streamlit dashboard

**Option 1 - Run Locally**


1. Clone the Github repository: git clone https://github.com/munozsan03/Astro_Team4.git, or download and extract ZIP file
2. Using Command Prompt or Terminal, move into the project folder: cd ~/Astro_Team4
3. Install Streamlit using Python: python -m pip install streamlit
4. Make sure you are in the directory that contains streamlit_app/
5. Run the Streamlit dashboard: python -m streamlit run streamlit_app/app.py

**Option 2 - Hosted Streamlit Deployment**

Dashboard link: https://astroteam4-jsxtx6fdranyr5uv6rdzcn.streamlit.app/

Try the QR-code With Your Phone! 
<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/1f629432-6134-4b37-b324-f4e95cd25a61" />

---


## Additional Documentation

Expanded biomarker rationale, physiological interpretation, scoring methodology, and supporting literature references are available in the supplementary markdown documentation files included within this repository.

These documents provide additional detail regarding biomarker selection methodology, translational significance, and analytical framework development for safety, efficacy, and resilience modeling during long-duration spaceflight.

Please refer to:

- `2. Bone Density Loss Prevention Efficacy Biomarker Justifications.md`
- `3. Bone Density Loss Prevention Efficacy Scoring Methodology.md`
- `4. Cardiotoxicity Safety Biomarker Justifications.md`
- `5. Cardiotoxicity Safety Scoring Methodology.md`
- `6. Neurobiological Resilience Biomarker Justifications.md`
- `7. Neurobiological Resilience Scoring Methodology.md`


AI-assisted development tools were used for selected documentation, debugging, and interface refinement tasks during development. 

<details>
<summary><strong>Use of AI</strong></summary>

<br>
# 🚀 Use of AI In Astronaut Omics Therapeutic Testing

## Background

Historically, drug discovery has been an **extremely slow, expensive, and high-risk process**. Developing even a single therapeutic often requires years of receptor identification, laboratory testing, large clinical studies, and the evaluation of thousands of molecular candidates before identifying one that is both effective and safe.

As previously mentioned, the complex environments in long-term spaceflight make this challenge even greater due to the **unique physiological changes** that cannot be traditionally accounted for.

---

## AI-Accelerated Drug Discovery

Very recent advances in **artificial intelligence and machine learning** have significantly accelerated this process. Many scientists who study both biochemistry and computer science have integrated large databases of existing proteins and small molecules into contemporary algorithms that can accelerate the drug discovery process by years.

In research papers and labs, a common workflow has been identified:

1. Identify a **G Protein-Coupled Receptor (GPCR)** responsible for the effects to mitigate
2. Use AI to **generate a peptide backbone** to inhibit the receptor
3. Use AI to **generate an amino acid sequence** that will fold into that peptide backbone
4. Use AI to **verify** that the amino acid sequence will actually fold into that structure

---

## Our Workflow — University of Houston

Below is the workflow our labs at the University of Houston adopt, which we plan to utilize to target the inhibition of **bone density loss**, **muscle atrophy**, and **neurodegeneration**.

While this is an example of Giovanni Victorio's work on the Cannabinoid Receptor Type 1, some aspects were changed to avoid revealing intellectual property.

| Tool | Input | Input Example | Output | Output Example |
|------|-------|--------|--------|--------|
| [**RFdiffusion**](https://github.com/RosettaCommons/RFdiffusion) | **G Protein-Coupled Receptor** *(3D Structure, .PDB file)* | <img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/94086785-a47b-49f3-b904-81ad94000ae1" /> | **Generated Peptide Backbone to Antagonize** *(3D Structure, .PDB file)* | <img width="483" height="497" alt="CB1 Peptide" src="https://github.com/user-attachments/assets/e0d1d308-bd18-4364-b428-fd07777b73c6" /> |
| [**LigandMPNN**](https://github.com/dauparas/LigandMPNN) | **Peptide Backbone** *(3D Structure, .PDB file)* | <img width="483" height="497" alt="CB1 Peptide" src="https://github.com/user-attachments/assets/03ca1daf-d626-4a13-bec8-04c815964e85" /> | **Amino Acid Sequence** *(Text)* | CYFVLWKC |
| [**AlphaFold**](https://github.com/google-deepmind/alphafold3) | **Amino Acid Sequence** *(Text)* | CYFVLWKC | **Validated Structure Based on Worldwide Protein Structure Databases** *(3D Structure, .CIF and .PDB file)* | <img width="854" height="746" alt="image" src="https://github.com/user-attachments/assets/e616da72-489b-49d6-b638-7b1c145fa9db" /> | 

By utilizing our existing AI drug discovery pipeline for peptides, we can either **agonize** receptors to encourage growth of bones, muscle, and brain matter, or **antagonize** the loss of bones, muscle, and brain matter.

---

## Anticipated GPCR Targets

### ✅ Targets to Agonize (Activate)

| Condition | GPCR Target | Justification | Structure | RCSB ID |
|-----------|-------------|-------------|-------------|-------------|
| Bone Density Loss | Parathyroid Hormone 1 Receptor | Activation of PTH1R stimulates osteoblast activity and promotes new bone formation. | <img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/b3a3d717-b5cc-4ade-94fb-2c11e65f569b" /> | 6FJ3 |
| Muscle Atrophy | Ghrelin Receptor | Activation increases growth hormone signaling, improves protein synthesis, and may support muscle maintenance. | <img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/c225a6ab-1131-4a07-8298-71d821f81b62" /> | 7W2Z |
| Neurodegeneration | Glucagon-Like Peptide-1 Receptor | GLP-1R activation has demonstrated neuroprotective effects, including reduced inflammation and improved neuronal survival. | <img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/89ce8f75-9357-4f82-92d2-2b701d56cf57" /> | 3C59 |


### 🚫 Targets to Antagonize (Inhibit)

| Condition | GPCR Target | Justification | Structure | RCSB ID |
|-----------|-------------|-------------|-------------|-------------|
| Bone Density Loss | Cannabinoid Receptor Type 1 | Excess CB1 signaling has been linked to increased bone resorption and reduced bone formation. | <img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/503aac1a-90f7-479e-94cf-5ea5be57ca5c" /> | 6N4B |
| Muscle Atrophy | Angiotensin II Type 1 Receptor | Chronic AT1R signaling contributes to oxidative stress, inflammation, and muscle catabolism.  | <img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/2d89158f-8231-45a5-84a8-6c5bdce34a55" /> | 4ZUD |
| Neurodegeneration | Adenosine A2A Receptor | Excess A2AR signaling is associated with neuroinflammatory and neurodegenerative pathways. | <img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/5ff3f421-babe-415a-ae5a-3757a3b0bb4f" /> | 5N2R |

---

# 🧬 Integration With Astronaut Omics Validation

## Why Omics Validation Is Necessary

Although AI-driven peptide therapeutics can now be designed computationally at unprecedented speeds, one of the largest challenges in space medicine remains the inability to perform traditional long-term clinical trials in microgravity environments.

Physiological responses in space differ substantially from Earth due to:

- Microgravity-induced musculoskeletal unloading
- Elevated radiation exposure
- Altered immune signaling
- Fluid redistribution
- Chronic stress and circadian disruption
- Confinement-related metabolic changes

As a result, therapeutics that appear effective on Earth may behave differently during long-duration missions.

Because large-scale pharmaceutical trials cannot realistically be conducted aboard spacecraft or lunar habitats, astronaut **multi-omics data** becomes one of the most valuable tools for validating therapeutic performance.

---

## Our Proposed Validation Framework

Our project combines:

1. **AI-guided Therapeutics***
2. **Astronaut Omics Datasets**
3. **Biomarker-based Efficacy, Safety, and Resilience Scoring**

into a unified precision medicine pipeline for long-term human spaceflight.

*In AI-guided drug discovery, in-vitro and in-vivo studies are still conducted to gather enough data before pursuing clinical trials.

Rather than waiting years for conventional clinical endpoints, astronaut biological data can provide continuous molecular feedback regarding whether a therapeutic is:

- Producing the intended biological response
- Causing unintended toxicity
- Maintaining astronaut physiological resilience

---

# 🚀 Use of AI In Streamlit App Creation

Besides the aforementioned AI programs for drug discovery, we also utilized Claude to create proof-of-concept visuals to guide our dashboard creation.

**Example Proof-of-Concept Visual**

<img width="1108" height="919" alt="image" src="https://github.com/user-attachments/assets/9d6c25a4-68e6-4a78-89bb-8b2b72ab7dfc" />

In addition to these visuals, Claude and ChatGPT were used for translating our scoring methodologies into coded modules, debugging various errors, and user interface refinement tasks like identifying where font changes were being made. Our final codebase and documents were also reformatted to the discretion of these AI programs while we did our best to mitigate any loss of our own diction.

</details>

