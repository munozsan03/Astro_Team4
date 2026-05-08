import streamlit as st
import pandas as pd
import numpy as np
import os

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="Torchlight Health Dashboard", layout="wide")


# ============================================================
# DATA LOADING
# ============================================================
# Build a path to the processed data directory, relative to this file's location.
# Expected files (all CSVs):
#   - plasma_proteomics.csv         → columns: Gene, logFC (+ others)
#   - plasma_metabolomics.csv       → columns: ID, logFC (+ others)
#   - cmp_metabolic_panel.csv       → row-indexed by metric name; columns like C001_T_L1, C001_T_R1, ...
#   - cardiac_cytokines_eve.csv     → same row/column layout as CMP
#   - urine_inflammation_panel.csv  → columns: crew_id, timepoint, + marker columns
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

@st.cache_data
def load_data():
    """Load all five processed data files and return as DataFrames."""
    pp   = pd.read_csv(os.path.join(DATA_DIR, "plasma_proteomics.csv"))
    met  = pd.read_csv(os.path.join(DATA_DIR, "plasma_metabolomics.csv"))
    cmp  = pd.read_csv(os.path.join(DATA_DIR, "cmp_metabolic_panel.csv"))
    card = pd.read_csv(os.path.join(DATA_DIR, "cardiac_cytokines_eve.csv"))
    urine= pd.read_csv(os.path.join(DATA_DIR, "urine_inflammation_panel.csv"))
    return pp, met, cmp, card, urine

# Attempt data load; flag failure so the app degrades gracefully instead of crashing.
try:
    pp, met, cmp, card, urine = load_data()
    DATA_LOADED = True
except Exception as e:
    DATA_LOADED = False
    DATA_ERROR = str(e)


# ============================================================
# HELPER FUNCTIONS
# These are shared utilities called by all three score modules.
# ============================================================

def get_logfc(pp_df, gene):
    """
    Look up the log-fold-change (logFC) for a single gene in the plasma proteomics table.

    Args:
        pp_df (DataFrame): Plasma proteomics data. Must have 'Gene' and 'logFC' columns.
        gene (str): Gene symbol to look up (case-insensitive).

    Returns:
        float | None: The logFC value, or None if the gene isn't found.
    """
    row = pp_df[pp_df['Gene'].str.upper() == gene.upper()]
    if row.empty:
        return None
    return float(row['logFC'].values[0])


def get_cmp_per_crew(cmp_df, metric_row_name, crew_id):
    """
    Retrieve all time-point values for a single CMP metric for one crew member.

    The CMP CSV uses row-indexed metrics (first column = metric name) and
    column names formatted as: {crew_id}_{session}_{timepoint}  e.g. C001_T_L1

    Args:
        cmp_df (DataFrame): CMP metabolic panel data.
        metric_row_name (str): Exact string in the first ('Unnamed: 0') column.
        crew_id (str): Crew member ID, e.g. 'C001'.

    Returns:
        dict: { timepoint_str: float_or_None }
              Timepoints prefixed with 'L' = pre-flight/launch phase.
              Timepoints prefixed with 'R' = post-flight/return phase.
    """
    row = cmp_df[cmp_df['Unnamed: 0'] == metric_row_name]
    if row.empty:
        return {}
    # Filter to columns that belong to this crew member
    cols = [c for c in cmp_df.columns if c.startswith(crew_id + '_')]
    result = {}
    for col in cols:
        tp = col.split('_')[2]   # Extract timepoint token (e.g. 'L1', 'R2')
        val = row[col].values[0]
        result[tp] = float(val) if not pd.isna(val) else None
    return result


def get_cardiac_per_crew(card_df, metric_row_name, crew_id):
    """
    Retrieve all time-point values for a single cardiac cytokine marker for one crew member.

    Identical column layout to CMP: {crew_id}_{session}_{timepoint}.

    Args:
        card_df (DataFrame): Cardiac cytokines (Eve) data.
        metric_row_name (str): Row label in the first column.
        crew_id (str): Crew member ID.

    Returns:
        dict: { timepoint_str: float_or_None }
    """
    row = card_df[card_df['Unnamed: 0'] == metric_row_name]
    if row.empty:
        return {}
    cols = [c for c in card_df.columns if c.startswith(crew_id + '_')]
    result = {}
    for col in cols:
        tp = col.split('_')[2]
        val = row[col].values[0]
        result[tp] = float(val) if not pd.isna(val) else None
    return result


