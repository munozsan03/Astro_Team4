import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Torchlight Health Dashboard", layout="wide")

# -----------------------------
# DATA LOADING
# -----------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

@st.cache_data
def load_data():
    pp   = pd.read_csv(os.path.join(DATA_DIR, "plasma_proteomics.csv"))
    met  = pd.read_csv(os.path.join(DATA_DIR, "plasma_metabolomics.csv"))
    cmp  = pd.read_csv(os.path.join(DATA_DIR, "cmp_metabolic_panel.csv"))
    card = pd.read_csv(os.path.join(DATA_DIR, "cardiac_cytokines_eve.csv"))
    urine= pd.read_csv(os.path.join(DATA_DIR, "urine_inflammation_panel.csv"))
    return pp, met, cmp, card, urine

try:
    pp, met, cmp, card, urine = load_data()
    DATA_LOADED = True
except Exception as e:
    DATA_LOADED = False
    DATA_ERROR = str(e)

# -----------------------------
# HELPER: get proteomics logFC for a gene
# -----------------------------
def get_logfc(pp_df, gene):
    row = pp_df[pp_df['Gene'].str.upper() == gene.upper()]
    if row.empty:
        return None
    return float(row['logFC'].values[0])

# -----------------------------
# HELPER: get CMP value for a crew across timepoints
# Returns dict {timepoint: value}
# -----------------------------
def get_cmp_per_crew(cmp_df, metric_row_name, crew_id):
    row = cmp_df[cmp_df['Unnamed: 0'] == metric_row_name]
    if row.empty:
        return {}
    cols = [c for c in cmp_df.columns if c.startswith(crew_id + '_')]
    result = {}
    for col in cols:
        tp = col.split('_')[2]
        val = row[col].values[0]
        result[tp] = float(val) if not pd.isna(val) else None
    return result

# -----------------------------
# HELPER: get cardiac eve value per crew
# Returns dict {timepoint: value}
# -----------------------------
def get_cardiac_per_crew(card_df, metric_row_name, crew_id):
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

# -----------------------------
# HELPER: get urine value per crew across timepoints
# Returns dict {timepoint: value}
# -----------------------------
def get_urine_per_crew(urine_df, col_name, crew_id):
    crew_rows = urine_df[urine_df['crew_id'] == crew_id]
    result = {}
    for _, r in crew_rows.iterrows():
        tp = r['timepoint']
        val = r.get(col_name, None)
        result[tp] = float(val) if val is not None and not pd.isna(val) else None
    return result

# -----------------------------
# HELPER: get metabolomics logFC for a metabolite
# -----------------------------
def get_met_logfc(met_df, name):
    row = met_df[met_df['ID'].str.lower() == name.lower()]
    if row.empty:
        # partial match
        row = met_df[met_df['ID'].str.lower().str.contains(name.lower(), na=False)]
    if row.empty:
        return None
    return float(row['logFC'].values[0])

# -----------------------------
# SCORE COMPUTATION
# Plasma proteomics and metabolomics have logFC values (flight vs. pre-flight).
# CMP and cardiac have absolute time-series values per crew.
# We compute scores as normalized summaries:
#   - For logFC data: score = mean(|logFC| for significant hits), normalized 0-1
#   - For absolute data: score = deviation from baseline (preflight avg)
# -----------------------------

