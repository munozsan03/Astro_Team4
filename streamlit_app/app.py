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


# ============================================================
# ╔══════════════════════════════════════════════════════════╗
# ║   BONE EFFICACY — EDITABLE PARAMETERS & WEIGHTS         ║
# ╚══════════════════════════════════════════════════════════╝
#
# HOW TO EDIT:
#   Each biomarker entry has:
#     "low"    : logFC (or ratio/npq) threshold → maps to score = 0
#     "high"   : logFC (or ratio/npq) threshold → maps to score = 100
#     "weight" : relative contribution to the Total Efficacy Score
#                (weights are auto-normalized, so only relative size matters)
#     "note"   : justification for the chosen thresholds
#
# For proteomics/metabolomics: values are logFC (log2 flight vs. pre-flight).
#   Positive logFC = upregulated in flight.
# For CMP: values are post-flight / pre-flight ratio.
#   1.0 = no change; >1 = elevated post-flight.
# For urine: values are post-flight / pre-flight ratio of npq concentrations.
#
# DIRECTION FLAGS:
#   "higher_is_better" = True  → high logFC/ratio is a GOOD sign (bone formation)
#   "higher_is_better" = False → high logFC/ratio is a BAD sign (bone resorption)
#   The scoring function uses this to flip the scale when needed.
# ============================================================