def get_urine_per_crew(urine_df, col_name, crew_id):
    """
    Retrieve all time-point values for a single urine marker for one crew member.

    The urine CSV is in 'long' format: one row per (crew_id, timepoint) combination.

    Args:
        urine_df (DataFrame): Urine inflammation panel data.
                              Must have 'crew_id' and 'timepoint' columns.
        col_name (str): Column name for the desired marker.
        crew_id (str): Crew member ID.

    Returns:
        dict: { timepoint_str: float_or_None }
    """
    crew_rows = urine_df[urine_df['crew_id'] == crew_id]
    result = {}
    for _, r in crew_rows.iterrows():
        tp = r['timepoint']
        val = r.get(col_name, None)
        result[tp] = float(val) if val is not None and not pd.isna(val) else None
    return result


def get_met_logfc(met_df, name):
    """
    Look up the logFC for a metabolite in the plasma metabolomics table.
    First tries an exact (case-insensitive) match on the 'ID' column;
    falls back to a partial/contains match if nothing is found.

    Args:
        met_df (DataFrame): Plasma metabolomics data. Must have 'ID' and 'logFC' columns.
        name (str): Metabolite name or partial name.

    Returns:
        float | None: The logFC value, or None if not found.
    """
    row = met_df[met_df['ID'].str.lower() == name.lower()]
    if row.empty:
        # Attempt partial string match as a fallback
        row = met_df[met_df['ID'].str.lower().str.contains(name.lower(), na=False)]
    if row.empty:
        return None
    return float(row['logFC'].values[0])


# ============================================================
# SCORE COMPUTATION — SHARED CONVENTIONS
#
# Two data formats feed into scores:
#
#   1. logFC data (proteomics & metabolomics):
#      - Represents flight vs. pre-flight fold change on a log2 scale.
#      - Positive  = upregulated during flight.
#      - Negative  = downregulated during flight.
#      - Used as-is; no per-crew variability (cohort-level aggregate).
#
#   2. Absolute time-series data (CMP, cardiac cytokines, urine panel):
#      - Raw concentration/value per crew member per timepoint.
#      - Preflight timepoints are labeled starting with 'L' (launch phase).
#      - Postflight timepoints are labeled starting with 'R' (return phase).
#      - Scores derived from postflight/preflight ratios or deviations.
#
# Final scores are clipped to [0, 1] throughout.
# ============================================================


# ============================================================
# MODULE 1 — BONE DENSITY LOSS INHIBITOR EFFICACY
# ============================================================
# PURPOSE: Estimate how effectively the bone-protective intervention is working.
#
# SCORE DIRECTION: Higher score = better efficacy.
#   - Green  (> 0.70): Treatment appears effective.
#   - Yellow (0.40–0.70): Uncertain / moderate signal.
#   - Red    (< 0.40): Weak or counter-productive signal.
#
# ALGORITHM OVERVIEW:
#   1. Pull logFC values for 20 bone-related proteomics markers.
#   2. Compute mean logFC across those markers.
#      - Positive mean → markers trending up → interpreted as beneficial
#        (e.g. bone matrix proteins, Wnt pathway components being upregulated).
#      - Negative mean → markers trending down → possible bone loss signal.
#   3. Map mean logFC to [0.05, 0.95] via:
#        score = 0.5 + clip(mean_logFC / 4.0, -0.45, 0.45)
#      The divisor (4.0) sets the sensitivity — tweak this to widen/narrow the range.
#   4. CMP, urine panel, and metabolomics are collected and displayed for context
#      but do NOT currently feed into the numeric score.
#      → TO ADD THEM: compute post/pre ratios or z-scores and blend into step 3.
# ============================================================