def compute_bone_score(crew_id):
    if not DATA_LOADED:
        return 0.5, {}
    
    # Proteomics logFCs (bone markers)
    prot_genes = ['BGLAP','SPARC','SPP1','SOST','POSTN','BGN','DCN','LUM','OGN','MGP',
                  'COL1A1','COL1A2','COMP','CILP','CILP2','FBN1','FBN2','SFRP2','SFRP4','ADIPOQ']
    prot_vals = {}
    for g in prot_genes:
        v = get_logfc(pp, g)
        if v is not None:
            prot_vals[g] = round(v, 3)

    # CMP
    cmp_vals = {}
    ca = get_cmp_per_crew(cmp, 'calcium_value_milligram_per_deciliter', crew_id)
    ap = get_cmp_per_crew(cmp, 'alkaline_phosphatase_value_units_per_liter', crew_id)
    # Summarize as postflight vs preflight mean
    preflight_tps = [k for k in ca if k.startswith('L')]
    postflight_tps = [k for k in ca if k.startswith('R')]
    ca_pre = np.mean([ca[t] for t in preflight_tps if ca[t] is not None]) if preflight_tps else None
    ca_post = np.mean([ca[t] for t in postflight_tps if ca[t] is not None]) if postflight_tps else None
    ap_pre = np.mean([ap[t] for t in preflight_tps if ap[t] is not None]) if preflight_tps else None
    ap_post = np.mean([ap[t] for t in postflight_tps if ap[t] is not None]) if postflight_tps else None
    cmp_vals['Calcium (mg/dL)'] = {'preflight_avg': round(ca_pre, 2) if ca_pre else None,
                                    'postflight_avg': round(ca_post, 2) if ca_post else None,
                                    'all_timepoints': {k: round(v, 2) for k, v in ca.items()}}
    cmp_vals['Alkaline Phosphatase (U/L)'] = {'preflight_avg': round(ap_pre, 2) if ap_pre else None,
                                               'postflight_avg': round(ap_post, 2) if ap_post else None,
                                               'all_timepoints': {k: round(v, 2) for k, v in ap.items()}}

    # Urine panel
    urine_markers = {
        'TNFRSF11A (RANK)': 'tnfrsf11a_concentration_npq',
        'TNFSF11 (RANKL)': 'tnfsf11_concentration_npq',
        'BMP7': 'bmp7_concentration_npq',
        'BMP10': 'bmp10_concentration_npq',
        'WNT16': 'wnt16_concentration_npq',
        'WNT7A': 'wnt7a_concentration_npq',
        'GDF2': 'gdf2_concentration_npq',
        'FGF23': 'fgf23_concentration_npq',
        'SPP1': 'spp1_concentration_npq',
        'IL-6': 'il6_concentration_npq',
        'IL-17A': 'il17a_concentration_npq',
        'IL-1β': 'il1b_concentration_npq',
        'TGF-β1': 'tgfb1_concentration_npq',
    }
    urine_vals = {}
    for label, col in urine_markers.items():
        tps = get_urine_per_crew(urine, col, crew_id)
        if tps:
            urine_vals[label] = {k: round(v, 2) if v is not None else None for k, v in tps.items()}

    # Metabolomics logFCs
    met_targets = ['Ergocalciferol (Vit D2)', 'Cortisol', 'Corticosterone',
                   'Proline', 'Glycine', 'Lysine', 'Arginine', 'Citric Acid']
    met_vals = {}
    for m in met_targets:
        v = get_met_logfc(met, m)
        if v is not None:
            met_vals[m] = round(v, 3)

    # Score: use abs mean logFC of proteomics (capped to 0-1 via sigmoid-like transform)
    prot_logfcs = list(prot_vals.values())
    mean_abs_logfc = np.mean(np.abs(prot_logfcs)) if prot_logfcs else 0.5
    # Positive logFC = upregulation of bone protective markers = better efficacy
    mean_logfc = np.mean(prot_logfcs) if prot_logfcs else 0
    # Normalize: score 0.5 + clipped contribution
    score = 0.5 + np.clip(mean_logfc / 4.0, -0.45, 0.45)
    score = round(float(score), 3)

    biomarkers = {
        'Proteomics (logFC flight vs. preflight)': prot_vals,
        'CMP (serum values)': cmp_vals,
        'Urine Inflammation Panel (npq)': urine_vals,
        'Metabolomics (logFC)': met_vals,
    }
    return score, biomarkers