BONE_BIOMARKER_PARAMS = {

    # ── PROTEOMICS (logFC, flight vs. pre-flight) ───────────────────────────
    # Bone matrix / formation proteins — upregulation is protective.
    # logFC range reference: typical plasma proteomics spans roughly −3 to +3.
    # We use ±2 as meaningful signal boundaries.

    "BGLAP (Osteocalcin)": {
        "low": -2.0, "high": 2.0, "weight": 8, "higher_is_better": True,
        "note": "Primary osteoblast-secreted bone matrix protein. Upregulation signals active bone formation. logFC > 0 is protective."
    },
    "SPARC (Osteonectin)": {
        "low": -2.0, "high": 2.0, "weight": 6, "higher_is_better": True,
        "note": "Bone mineralization scaffolding protein. Higher expression supports matrix deposition."
    },
    "SPP1 (Osteopontin — proteomics)": {
        "low": -2.0, "high": 2.0, "weight": 4, "higher_is_better": False,
        "note": "Osteopontin also promotes osteoclast activity. Upregulation here signals resorption risk. Lower is better."
    },
    "SOST (Sclerostin)": {
        "low": -2.0, "high": 2.0, "weight": 8, "higher_is_better": False,
        "note": "Sclerostin inhibits Wnt signaling and suppresses bone formation. Downregulation (negative logFC) is the goal of most bone-protective drugs."
    },
    "POSTN (Periostin)": {
        "low": -2.0, "high": 2.0, "weight": 5, "higher_is_better": True,
        "note": "Periosteal bone formation marker. Upregulation indicates drug is stimulating new bone deposition."
    },
    "BGN (Biglycan)": {
        "low": -2.0, "high": 2.0, "weight": 4, "higher_is_better": True,
        "note": "Bone matrix proteoglycan that regulates collagen fibrillogenesis. Higher = better matrix integrity."
    },
    "DCN (Decorin)": {
        "low": -2.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "note": "Collagen-binding proteoglycan. Supports structural bone matrix."
    },
    "COL1A1 (Collagen I α1)": {
        "low": -2.0, "high": 2.0, "weight": 7, "higher_is_better": True,
        "note": "Primary structural collagen of bone. Upregulation directly reflects bone matrix synthesis."
    },
    "COL1A2 (Collagen I α2)": {
        "low": -2.0, "high": 2.0, "weight": 5, "higher_is_better": True,
        "note": "Partners with COL1A1 to form mature type-I collagen triple helix."
    },
    "SFRP2 (Wnt modulator)": {
        "low": -2.0, "high": 2.0, "weight": 4, "higher_is_better": True,
        "note": "SFRP2 can act as a Wnt pathway facilitator in bone context; mild upregulation is generally supportive."
    },
    "SFRP4 (Wnt modulator)": {
        "low": -2.0, "high": 2.0, "weight": 3, "higher_is_better": False,
        "note": "SFRP4 inhibits Wnt signaling and is associated with osteoporosis. Downregulation is favorable."
    },
    "MGP (Matrix Gla Protein)": {
        "low": -2.0, "high": 2.0, "weight": 3, "higher_is_better": False,
        "note": "MGP inhibits mineralization when elevated. Some downregulation may support mineral deposition."
    },
    "ADIPOQ (Adiponectin)": {
        "low": -2.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "note": "Adiponectin promotes osteoblast differentiation and inhibits osteoclast activity."
    },

    # ── CMP — SERUM CHEMISTRY (post-flight / pre-flight ratio) ──────────────
    # Ratio = 1.0 means no change. Thresholds set around clinically meaningful shifts.

    "Calcium (CMP ratio)": {
        "low": 0.90, "high": 1.10, "weight": 6, "higher_is_better": True,
        "note": "Serum calcium supports bone mineral density. A post/pre ratio below 0.90 suggests hypocalcemia / bone resorption mobilizing calcium out of bone faster than dietary intake replaces it. Ratio above 1.10 may indicate hypercalcemia from excess bone breakdown or supplementation."
    },
    "Alkaline Phosphatase (CMP ratio)": {
        "low": 0.80, "high": 1.40, "weight": 5, "higher_is_better": True,
        "note": "Alk Phos is a marker of osteoblast activity. Modest elevation (ratio 1.0–1.4) indicates active bone formation — a positive drug response. Ratio > 1.4 may reflect liver stress or excessive turnover. Ratio < 0.80 suggests suppressed osteoblast activity."
    },

    # ── URINE INFLAMMATION PANEL (post-flight / pre-flight ratio, npq) ──────
    # These are cytokines that drive or suppress osteoclast activity.

    "RANKL (urine ratio)": {
        "low": 0.80, "high": 2.0, "weight": 7, "higher_is_better": False,
        "note": "RANKL drives osteoclastogenesis. Elevated post-flight ratio signals continued bone resorption stimulus. Anti-RANKL drugs (e.g. denosumab) should suppress this; ratio < 1.0 is the therapeutic goal."
    },
    "RANK (urine ratio)": {
        "low": 0.80, "high": 2.0, "weight": 4, "higher_is_better": False,
        "note": "RANK receptor expression on osteoclast precursors. Elevated post-flight ratio indicates increased osteoclast priming."
    },
    "BMP7 (urine ratio)": {
        "low": 0.80, "high": 2.0, "weight": 5, "higher_is_better": True,
        "note": "BMP7 is osteogenic; promotes osteoblast differentiation. Higher post-flight ratio is a protective sign."
    },
    "WNT16 (urine ratio)": {
        "low": 0.80, "high": 2.0, "weight": 5, "higher_is_better": True,
        "note": "WNT16 is a key bone formation signal that suppresses osteoclastogenesis. Higher ratio is beneficial."
    },
    "FGF23 (urine ratio)": {
        "low": 0.80, "high": 2.0, "weight": 4, "higher_is_better": False,
        "note": "FGF23 inhibits Vitamin D activation and phosphate reabsorption. Elevated FGF23 post-flight compromises bone mineral metabolism."
    },
    "IL-6 (urine ratio)": {
        "low": 0.80, "high": 2.0, "weight": 5, "higher_is_better": False,
        "note": "IL-6 activates osteoclasts and drives bone loss. Elevated post-flight IL-6 is a direct bone-resorption signal."
    },
    "IL-17A (urine ratio)": {
        "low": 0.80, "high": 2.0, "weight": 4, "higher_is_better": False,
        "note": "IL-17A stimulates osteoclast differentiation and is linked to inflammatory bone loss."
    },
    "TGF-β1 (urine ratio)": {
        "low": 0.80, "high": 1.60, "weight": 3, "higher_is_better": True,
        "note": "TGF-β1 is pleiotropic: modest elevation supports bone formation coupling, but very high levels can promote resorption. Moderate post-flight elevation is a positive sign."
    },

    # ── METABOLOMICS (logFC, flight vs. pre-flight) ──────────────────────────

    "Vitamin D2 (Ergocalciferol)": {
        "low": -2.0, "high": 2.0, "weight": 6, "higher_is_better": True,
        "note": "Vitamin D is essential for calcium absorption and bone mineralization. Upregulation strongly supports bone health intervention efficacy."
    },
    "Cortisol (metabolomics)": {
        "low": -2.0, "high": 2.0, "weight": 5, "higher_is_better": False,
        "note": "Chronic cortisol elevation suppresses osteoblasts and promotes bone loss (glucocorticoid-induced osteoporosis). Downregulation is protective."
    },
    "Proline": {
        "low": -2.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "note": "Proline is a primary amino acid in collagen. Higher availability supports bone matrix synthesis."
    },
    "Glycine": {
        "low": -2.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "note": "Glycine is the most abundant amino acid in collagen (every third residue). Higher availability supports bone matrix production."
    },
    "Lysine": {
        "low": -2.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "note": "Lysine is essential for collagen cross-linking, which determines bone mechanical strength."
    },
    "Citric Acid": {
        "low": -2.0, "high": 2.0, "weight": 2, "higher_is_better": True,
        "note": "Citrate is incorporated into bone mineral crystals. Higher citrate supports bone mineral integrity."
    },
}