def compute_bone_score(crew_id):
    """
    Compute the Bone Density Loss Inhibitor Efficacy score for a crew member.

    Returns:
        score (float): Efficacy score in [0, 1]. Higher = more effective.
        biomarkers (dict): Structured data for the expander display.
    """
    if not DATA_LOADED:
        return 0.5, {}   # Neutral fallback when data is unavailable

    # ----------------------------------------------------------
    # 1. PROTEOMICS — bone marker panel
    # 20 proteins associated with bone remodeling, matrix maintenance,
    # and Wnt/BMP signaling pathways.
    # logFC = flight vs. pre-flight (positive = upregulated in-flight).
    # ----------------------------------------------------------
    prot_genes = [
        'BGLAP',   # Osteocalcin — bone matrix protein, osteoblast marker
        'SPARC',   # Osteonectin — bone mineralization
        'SPP1',    # Osteopontin — bone resorption / osteoclast activity
        'SOST',    # Sclerostin — inhibits Wnt signaling (downreg = good)
        'POSTN',   # Periostin — bone formation
        'BGN',     # Biglycan — bone matrix proteoglycan
        'DCN',     # Decorin — collagen binding
        'LUM',     # Lumican — ECM regulation
        'OGN',     # Osteoglycin
        'MGP',     # Matrix Gla Protein — mineralization inhibitor
        'COL1A1',  # Collagen I alpha-1 — primary bone matrix collagen
        'COL1A2',  # Collagen I alpha-2
        'COMP',    # Cartilage oligomeric matrix protein
        'CILP',    # Cartilage intermediate layer protein
        'CILP2',
        'FBN1',    # Fibrillin-1 — ECM/connective tissue
        'FBN2',    # Fibrillin-2
        'SFRP2',   # Secreted frizzled-related protein 2 — Wnt modulator
        'SFRP4',   # Secreted frizzled-related protein 4 — Wnt modulator
        'ADIPOQ',  # Adiponectin — bone/fat crosstalk
    ]
    prot_vals = {}
    for g in prot_genes:
        v = get_logfc(pp, g)
        if v is not None:
            prot_vals[g] = round(v, 3)

    # ----------------------------------------------------------
    # 2. CMP — serum chemistry (calcium and alkaline phosphatase)
    # Calcium: low = bone resorption signal.
    # Alk Phos: elevated = osteoblast activity (bone formation or damage).
    # Summarized as preflight avg vs. postflight avg per crew member.
    # NOTE: Not yet integrated into the numeric score.
    # ----------------------------------------------------------
    cmp_vals = {}
    ca = get_cmp_per_crew(cmp, 'calcium_value_milligram_per_deciliter', crew_id)
    ap = get_cmp_per_crew(cmp, 'alkaline_phosphatase_value_units_per_liter', crew_id)

    preflight_tps  = [k for k in ca if k.startswith('L')]
    postflight_tps = [k for k in ca if k.startswith('R')]

    ca_pre  = np.mean([ca[t] for t in preflight_tps  if ca[t] is not None]) if preflight_tps  else None
    ca_post = np.mean([ca[t] for t in postflight_tps if ca[t] is not None]) if postflight_tps else None
    ap_pre  = np.mean([ap[t] for t in preflight_tps  if ap[t] is not None]) if preflight_tps  else None
    ap_post = np.mean([ap[t] for t in postflight_tps if ap[t] is not None]) if postflight_tps else None

    cmp_vals['Calcium (mg/dL)'] = {
        'preflight_avg':  round(ca_pre, 2)  if ca_pre  else None,
        'postflight_avg': round(ca_post, 2) if ca_post else None,
        'all_timepoints': {k: round(v, 2) for k, v in ca.items()},
    }
    cmp_vals['Alkaline Phosphatase (U/L)'] = {
        'preflight_avg':  round(ap_pre, 2)  if ap_pre  else None,
        'postflight_avg': round(ap_post, 2) if ap_post else None,
        'all_timepoints': {k: round(v, 2) for k, v in ap.items()},
    }

    # ----------------------------------------------------------
    # 3. URINE PANEL — cytokines and bone signaling molecules
    # Absolute concentrations (npq units) per timepoint per crew.
    # Covers RANK/RANKL axis, BMPs, Wnts, FGF23, and inflammatory cytokines
    # that influence bone turnover.
    # NOTE: Not yet integrated into the numeric score.
    # ----------------------------------------------------------
    urine_markers = {
        'TNFRSF11A (RANK)':  'tnfrsf11a_concentration_npq',   # Osteoclast differentiation receptor
        'TNFSF11 (RANKL)':   'tnfsf11_concentration_npq',     # RANK ligand — drives osteoclastogenesis
        'BMP7':              'bmp7_concentration_npq',         # Bone morphogenetic protein 7 — osteogenic
        'BMP10':             'bmp10_concentration_npq',
        'WNT16':             'wnt16_concentration_npq',        # Wnt16 — bone formation signal
        'WNT7A':             'wnt7a_concentration_npq',
        'GDF2':              'gdf2_concentration_npq',         # Growth differentiation factor 2
        'FGF23':             'fgf23_concentration_npq',        # Fibroblast growth factor 23 — phosphate/D3 axis
        'SPP1':              'spp1_concentration_npq',         # Osteopontin (urine)
        'IL-6':              'il6_concentration_npq',          # Pro-inflammatory; promotes bone resorption
        'IL-17A':            'il17a_concentration_npq',        # Inflammatory; linked to osteoclast activation
        'IL-1β':             'il1b_concentration_npq',         # Pro-resorptive cytokine
        'TGF-β1':            'tgfb1_concentration_npq',        # Pleiotropic bone regulator
    }
    urine_vals = {}
    for label, col in urine_markers.items():
        tps = get_urine_per_crew(urine, col, crew_id)
        if tps:
            urine_vals[label] = {k: round(v, 2) if v is not None else None for k, v in tps.items()}

    # ----------------------------------------------------------
    # 4. METABOLOMICS — metabolites relevant to bone biology
    # Vitamin D (ergocalciferol) supports calcium absorption.
    # Cortisol/corticosterone at high levels suppress bone formation.
    # Amino acids (proline, glycine, lysine, arginine) are collagen precursors.
    # Citric acid participates in bone mineral metabolism.
    # NOTE: Not yet integrated into the numeric score.
    # ----------------------------------------------------------
    met_targets = [
        'Ergocalciferol (Vit D2)',   # Vitamin D — calcium absorption
        'Cortisol',                  # Glucocorticoid — high = bone loss
        'Corticosterone',            # Rodent/human stress hormone
        'Proline',                   # Collagen precursor amino acid
        'Glycine',                   # Collagen precursor amino acid
        'Lysine',                    # Collagen cross-linking amino acid
        'Arginine',                  # Bone cell signaling amino acid
        'Citric Acid',               # TCA cycle / bone mineralization link
    ]
    met_vals = {}
    for m in met_targets:
        v = get_met_logfc(met, m)
        if v is not None:
            met_vals[m] = round(v, 3)

    # ----------------------------------------------------------
    # 5. SCORE CALCULATION
    #
    # Current formula uses proteomics mean logFC only:
    #   score = 0.5 + clip(mean_logFC / 4.0, -0.45, 0.45)
    #
    # Rationale:
    #   - Positive mean logFC across bone matrix proteins → markers upregulated
    #     in flight → treatment may be preserving/stimulating bone formation.
    #   - The divisor 4.0 means a mean logFC of +4.0 maps to the max score (~0.95).
    #   - Adjust the divisor to change sensitivity to logFC magnitude.
    #
    # To incorporate CMP or urine data, compute a post/pre ratio, normalize it
    # to a [-0.45, 0.45] contribution, and add it to the sum before clipping.
    # ----------------------------------------------------------
    prot_logfcs = list(prot_vals.values())
    mean_logfc  = np.mean(prot_logfcs) if prot_logfcs else 0   # Signed mean (direction matters)

    score = 0.5 + np.clip(mean_logfc / 4.0, -0.45, 0.45)
    score = round(float(score), 3)

    # Package all collected data for the UI expanders
    biomarkers = {
        'Proteomics (logFC flight vs. preflight)': prot_vals,
        'CMP (serum values)':                      cmp_vals,
        'Urine Inflammation Panel (npq)':          urine_vals,
        'Metabolomics (logFC)':                    met_vals,
    }
    return score, biomarkers