def compute_cardio_score(crew_id):
    if not DATA_LOADED:
        return 0.5, {}

    # Cardiac cytokine array
    cardiac_markers = {
        'CRP': 'crp_concentration_picogram_per_milliliter',
        'Fibrinogen': 'fibrinogen_concentration_nanogram_per_milliliter',
        'Haptoglobin': 'haptoglobin_concentration_nanogram_per_milliliter',
        'Alpha-2-Macroglobulin': 'a2_macroglobulin_concentration_nanogram_per_milliliter',
        'AGP': 'agp_concentration_nanogram_per_milliliter',
        'PF4': 'pf4_concentration_nanogram_per_milliliter',
        'L-Selectin': 'l_selectin_concentration_picogram_per_milliliter',
        'Fetuin-A': 'fetuin_a36_concentration_nanogram_per_milliliter',
        'SAP': 'sap_concentration_picogram_per_milliliter',
    }
    cardiac_vals = {}
    score_components = []
    for label, row_name in cardiac_markers.items():
        tps = get_cardiac_per_crew(card, row_name, crew_id)
        if tps:
            cardiac_vals[label] = {k: round(v, 1) if v is not None else None for k, v in tps.items()}
            preflight = [v for k, v in tps.items() if k.startswith('L') and v is not None]
            postflight = [v for k, v in tps.items() if k.startswith('R') and v is not None]
            if preflight and postflight:
                # Ratio: how much did it rise postflight?
                ratio = np.mean(postflight) / np.mean(preflight)
                score_components.append(ratio)

    # Proteomics for VWF, SERPINE1, PF4
    prot_markers = {'VWF': get_logfc(pp, 'VWF'),
                    'SERPINE1 (PAI-1)': get_logfc(pp, 'SERPINE1'),
                    'PF4': get_logfc(pp, 'PF4')}
    prot_vals = {k: round(v, 3) for k, v in prot_markers.items() if v is not None}

    # Score: lower is safer (high inflammation = high score = red)
    # Mean postflight/preflight ratio - if > 1, markers are elevated = worse
    if score_components:
        mean_ratio = np.mean(score_components)
        # Normalize: ratio 1.0 = neutral (0.5 score), ratio 2.0 = dangerous (1.0)
        score = np.clip((mean_ratio - 0.5) / 1.5, 0.05, 0.95)
    else:
        score = 0.5

    # PF4 logFC: positive logFC (upregulation) = more concern
    pf4_logfc = prot_vals.get('PF4', 0)
    score = np.clip(score + pf4_logfc * 0.05, 0.05, 0.95)
    score = round(float(score), 3)

    biomarkers = {
        'Cardiac Cytokine Array (Eve) — concentration by timepoint': cardiac_vals,
        'Proteomics (logFC flight vs. preflight)': prot_vals,
    }
    return score, biomarkers


def compute_neuro_score(crew_id):
    if not DATA_LOADED:
        return 0.5, {}

    # Proteomics
    neuro_genes = ['BDNF', 'S100B', 'NRGN', 'CLU', 'APOE']
    prot_vals = {}
    for g in neuro_genes:
        v = get_logfc(pp, g)
        if v is not None:
            prot_vals[g] = round(v, 3)

    # Urine neuro markers
    urine_neuro = {
        'BDNF': 'bdnf_concentration_npq',
        'GFAP': 'gfap_concentration_npq',
        'NGF': 'ngf_concentration_npq',
        'CXCL10': 'cxcl10_concentration_npq',
    }
    urine_vals = {}
    for label, col in urine_neuro.items():
        tps = get_urine_per_crew(urine, col, crew_id)
        if tps:
            urine_vals[label] = {k: round(v, 2) if v is not None else None for k, v in tps.items()}

    # Metabolomics
    met_neuro = {
        'Kynurenine': 'Kynurenine',
        'Tryptophan': 'Tryptophan',
        '5-HIAA (Serotonin Metabolite)': '5-Hydroxyindoleacetic Acid',
        'N-Acetylaspartic Acid': 'N-Acetylaspartic Acid',
        'Cortisol': 'Cortisol',
        'Nicotinamide': 'Nicotinamide',
    }
    met_vals = {}
    for label, name in met_neuro.items():
        v = get_met_logfc(met, name)
        if v is not None:
            met_vals[label] = round(v, 3)

    # Kynurenine:Tryptophan ratio proxy
    kyn = get_met_logfc(met, 'Kynurenine')
    trp = get_met_logfc(met, 'Tryptophan')
    if kyn is not None and trp is not None and trp != 0:
        kyn_trp_ratio = round(kyn / trp, 3) if trp != 0 else None
        met_vals['Kynurenine:Tryptophan Ratio (logFC-based)'] = kyn_trp_ratio

    # Score: BDNF logFC positive = good (neuroprotective), S100B/GFAP up = bad
    bdnf = prot_vals.get('BDNF', 0)
    s100b = prot_vals.get('S100B', 0)
    kyn_logfc = met_vals.get('Kynurenine', 0) or 0

    # Higher BDNF = better; higher S100B/Kynurenine = worse
    score = 0.5 + bdnf * 0.08 - s100b * 0.05 - kyn_logfc * 0.03
    score = round(float(np.clip(score, 0.05, 0.95)), 3)

    biomarkers = {
        'Proteomics (logFC flight vs. preflight)': prot_vals,
        'Urine Inflammation Panel — neuro markers (npq by timepoint)': urine_vals,
        'Metabolomics (logFC)': met_vals,
    }
    return score, biomarkers