# ============================================================
# BONE SCORE ENGINE
# ============================================================

def score_biomarker(value, low, high, higher_is_better):
    """
    Map a raw biomarker value to a 0–100 score.

    The range [low, high] defines the full scale.
    Values outside this range are clipped to [0, 100].
    'higher_is_better' flips the direction so the score always means:
        100 = maximally protective / efficacious
          0 = maximally harmful / no efficacy

    Args:
        value (float): The raw biomarker value (logFC, ratio, etc.)
        low (float): Value that maps to score 0 (worst)
        high (float): Value that maps to score 100 (best)
        higher_is_better (bool): If True, higher raw value → higher score.

    Returns:
        float: Score in [0, 100].
    """
    if value is None:
        return None
    if higher_is_better:
        score = (value - low) / (high - low) * 100
    else:
        score = (high - value) / (high - low) * 100
    return float(np.clip(score, 0, 100))


def render_score_bar(label, score, note, data_value=None, data_label="value"):
    """
    Render a single biomarker row: label, colored bar (green/red), numeric score,
    raw data value, and justification note — all inside the Streamlit app.

    Args:
        label (str): Biomarker display name.
        score (float | None): 0–100 score, or None if data unavailable.
        note (str): Justification for the parameter thresholds.
        data_value: Raw value to display alongside the score.
        data_label (str): Label for the raw value (e.g., 'logFC', 'ratio').
    """
    if score is None:
        st.markdown(f"**{label}** — *data not available*")
        return

    # Color: green above 50, red below, with an orange midzone
    if score >= 60:
        bar_color = "#2ecc71"       # green
        text_color = "#1a5e35"
    elif score >= 40:
        bar_color = "#f39c12"       # amber
        text_color = "#7d4e00"
    else:
        bar_color = "#e74c3c"       # red
        text_color = "#6e1a1a"

    bar_pct = score  # 0–100

    raw_display = ""
    if data_value is not None:
        raw_display = f"<span style='font-size:12px; color:#888;'>({data_label}: {data_value:+.3f})</span>"

    st.markdown(
        f"""
        <div style="margin-bottom: 10px;">
          <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:3px;">
            <span style="font-weight:600; font-size:14px;">{label}</span>
            <span style="font-weight:700; color:{text_color}; font-size:15px;">
              {score:.1f}/100 &nbsp; {raw_display}
            </span>
          </div>
          <div style="background:#e0e0e0; border-radius:6px; height:14px; width:100%;">
            <div style="background:{bar_color}; width:{bar_pct}%; height:14px; border-radius:6px; transition: width 0.4s;"></div>
          </div>
          <div style="font-size:11px; color:#777; margin-top:2px; font-style:italic;">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_total_score_bar(score):
    """
    Render a large, prominent total efficacy score bar at the top of the Bone tab.

    Args:
        score (float): Total weighted score 0–100.
    """
    if score >= 60:
        bar_color = "#27ae60"
        label_color = "#1a5e35"
        verdict = "✅ Drug Efficacy Signal: POSITIVE"
        verdict_color = "#1a5e35"
    elif score >= 40:
        bar_color = "#e67e22"
        label_color = "#7d4e00"
        verdict = "⚠️ Drug Efficacy Signal: UNCERTAIN"
        verdict_color = "#7d4e00"
    else:
        bar_color = "#c0392b"
        label_color = "#6e1a1a"
        verdict = "🚨 Drug Efficacy Signal: INSUFFICIENT"
        verdict_color = "#6e1a1a"

    st.markdown(
        f"""
        <div style="border:2px solid {bar_color}; border-radius:12px; padding:18px 22px; margin-bottom:24px; background:#fafafa;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:18px; font-weight:700; color:#333;">Total Bone Efficacy Score</span>
            <span style="font-size:28px; font-weight:900; color:{label_color};">{score:.1f} / 100</span>
          </div>
          <div style="background:#e0e0e0; border-radius:8px; height:22px; width:100%; margin-bottom:10px;">
            <div style="background:{bar_color}; width:{score}%; height:22px; border-radius:8px;"></div>
          </div>
          <div style="font-size:16px; font-weight:700; color:{verdict_color};">{verdict}</div>
          <div style="font-size:12px; color:#888; margin-top:4px;">
            Weighted composite across {len(BONE_BIOMARKER_PARAMS)} biomarkers (proteomics, CMP, urine panel, metabolomics).
            Score ≥ 60 = positive efficacy signal &nbsp;|&nbsp; 40–59 = uncertain &nbsp;|&nbsp; &lt; 40 = insufficient evidence of efficacy.
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HELPER FUNCTIONS (unchanged from original)
# ============================================================

def get_logfc(pp_df, gene):
    row = pp_df[pp_df['Gene'].str.upper() == gene.upper()]
    if row.empty:
        return None
    return float(row['logFC'].values[0])


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


def get_urine_per_crew(urine_df, col_name, crew_id):
    crew_rows = urine_df[urine_df['crew_id'] == crew_id]
    result = {}
    for _, r in crew_rows.iterrows():
        tp = r['timepoint']
        val = r.get(col_name, None)
        result[tp] = float(val) if val is not None and not pd.isna(val) else None
    return result


def get_met_logfc(met_df, name):
    row = met_df[met_df['ID'].str.lower() == name.lower()]
    if row.empty:
        row = met_df[met_df['ID'].str.lower().str.contains(name.lower(), na=False)]
    if row.empty:
        return None
    return float(row['logFC'].values[0])


# ============================================================
# MODULE 1 — BONE TAB (rewritten for 0–100 per-biomarker scoring)
# ============================================================

def render_bone_tab(crew_id):
    """
    Render the full Bone Density Loss Inhibitor Efficacy tab.
    Computes a 0–100 score for each biomarker and a weighted total.
    """
    st.title("🦴 Bone Density Loss Inhibitor Efficacy")
    st.write(
        "Each biomarker is scored 0–100 based on calibrated thresholds. "
        "The **Total Efficacy Score** is a weighted average across all biomarkers. "
        "**Green bars** indicate a protective/efficacious signal; "
        "**red bars** indicate bone-loss risk or insufficient drug effect."
    )

    # ── Gather raw data ──────────────────────────────────────────────────────

    # PROTEOMICS
    prot_map = {
        "BGLAP (Osteocalcin)":       get_logfc(pp, 'BGLAP'),
        "SPARC (Osteonectin)":        get_logfc(pp, 'SPARC'),
        "SPP1 (Osteopontin — proteomics)": get_logfc(pp, 'SPP1'),
        "SOST (Sclerostin)":          get_logfc(pp, 'SOST'),
        "POSTN (Periostin)":          get_logfc(pp, 'POSTN'),
        "BGN (Biglycan)":             get_logfc(pp, 'BGN'),
        "DCN (Decorin)":              get_logfc(pp, 'DCN'),
        "COL1A1 (Collagen I α1)":     get_logfc(pp, 'COL1A1'),
        "COL1A2 (Collagen I α2)":     get_logfc(pp, 'COL1A2'),
        "SFRP2 (Wnt modulator)":      get_logfc(pp, 'SFRP2'),
        "SFRP4 (Wnt modulator)":      get_logfc(pp, 'SFRP4'),
        "MGP (Matrix Gla Protein)":   get_logfc(pp, 'MGP'),
        "ADIPOQ (Adiponectin)":       get_logfc(pp, 'ADIPOQ'),
    }

    # CMP — compute post/pre ratios
    ca = get_cmp_per_crew(cmp, 'calcium_value_milligram_per_deciliter', crew_id)
    ap = get_cmp_per_crew(cmp, 'alkaline_phosphatase_value_units_per_liter', crew_id)

    def post_pre_ratio(tps_dict):
        pre  = [v for k, v in tps_dict.items() if k.startswith('L') and v is not None]
        post = [v for k, v in tps_dict.items() if k.startswith('R') and v is not None]
        if pre and post and np.mean(pre) != 0:
            return np.mean(post) / np.mean(pre)
        return None

    cmp_map = {
        "Calcium (CMP ratio)":               post_pre_ratio(ca),
        "Alkaline Phosphatase (CMP ratio)":   post_pre_ratio(ap),
    }

    # URINE — post/pre ratios
    urine_col_map = {
        "RANKL (urine ratio)":  'tnfsf11_concentration_npq',
        "RANK (urine ratio)":   'tnfrsf11a_concentration_npq',
        "BMP7 (urine ratio)":   'bmp7_concentration_npq',
        "WNT16 (urine ratio)":  'wnt16_concentration_npq',
        "FGF23 (urine ratio)":  'fgf23_concentration_npq',
        "IL-6 (urine ratio)":   'il6_concentration_npq',
        "IL-17A (urine ratio)": 'il17a_concentration_npq',
        "TGF-β1 (urine ratio)": 'tgfb1_concentration_npq',
    }
    urine_map = {}
    for label, col in urine_col_map.items():
        tps = get_urine_per_crew(urine, col, crew_id)
        urine_map[label] = post_pre_ratio(tps)

    # METABOLOMICS
    met_map = {
        "Vitamin D2 (Ergocalciferol)":  get_met_logfc(met, 'Ergocalciferol'),
        "Cortisol (metabolomics)":       get_met_logfc(met, 'Cortisol'),
        "Proline":                       get_met_logfc(met, 'Proline'),
        "Glycine":                       get_met_logfc(met, 'Glycine'),
        "Lysine":                        get_met_logfc(met, 'Lysine'),
        "Citric Acid":                   get_met_logfc(met, 'Citric Acid'),
    }

    # Merge all raw values into one lookup
    all_raw = {**prot_map, **cmp_map, **urine_map, **met_map}

    # ── Compute per-biomarker scores and weighted total ──────────────────────

    scores = {}
    for name, params in BONE_BIOMARKER_PARAMS.items():
        raw = all_raw.get(name)
        scores[name] = score_biomarker(
            raw, params["low"], params["high"], params["higher_is_better"]
        )

    # Weighted average (only over biomarkers with available data)
    total_weight = 0.0
    weighted_sum = 0.0
    for name, params in BONE_BIOMARKER_PARAMS.items():
        s = scores.get(name)
        if s is not None:
            weighted_sum += s * params["weight"]
            total_weight += params["weight"]

    total_score = (weighted_sum / total_weight) if total_weight > 0 else 50.0

    # ── Render total score ───────────────────────────────────────────────────
    render_total_score_bar(total_score)

    # ── Per-biomarker breakdown ──────────────────────────────────────────────
    sections = [
        ("🔬 Proteomics (logFC — flight vs. pre-flight)", prot_map, "logFC"),
        ("🧪 CMP Serum Chemistry (post/pre ratio)", cmp_map, "ratio"),
        ("💧 Urine Inflammation Panel (post/pre ratio)", urine_map, "ratio"),
        ("⚗️ Metabolomics (logFC — flight vs. pre-flight)", met_map, "logFC"),
    ]

    for section_title, raw_dict, val_label in sections:
        with st.expander(section_title, expanded=True):
            any_data = False
            for name, raw_val in raw_dict.items():
                params = BONE_BIOMARKER_PARAMS.get(name)
                if params is None:
                    continue
                s = scores.get(name)
                render_score_bar(
                    label=name,
                    score=s,
                    note=params["note"],
                    data_value=raw_val,
                    data_label=val_label,
                )
                any_data = True
            if not any_data:
                st.write("*No data available for this section.*")


# ============================================================
# MODULE 2 — CARDIOTOXICITY SAFETY (unchanged logic, score kept 0–1)
# ============================================================

def compute_cardio_score(crew_id):
    if not DATA_LOADED:
        return 0.5, {}

    cardiac_markers = {
        'CRP':                  'crp_concentration_picogram_per_milliliter',
        'Fibrinogen':           'fibrinogen_concentration_nanogram_per_milliliter',
        'Haptoglobin':          'haptoglobin_concentration_nanogram_per_milliliter',
        'Alpha-2-Macroglobulin':'a2_macroglobulin_concentration_nanogram_per_milliliter',
        'AGP':                  'agp_concentration_nanogram_per_milliliter',
        'PF4':                  'pf4_concentration_nanogram_per_milliliter',
        'L-Selectin':           'l_selectin_concentration_picogram_per_milliliter',
        'Fetuin-A':             'fetuin_a36_concentration_nanogram_per_milliliter',
        'SAP':                  'sap_concentration_picogram_per_milliliter',
    }
    cardiac_vals = {}
    score_components = []

    for label, row_name in cardiac_markers.items():
        tps = get_cardiac_per_crew(card, row_name, crew_id)
        if tps:
            cardiac_vals[label] = {k: round(v, 1) if v is not None else None for k, v in tps.items()}
            preflight  = [v for k, v in tps.items() if k.startswith('L') and v is not None]
            postflight = [v for k, v in tps.items() if k.startswith('R') and v is not None]
            if preflight and postflight:
                ratio = np.mean(postflight) / np.mean(preflight)
                score_components.append(ratio)

    prot_markers = {
        'VWF':              get_logfc(pp, 'VWF'),
        'SERPINE1 (PAI-1)': get_logfc(pp, 'SERPINE1'),
        'PF4':              get_logfc(pp, 'PF4'),
    }
    prot_vals = {k: round(v, 3) for k, v in prot_markers.items() if v is not None}

    if score_components:
        mean_ratio = np.mean(score_components)
        score = np.clip((mean_ratio - 0.5) / 1.5, 0.05, 0.95)
    else:
        score = 0.5

    pf4_logfc = prot_vals.get('PF4', 0)
    score = np.clip(score + pf4_logfc * 0.05, 0.05, 0.95)
    score = round(float(score), 3)

    biomarkers = {
        'Cardiac Cytokine Array (Eve) — concentration by timepoint': cardiac_vals,
        'Proteomics (logFC flight vs. preflight)':                   prot_vals,
    }
    return score, biomarkers


# ============================================================
# MODULE 3 — NEUROLOGICAL RESILIENCE (unchanged)
# ============================================================

def compute_neuro_score(crew_id):
    if not DATA_LOADED:
        return 0.5, {}

    neuro_genes = ['BDNF', 'S100B', 'NRGN', 'CLU', 'APOE']
    prot_vals = {}
    for g in neuro_genes:
        v = get_logfc(pp, g)
        if v is not None:
            prot_vals[g] = round(v, 3)

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

    met_neuro = {
        'Kynurenine':                    'Kynurenine',
        'Tryptophan':                    'Tryptophan',
        '5-HIAA (Serotonin Metabolite)': '5-Hydroxyindoleacetic Acid',
        'N-Acetylaspartic Acid':         'N-Acetylaspartic Acid',
        'Cortisol':                      'Cortisol',
        'Nicotinamide':                  'Nicotinamide',
    }
    met_vals = {}
    for label, name in met_neuro.items():
        v = get_met_logfc(met, name)
        if v is not None:
            met_vals[label] = round(v, 3)

    kyn = get_met_logfc(met, 'Kynurenine')
    trp = get_met_logfc(met, 'Tryptophan')
    if kyn is not None and trp is not None and trp != 0:
        met_vals['Kynurenine:Tryptophan Ratio (logFC-based)'] = round(kyn / trp, 3)

    bdnf      = prot_vals.get('BDNF', 0)
    s100b     = prot_vals.get('S100B', 0)
    kyn_logfc = met_vals.get('Kynurenine', 0) or 0

    score = 0.5 + bdnf * 0.08 - s100b * 0.05 - kyn_logfc * 0.03
    score = round(float(np.clip(score, 0.05, 0.95)), 3)

    biomarkers = {
        'Proteomics (logFC flight vs. preflight)':                      prot_vals,
        'Urine Inflammation Panel — neuro markers (npq by timepoint)': urine_vals,
        'Metabolomics (logFC)':                                         met_vals,
    }
    return score, biomarkers


# ============================================================
# UI HELPERS (for Cardio + Neuro tabs — unchanged)
# ============================================================

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
            width: 140px; height: 140px; border-radius: 50%;
            background-color: {color};
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; font-weight: bold; color: black;">
        {score:.3f}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("Controls")

if not DATA_LOADED:
    st.sidebar.error(f"⚠️ Could not load CSV data from:\n`{DATA_DIR}`\n\nError: {DATA_ERROR}")
    st.sidebar.info("Adjust `DATA_DIR` at the top of `app.py` to point to your `data/processed/` folder.")

crew = st.sidebar.selectbox("Crew Member", ["C001", "C002", "C003", "C004"])


# ============================================================
# TAB LAYOUT
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
    if DATA_LOADED:
        render_bone_tab(crew)
    else:
        st.warning("Data not loaded. Check the sidebar for details.")


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