# ============================================================
# MODULE 2 — CARDIOTOXICITY SAFETY
# ============================================================
# PURPOSE: Flag cardiac stress and inflammation risk from the intervention.
#
# SCORE DIRECTION: Lower score = safer. (Inverted from bone/neuro!)
#   - Green  (< 0.35): Low cardiac risk.
#   - Yellow (0.35–0.65): Moderate / watch-list.
#   - Red    (> 0.65): Elevated cardiac concern.
#
# ALGORITHM OVERVIEW:
#   1. For each of 9 cardiac cytokine markers, compute the ratio:
#        postflight_mean / preflight_mean
#      Ratio > 1 means the marker rose during/after flight — concerning.
#   2. Average the ratios across all available markers.
#   3. Map to [0.05, 0.95] via:
#        score = clip((mean_ratio - 0.5) / 1.5, 0.05, 0.95)
#      A ratio of 1.0 (no change) maps to ≈0.33 (green zone).
#      A ratio of 2.0 (doubled) maps to ≈1.0 (red zone).
#   4. Add a small PF4 proteomics penalty:
#        score += PF4_logFC * 0.05
#      PF4 upregulation signals platelet activation / thrombosis risk.
#      Coefficient (0.05) can be increased to give PF4 more weight.
# ============================================================

def compute_cardio_score(crew_id):
    """
    Compute the Cardiotoxicity Safety score for a crew member.

    Returns:
        score (float): Risk score in [0, 1]. Lower = safer.
        biomarkers (dict): Structured data for the expander display.
    """
    if not DATA_LOADED:
        return 0.5, {}

    # ----------------------------------------------------------
    # 1. CARDIAC CYTOKINE ARRAY (Eve platform) — per crew, per timepoint
    # These are acute-phase and inflammatory proteins measured in plasma.
    # High post-flight elevation vs. pre-flight baseline signals cardiac stress.
    # ----------------------------------------------------------
    cardiac_markers = {
        'CRP':                 'crp_concentration_picogram_per_milliliter',       # C-reactive protein — systemic inflammation
        'Fibrinogen':          'fibrinogen_concentration_nanogram_per_milliliter', # Clotting / acute phase
        'Haptoglobin':         'haptoglobin_concentration_nanogram_per_milliliter',# Hemolysis marker
        'Alpha-2-Macroglobulin':'a2_macroglobulin_concentration_nanogram_per_milliliter', # Protease inhibitor / acute phase
        'AGP':                 'agp_concentration_nanogram_per_milliliter',        # Alpha-1-acid glycoprotein — inflammation
        'PF4':                 'pf4_concentration_nanogram_per_milliliter',        # Platelet factor 4 — platelet activation
        'L-Selectin':          'l_selectin_concentration_picogram_per_milliliter', # Leukocyte adhesion / endothelial stress
        'Fetuin-A':            'fetuin_a36_concentration_nanogram_per_milliliter', # Vascular calcification inhibitor
        'SAP':                 'sap_concentration_picogram_per_milliliter',        # Serum amyloid P — acute phase
    }
    cardiac_vals    = {}
    score_components = []   # Will hold postflight/preflight ratios for each marker

    for label, row_name in cardiac_markers.items():
        tps = get_cardiac_per_crew(card, row_name, crew_id)
        if tps:
            cardiac_vals[label] = {k: round(v, 1) if v is not None else None for k, v in tps.items()}

            # Split into pre- and post-flight windows
            preflight  = [v for k, v in tps.items() if k.startswith('L') and v is not None]
            postflight = [v for k, v in tps.items() if k.startswith('R') and v is not None]

            if preflight and postflight:
                # Post/pre ratio: >1 means the marker rose after flight (concerning)
                ratio = np.mean(postflight) / np.mean(preflight)
                score_components.append(ratio)

    # ----------------------------------------------------------
    # 2. PROTEOMICS — thrombosis and endothelial damage markers
    # These are flight vs. pre-flight logFC values (cohort level).
    # VWF: von Willebrand factor — endothelial injury / thrombosis
    # SERPINE1 (PAI-1): plasminogen activator inhibitor — clot resolution impaired
    # PF4: platelet factor 4 — platelet activation (also in cytokine array above)
    # ----------------------------------------------------------
    prot_markers = {
        'VWF':              get_logfc(pp, 'VWF'),
        'SERPINE1 (PAI-1)': get_logfc(pp, 'SERPINE1'),
        'PF4':              get_logfc(pp, 'PF4'),
    }
    prot_vals = {k: round(v, 3) for k, v in prot_markers.items() if v is not None}

    # ----------------------------------------------------------
    # 3. SCORE CALCULATION
    #
    # Base score from cardiac cytokine post/pre ratios:
    #   score = clip((mean_ratio - 0.5) / 1.5, 0.05, 0.95)
    #
    # Calibration reference points:
    #   mean_ratio = 0.5  → score ≈ 0.0  (markers dropped — very safe)
    #   mean_ratio = 1.0  → score ≈ 0.33 (no change — healthy baseline)
    #   mean_ratio = 1.5  → score ≈ 0.67 (50% elevation — borderline)
    #   mean_ratio = 2.0  → score ≈ 1.0  (doubled — high risk)
    #
    # PF4 adjustment:
    #   Each unit of PF4 logFC adds 0.05 to the score.
    #   Increase the coefficient (e.g., 0.10) to weight PF4 more heavily.
    #   This can be expanded to include VWF and SERPINE1 similarly.
    # ----------------------------------------------------------
    if score_components:
        mean_ratio = np.mean(score_components)
        score = np.clip((mean_ratio - 0.5) / 1.5, 0.05, 0.95)
    else:
        score = 0.5   # Neutral fallback if no time-series data available

    # Add PF4 proteomics penalty (positive logFC = more platelet activation = more risk)
    pf4_logfc = prot_vals.get('PF4', 0)
    score = np.clip(score + pf4_logfc * 0.05, 0.05, 0.95)
    score = round(float(score), 3)

    biomarkers = {
        'Cardiac Cytokine Array (Eve) — concentration by timepoint': cardiac_vals,
        'Proteomics (logFC flight vs. preflight)':                   prot_vals,
    }
    return score, biomarkers