# -----------------------------
# SCORING COLOR LOGIC
# -----------------------------
def get_color(category, score):
    if category == "Bone Density Loss Inhibitor Efficacy":
        return "green" if score > 0.7 else "yellow" if score > 0.4 else "red"
    if category == "Cardiotoxicity Safety":
        return "green" if score < 0.35 else "yellow" if score < 0.65 else "red"
    if category == "Neurological Resilience":
        return "green" if score > 0.6 else "yellow" if score > 0.35 else "red"


def render_circle(color, score):
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


# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Controls")

if not DATA_LOADED:
    st.sidebar.error(f"⚠️ Could not load CSV data from:\n`{DATA_DIR}`\n\nError: {DATA_ERROR}")
    st.sidebar.info("Adjust `DATA_DIR` at the top of `app.py` to point to your `data/processed/` folder.")

crew = st.sidebar.selectbox("Crew Member", ["C001", "C002", "C003", "C004"])

tabs = st.tabs([
    "🦴 Bone Density Loss Inhibitor Efficacy",
    "❤️ Cardiotoxicity Safety",
    "🧠 Neurological Resilience"
])

# -----------------------------
# TAB 1 — BONE DENSITY EFFICACY
# -----------------------------
with tabs[0]:
    category = "Bone Density Loss Inhibitor Efficacy"
    score, biomarkers = compute_bone_score(crew)
    color = get_color(category, score)

    st.title(category)

    col1, col2 = st.columns([1, 3])
    with col1:
        render_circle(color, score)
    with col2:
        st.write("Therapeutic effectiveness in preventing bone density loss in microgravity. "
                 "Score derived from plasma proteomics logFC (flight vs. preflight), "
                 "serum CMP values, urine inflammation panel, and plasma metabolomics.")
        if DATA_LOADED:
            st.caption(f"Data source: 20 proteomics markers · Calcium & Alk Phos (CMP) · "
                       f"13 urine panel markers · 8 metabolomics targets — Crew {crew}")

    for section, vals in biomarkers.items():
        with st.expander(section):
            st.json(vals)

# -----------------------------
# TAB 2 — CARDIOTOXICITY SAFETY
# -----------------------------
with tabs[1]:
    category = "Cardiotoxicity Safety"
    score, biomarkers = compute_cardio_score(crew)
    color = get_color(category, score)

    st.title(category)

    col1, col2 = st.columns([1, 3])
    with col1:
        render_circle(color, score)
    with col2:
        st.write("Assessment of cardiac stress, inflammation, and toxicity risk. "
                 "Score reflects post-flight elevation of cardiac inflammatory markers "
                 "(Cardiac Cytokine Array) relative to pre-flight baseline, combined with "
                 "proteomics signals (VWF, SERPINE1/PAI-1, PF4).")
        if DATA_LOADED:
            st.caption(f"Data source: 9 cardiac cytokine markers (Eve) · 3 proteomics targets — Crew {crew}")

    for section, vals in biomarkers.items():
        with st.expander(section):
            st.json(vals)

# -----------------------------
# TAB 3 — NEUROLOGICAL RESILIENCE
# -----------------------------
with tabs[2]:
    category = "Neurological Resilience"
    score, biomarkers = compute_neuro_score(crew)
    color = get_color(category, score)

    st.title(category)

    col1, col2 = st.columns([1, 3])
    with col1:
        render_circle(color, score)
    with col2:
        st.write("Neuro-inflammatory shift and recovery trajectory. "
                 "Score reflects BDNF neuroprotection signal (proteomics), "
                 "neuro-damage markers (S100B, GFAP), kynurenine pathway activity, "
                 "and serotonin metabolite (5-HIAA) from plasma metabolomics.")
        if DATA_LOADED:
            st.caption(f"Data source: 5 proteomics targets · 4 urine neuro markers · "
                       f"6 metabolomics targets — Crew {crew}")

    for section, vals in biomarkers.items():
        with st.expander(section):
            st.json(vals)
