# Astro_Team4

## Biomarker-Driven Therapeutic Evaluation for Long-Duration Spaceflight

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


-  Bone Density Loss

-  Muscle Atrophy
  
-  Neurobiological Degeneration


Terrestrial solutions to these risks include drug therapeutics that require clinical trials for safety and efficacy to be approved for human use. Evaluating potential drug therapeutics during long-term space travel for these risks will be challenging due to the lack of clinical trials in these extreme environments. Our tool targets future drug discovery validation in space missions that tackle issues of bone density loss, muscle atrophy, and neurodegeneration.

In traditional clinical development:

- **Phase I Clinical Trials** primarily evaluate drug safety, tolerability, and adverse physiological effects.
- **Phase II Clinical Trials** primarily evaluate therapeutic efficacy and biological effectiveness.

However, evaluating potential therapeutics during long-duration spaceflight presents major challenges due to the lack of validated clinical trial frameworks in microgravity and radiation-exposed environments.

---

## Clinical Motivation 

There are no validated frameworks for assessing drug safety and efficacy in microgravity environments, leaving astronauts on long-duration missions without evidence-based therapeutic options for progressive bone loss, muscle atrophy, and neurodegeneration.


**Approach**

We plan to create a dashboard that displays different biomarker concentrations that are taken from the samples measured throughout the mission duration. These biomarkers would test both the safety and efficacy of potential therapeutics used to treat the three identified risks of bone density loss, muscle atrophy, and neurobiological degeneration.
Using the current dataset, we will author a tool that displays a dashboard of each of the three risks, along with important details of biomarker concentrations and the level of severity for safety.

**Expected Output**

There will be three categories for the outputs, each targeting the three aforementioned risks related to bones, muscles, and the brain.

Within each category are two types of graphics:

Safety graphics will calculate the current risk of each subject based on normal biomarker indications.
Efficacy graphics will show quantitative results of biomarkers indicative of effective or ineffective treatments.

---

## Prototype Visuals

The dashboard prototype visualizes astronaut health risks using biomarker-based safety, efficacy, and resilience scoring. These visuals are intended to demonstrate how mission biomarker data could support future therapeutic monitoring during long-duration spaceflight.

<img width="1895" height="519" alt="image" src="https://github.com/user-attachments/assets/4e30a35f-527e-4da5-b5c1-0f6d451522ed" />

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

---

## Accessing the Dashboard

There are 3 ways to access or run the Astro_team4 Streamlit dashboard

**Option 1**

Use this option if you want to download the project and run the dashboard on your own computer.

1. Clone the Github repository: git clone https://github.com/munozsan03/Astro_Team4.git
2. Move into the project folder: cd Astro_Team4

**Option 2**

Use this option if the dashboard is deployed online.

Dashboard link
QR Code

**Option 3**

Use this option if you already have the project folder on your computer and only need to install Streamlit and run the app.

1. Install Streamlit using Python
2. Move into the project folder: cd Astro_Team4
3. Run the dashboard: python -m streamlit run streamlit_app/app.py
4. After running the command, Streamlit will show a local URL such as: http://localhost:8501