# ============================================================
# MODULE 3 — NEUROLOGICAL RESILIENCE
# ============================================================
# PURPOSE: Assess the brain's capacity to withstand and recover from
#          space-flight stressors (microgravity, radiation, isolation, CO2).
#
# SCORE DIRECTION: Higher score = more resilient.
#   - Green  (> 0.60): Good neuroprotective signal.
#   - Yellow (0.35–0.60): Mixed or uncertain.
#   - Red    (< 0.35): Concerning neuro-inflammatory signal.
#
# ALGORITHM OVERVIEW:
#   1. BDNF logFC (proteomics): brain-derived neurotrophic factor.
#      Positive = upregulated → neuroprotective → increases score.
#   2. S100B logFC (proteomics): glial/astrocyte injury marker.
#      Positive = upregulated → glial activation/damage → decreases score.
#   3. Kynurenine logFC (metabolomics): tryptophan catabolism byproduct.
#      Elevated kynurenine diverts tryptophan away from serotonin synthesis
#      and can produce neurotoxic quinolinic acid → decreases score.
#
#   Formula:
#     score = 0.5 + (BDNF × 0.08) − (S100B × 0.05) − (Kynurenine × 0.03)
#
#   Coefficients to tune:
#     BDNF    × 0.08 — increase to give neuroprotection more weight
#     S100B   × 0.05 — increase to penalize glial damage more
#     Kynurenine × 0.03 — increase to penalize neuroinflammation more
# ============================================================

def compute_neuro_score(crew_id):
    """
    Compute the Neurological Resilience score for a crew member.

    Returns:
        score (float): Resilience score in [0, 1]. Higher = more resilient.
        biomarkers (dict): Structured data for the expander display.
    """
    if not DATA_LOADED:
        return 0.5, {}

    # ----------------------------------------------------------
    # 1. PROTEOMICS — neurotrophic and injury markers
    # logFC = flight vs. pre-flight.
    # BDNF:  Brain-derived neurotrophic factor — neuroprotection, plasticity
    # S100B: Astrocyte marker — elevated = glial activation or BBB disruption
    # NRGN:  Neurogranin — synaptic marker, elevated = synaptic damage
    # CLU:   Clusterin — neuroprotective chaperone, stress-responsive
    # APOE:  Apolipoprotein E — lipid transport; APOE4 isoform risk for neuro
    # ----------------------------------------------------------
    neuro_genes = ['BDNF', 'S100B', 'NRGN', 'CLU', 'APOE']
    prot_vals = {}
    for g in neuro_genes:
        v = get_logfc(pp, g)
        if v is not None:
            prot_vals[g] = round(v, 3)

    # ----------------------------------------------------------
    # 2. URINE PANEL — neuro-specific markers (per crew, per timepoint)
    # BDNF:   Brain-derived neurotrophic factor (urine proxy)
    # GFAP:   Glial fibrillary acidic protein — astrocyte damage marker
    # NGF:    Nerve growth factor — neuronal survival signal
    # CXCL10: Interferon-γ-induced chemokine — neuroinflammation signal
    # NOTE: Not yet integrated into the numeric score.
    # ----------------------------------------------------------
    urine_neuro = {
        'BDNF':   'bdnf_concentration_npq',
        'GFAP':   'gfap_concentration_npq',
        'NGF':    'ngf_concentration_npq',
        'CXCL10': 'cxcl10_concentration_npq',
    }
    urine_vals = {}
    for label, col in urine_neuro.items():
        tps = get_urine_per_crew(urine, col, crew_id)
        if tps:
            urine_vals[label] = {k: round(v, 2) if v is not None else None for k, v in tps.items()}

    # ----------------------------------------------------------
    # 3. METABOLOMICS — neuro-relevant metabolites
    # Kynurenine:  Tryptophan catabolite — high = serotonin diversion, potential neurotoxicity
    # Tryptophan:  Serotonin precursor — depletion = mood/cognition risk
    # 5-HIAA:      Serotonin metabolite (5-hydroxyindoleacetic acid) — serotonin turnover proxy
    # N-Acetylaspartic Acid: Neuron-specific marker — decline = neuronal loss
    # Cortisol:    Stress hormone — high = hippocampal volume reduction risk
    # Nicotinamide: NAD+ precursor — neuroprotective at sufficient levels
    # ----------------------------------------------------------
    met_neuro = {
        'Kynurenine':                        'Kynurenine',
        'Tryptophan':                        'Tryptophan',
        '5-HIAA (Serotonin Metabolite)':     '5-Hydroxyindoleacetic Acid',
        'N-Acetylaspartic Acid':             'N-Acetylaspartic Acid',
        'Cortisol':                          'Cortisol',
        'Nicotinamide':                      'Nicotinamide',
    }
    met_vals = {}
    for label, name in met_neuro.items():
        v = get_met_logfc(met, name)
        if v is not None:
            met_vals[label] = round(v, 3)

    # Kynurenine:Tryptophan ratio (logFC-based proxy)
    # A rising ratio indicates increased tryptophan diversion toward kynurenine
    # and away from serotonin synthesis — a neuroinflammation signal.
    # NOTE: This ratio uses logFCs, not absolute concentrations, so interpret cautiously.
    kyn = get_met_logfc(met, 'Kynurenine')
    trp = get_met_logfc(met, 'Tryptophan')
    if kyn is not None and trp is not None and trp != 0:
        kyn_trp_ratio = round(kyn / trp, 3)
        met_vals['Kynurenine:Tryptophan Ratio (logFC-based)'] = kyn_trp_ratio

    # ----------------------------------------------------------
    # 4. SCORE CALCULATION
    #
    # Pulls three signals from the data above:
    #   bdnf       — proteomics logFC for BDNF
    #   s100b      — proteomics logFC for S100B
    #   kyn_logfc  — metabolomics logFC for Kynurenine
    #
    # Formula:
    #   score = 0.5 + (BDNF × 0.08) − (S100B × 0.05) − (Kynurenine × 0.03)
    #
    # Positive BDNF → neuroprotective upregulation → raises score.
    # Positive S100B → glial/injury signal → lowers score.
    # Positive Kynurenine → neuroinflammation / serotonin depletion → lowers score.
    #
    # To extend:
    #   - Add GFAP urine post/pre ratio as another penalty term.
    #   - Incorporate Cortisol logFC (positive = more stress = penalty).
    #   - Weight 5-HIAA: low serotonin metabolite = another penalty.
    # ----------------------------------------------------------
    bdnf      = prot_vals.get('BDNF', 0)
    s100b     = prot_vals.get('S100B', 0)
    kyn_logfc = met_vals.get('Kynurenine', 0) or 0

    score = 0.5 + bdnf * 0.08 - s100b * 0.05 - kyn_logfc * 0.03
    score = round(float(np.clip(score, 0.05, 0.95)), 3)

    biomarkers = {
        'Proteomics (logFC flight vs. preflight)':                        prot_vals,
        'Urine Inflammation Panel — neuro markers (npq by timepoint)':   urine_vals,
        'Metabolomics (logFC)':                                           met_vals,
    }
    return score, biomarkers


# ============================================================
# UI HELPERS
# ============================================================

def get_color(category, score):
    """
    Map a score to a traffic-light color based on the category's direction.

    Note the asymmetry:
      - Bone Efficacy and Neuro Resilience: high score = good = green.
      - Cardiotoxicity Safety:              low score  = good = green.

    Args:
        category (str): One of the three tab category names.
        score (float): Score in [0, 1].

    Returns:
        str: 'green', 'yellow', or 'red'.
    """
    if category == "Bone Density Loss Inhibitor Efficacy":
        return "green" if score > 0.7 else "yellow" if score > 0.4 else "red"
    if category == "Cardiotoxicity Safety":
        return "green" if score < 0.35 else "yellow" if score < 0.65 else "red"
    if category == "Neurological Resilience":
        return "green" if score > 0.6 else "yellow" if score > 0.35 else "red"


def render_circle(color, score):
    """
    Render a large colored circle with the score value in the center.

    Args:
        color (str): CSS color string ('green', 'yellow', 'red', or hex).
        score (float): Numeric score to display inside the circle.
    """
    st.markdown(
        f"""
        <div style="
            width: 140px;
            height: 140px;
            border-radius: 50%;
            background-color: {color};
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            font-weight: bold;
            color: black;
        ">
        {score:.3f}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("Controls")

# Show a data-load error in the sidebar so the app stays usable for UI testing
# even when CSV files are missing.
if not DATA_LOADED:
    st.sidebar.error(f"⚠️ Could not load CSV data from:\n`{DATA_DIR}`\n\nError: {DATA_ERROR}")
    st.sidebar.info("Adjust `DATA_DIR` at the top of `app.py` to point to your `data/processed/` folder.")

# Crew member selector — passed into all three score functions
crew = st.sidebar.selectbox("Crew Member", ["C001", "C002", "C003", "C004"])


# ============================================================
# TAB LAYOUT
# Three tabs, one per health domain.
# ============================================================
tabs = st.tabs([
    "🦴 Bone Density Loss Inhibitor Efficacy",
    "❤️ Cardiotoxicity Safety",
    "🧠 Neurological Resilience"
])


# ============================================================
# TAB 1 — BONE DENSITY LOSS INHIBITOR EFFICACY
# ============================================================
with tabs[0]:
    category = "Bone Density Loss Inhibitor Efficacy"
    score, biomarkers = compute_bone_score(crew)
    color = get_color(category, score)

    st.title(category)

    col1, col2 = st.columns([1, 3])
    with col1:
        render_circle(color, score)
    with col2:
        st.write(
            "Therapeutic effectiveness in preventing bone density loss in microgravity. "
            "Score derived from plasma proteomics logFC (flight vs. preflight), "
            "serum CMP values, urine inflammation panel, and plasma metabolomics."
        )
        if DATA_LOADED:
            st.caption(
                f"Data source: 20 proteomics markers · Calcium & Alk Phos (CMP) · "
                f"13 urine panel markers · 8 metabolomics targets — Crew {crew}"
            )

    # Expandable sections showing the raw biomarker data
    for section, vals in biomarkers.items():
        with st.expander(section):
            st.json(vals)


# ============================================================
# TAB 2 — CARDIOTOXICITY SAFETY
# ============================================================
with tabs[1]:
    category = "Cardiotoxicity Safety"
    score, biomarkers = compute_cardio_score(crew)
    color = get_color(category, score)

    st.title(category)

    col1, col2 = st.columns([1, 3])
    with col1:
        render_circle(color, score)
    with col2:
        st.write(
            "Assessment of cardiac stress, inflammation, and toxicity risk. "
            "Score reflects post-flight elevation of cardiac inflammatory markers "
            "(Cardiac Cytokine Array) relative to pre-flight baseline, combined with "
            "proteomics signals (VWF, SERPINE1/PAI-1, PF4)."
        )
        if DATA_LOADED:
            st.caption(f"Data source: 9 cardiac cytokine markers (Eve) · 3 proteomics targets — Crew {crew}")

    for section, vals in biomarkers.items():
        with st.expander(section):
            st.json(vals)


# ============================================================
# TAB 3 — NEUROLOGICAL RESILIENCE
# ============================================================
with tabs[2]:
    category = "Neurological Resilience"
    score, biomarkers = compute_neuro_score(crew)
    color = get_color(category, score)

    st.title(category)

    col1, col2 = st.columns([1, 3])
    with col1:
        render_circle(color, score)
    with col2:
        st.write(
            "Neuro-inflammatory shift and recovery trajectory. "
            "Score reflects BDNF neuroprotection signal (proteomics), "
            "neuro-damage markers (S100B, GFAP), kynurenine pathway activity, "
            "and serotonin metabolite (5-HIAA) from plasma metabolomics."
        )
        if DATA_LOADED:
            st.caption(
                f"Data source: 5 proteomics targets · 4 urine neuro markers · "
                f"6 metabolomics targets — Crew {crew}"
            )

    for section, vals in biomarkers.items():
        with st.expander(section):
            st.json(vals)
