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
# CREW MEMBER SELECTION — SESSION STATE
# ============================================================
CREW_CONFIG = {
    "C001": {"label": "Crew Member 1", "color": "#3b82f6", "hover": "#2563eb", "text": "#ffffff"},
    "C002": {"label": "Crew Member 2", "color": "#10b981", "hover": "#059669", "text": "#ffffff"},
    "C003": {"label": "Crew Member 3", "color": "#f59e0b", "hover": "#d97706", "text": "#ffffff"},
    "C004": {"label": "Crew Member 4", "color": "#ef4444", "hover": "#dc2626", "text": "#ffffff"},
}

if "selected_crew" not in st.session_state:
    st.session_state.selected_crew = "C001"


# ============================================================
# ╔══════════════════════════════════════════════════════════╗
# ║   BONE EFFICACY — EDITABLE PARAMETERS & WEIGHTS         ║
# ╚══════════════════════════════════════════════════════════╝
BONE_BIOMARKER_PARAMS = {

    # ── PROTEOMICS (logFC, flight vs. pre-flight) ───────────────────────────

    "BGLAP (Osteocalcin)": {
        "low": -0.5, "high": 2.0, "weight": 8, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Primary osteoblast-secreted bone matrix protein. Upregulation signals active bone formation. Only penalized when logFC drops below -0.5."
    },
    "SPARC (Osteonectin)": {
        "low": -0.5, "high": 2.0, "weight": 6, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Bone mineralization scaffolding protein. Higher expression supports matrix deposition. Only penalized when logFC drops below -0.5."
    },
    "SPP1 (Osteopontin — proteomics)": {
        "low": -2.0, "high": 0.75, "weight": 4, "higher_is_better": False,
        "threshold_type": "high",
        "note": "Osteopontin promotes osteoclast activity. Only penalized when logFC rises above +0.75."
    },
    "SOST (Sclerostin)": {
        "low": -2.0, "high": 0.5, "weight": 8, "higher_is_better": False,
        "threshold_type": "high",
        "note": "Sclerostin inhibits Wnt signaling and suppresses bone formation. Only penalized when logFC rises above +0.5."
    },
    "POSTN (Periostin)": {
        "low": -0.5, "high": 2.0, "weight": 5, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Periosteal bone formation marker. Only penalized when logFC drops below -0.5."
    },
    "BGN (Biglycan)": {
        "low": -0.75, "high": 2.0, "weight": 4, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Bone matrix proteoglycan regulating collagen fibrillogenesis. Only penalized when logFC drops below -0.75."
    },
    "DCN (Decorin)": {
        "low": -0.75, "high": 2.0, "weight": 3, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Collagen-binding proteoglycan supporting structural bone matrix. Only penalized when logFC drops below -0.75."
    },
    "COL1A1 (Collagen I α1)": {
        "low": -0.5, "high": 2.0, "weight": 7, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Primary structural collagen of bone. Only penalized when logFC drops below -0.5."
    },
    "COL1A2 (Collagen I α2)": {
        "low": -0.5, "high": 2.0, "weight": 5, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Partners with COL1A1 to form mature type-I collagen triple helix. Only penalized when logFC drops below -0.5."
    },
    "SFRP2 (Wnt modulator)": {
        "low": -1.0, "high": 1.5, "weight": 4, "higher_is_better": True,
        "threshold_type": "both",
        "note": "SFRP2 facilitates Wnt signaling in bone; mild upregulation is supportive but excessive dysregulation becomes inhibitory. Penalized below -1.0 and above +1.5."
    },
    "SFRP4 (Wnt modulator)": {
        "low": -2.0, "high": 0.5, "weight": 3, "higher_is_better": False,
        "threshold_type": "high",
        "note": "SFRP4 inhibits Wnt signaling and is associated with osteoporosis. Only penalized when logFC rises above +0.5."
    },
    "MGP (Matrix Gla Protein)": {
        "low": -2.0, "high": 0.75, "weight": 3, "higher_is_better": False,
        "threshold_type": "high",
        "note": "MGP inhibits mineralization when elevated. Only penalized when logFC rises above +0.75."
    },
    "ADIPOQ (Adiponectin)": {
        "low": -1.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "threshold_type": "both",
        "note": "Adiponectin promotes osteoblast differentiation. Moderate elevation is protective; penalized below -1.0 and above +2.0."
    },

    # ── CMP — SERUM CHEMISTRY (post-flight / pre-flight ratio) ──────────────

    "Calcium (CMP ratio)": {
        "low": 0.90, "high": 1.10, "weight": 6, "higher_is_better": True,
        "threshold_type": "both",
        "note": "Serum calcium must stay balanced. Ratio < 0.90 suggests hypocalcemia; ratio > 1.10 may indicate hypercalcemia. Penalized at both extremes."
    },
    "Alkaline Phosphatase (CMP ratio)": {
        "low": 0.80, "high": 1.40, "weight": 5, "higher_is_better": True,
        "threshold_type": "both",
        "note": "Alk Phos reflects osteoblast activity. Modest elevation is favorable; ratio > 1.4 may indicate liver stress or excessive turnover; ratio < 0.80 suggests suppressed osteoblasts."
    },

    # ── URINE INFLAMMATION PANEL (post-flight / pre-flight ratio, npq) ──────

    "RANKL (urine ratio)": {
        "low": 0.80, "high": 1.25, "weight": 7, "higher_is_better": False,
        "threshold_type": "high",
        "note": "RANKL drives osteoclastogenesis. Elevated post-flight ratio signals continued bone resorption stimulus. Only penalized when ratio rises above 1.25."
    },
    "RANK (urine ratio)": {
        "low": 0.80, "high": 1.25, "weight": 4, "higher_is_better": False,
        "threshold_type": "high",
        "note": "RANK receptor expression on osteoclast precursors. Only penalized when ratio rises above 1.25."
    },
    "BMP7 (urine ratio)": {
        "low": 0.90, "high": 2.0, "weight": 5, "higher_is_better": True,
        "threshold_type": "low",
        "note": "BMP7 promotes osteoblast differentiation. Higher post-flight ratio is protective. Only penalized when ratio drops below 0.90."
    },
    "WNT16 (urine ratio)": {
        "low": 0.90, "high": 2.0, "weight": 5, "higher_is_better": True,
        "threshold_type": "low",
        "note": "WNT16 suppresses osteoclastogenesis and supports cortical bone integrity. Only penalized when ratio drops below 0.90."
    },
    "FGF23 (urine ratio)": {
        "low": 0.80, "high": 1.20, "weight": 4, "higher_is_better": False,
        "threshold_type": "high",
        "note": "FGF23 inhibits Vitamin D activation and phosphate reabsorption. Only penalized when ratio rises above 1.20."
    },
    "IL-6 (urine ratio)": {
        "low": 0.80, "high": 1.30, "weight": 5, "higher_is_better": False,
        "threshold_type": "high",
        "note": "IL-6 activates osteoclasts and drives bone loss. Only penalized when ratio rises above 1.30."
    },
    "IL-17A (urine ratio)": {
        "low": 0.80, "high": 1.25, "weight": 4, "higher_is_better": False,
        "threshold_type": "high",
        "note": "IL-17A stimulates osteoclast differentiation and inflammatory bone loss. Only penalized when ratio rises above 1.25."
    },
    "TGF-β1 (urine ratio)": {
        "low": 0.80, "high": 1.60, "weight": 3, "higher_is_better": True,
        "threshold_type": "both",
        "note": "TGF-β1 is pleiotropic: modest elevation supports bone formation coupling, but very high levels can promote resorption/fibrosis imbalance. Penalized below 0.80 and above 1.60."
    },

    # ── METABOLOMICS (logFC, flight vs. pre-flight) ──────────────────────────

    "Vitamin D2 (Ergocalciferol)": {
        "low": -0.5, "high": 2.0, "weight": 6, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Vitamin D is essential for calcium absorption and bone mineralization. Only penalized when logFC drops below -0.5."
    },
    "Cortisol (metabolomics)": {
        "low": -2.0, "high": 0.75, "weight": 5, "higher_is_better": False,
        "threshold_type": "high",
        "note": "Chronic cortisol elevation suppresses osteoblasts and promotes bone loss. Only penalized when logFC rises above +0.75."
    },
    "Proline": {
        "low": -1.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Proline is a primary amino acid in collagen. Only penalized when logFC drops below -1.0."
    },
    "Glycine": {
        "low": -1.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Glycine is the most abundant amino acid in collagen. Only penalized when logFC drops below -1.0."
    },
    "Lysine": {
        "low": -1.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Lysine is essential for collagen cross-linking. Only penalized when logFC drops below -1.0."
    },
    "Citric Acid": {
        "low": -1.0, "high": 2.0, "weight": 2, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Citrate is incorporated into bone mineral crystals. Only penalized when logFC drops below -1.0."
    },
}


# ============================================================
# BONE SCORE ENGINE
# ============================================================

def score_biomarker(value, low, high, higher_is_better, threshold_type="both"):
    if value is None:
        return None

    span = high - low

    if threshold_type == "low":
        if higher_is_better:
            if value >= low:
                return 100.0
            score = (value - (low - span)) / span * 100
        else:
            if value >= low:
                return 100.0
            score = (value - (low - span)) / span * 100

    elif threshold_type == "high":
        if not higher_is_better:
            if value <= high:
                return 100.0
            score = ((high + span) - value) / span * 100
        else:
            if value <= high:
                return 100.0
            score = ((high + span) - value) / span * 100

    else:  # "both"
        if low <= value <= high:
            return 100.0
        elif value < low:
            score = (value - (low - span)) / span * 100
        else:
            score = ((high + span) - value) / span * 100

    return float(np.clip(score, 0, 100))


def render_score_bar(label, score, note, threshold_type="both", data_value=None, data_label="value"):
    if score is None:
        st.markdown(f"**{label}** — *data not available*")
        return

    if score >= 60:
        bar_color = "#2ecc71"
        text_color = "#1a5e35"
    elif score >= 40:
        bar_color = "#f39c12"
        text_color = "#7d4e00"
    else:
        bar_color = "#e74c3c"
        text_color = "#6e1a1a"

    bar_pct = score

    raw_display = ""
    if data_value is not None:
        raw_display = f"<span style='font-size:12px; color:#888;'>({data_label}: {data_value:+.3f})</span>"

    badge_styles = {
        "low":  ("⬇ low threshold",  "#d4edff", "#0066aa"),
        "high": ("⬆ high threshold", "#fde8e8", "#aa0000"),
        "both": ("↕ both thresholds", "#f0e8fd", "#6600aa"),
    }
    badge_text, badge_bg, badge_fg = badge_styles.get(
        threshold_type, ("threshold", "#eee", "#333")
    )
    badge_html = (
        f"<span style='font-size:10px; background:{badge_bg}; color:{badge_fg}; "
        f"border-radius:4px; padding:1px 5px; margin-left:6px; "
        f"font-weight:600; vertical-align:middle;'>{badge_text}</span>"
    )

    st.markdown(
        f"""
        <div style="margin-bottom: 10px;">
          <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:3px;">
            <span style="font-weight:600; font-size:14px;">{label}{badge_html}</span>
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
# HELPER FUNCTIONS
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
# MODULE 1 — BONE TAB
# ============================================================

def render_bone_tab(crew_id):
    st.title("🦴 Bone Density Loss Inhibitor Efficacy")
    st.write(
        "Each biomarker is scored 0–100 based on calibrated thresholds. "
        "The **Total Efficacy Score** is a weighted average across all biomarkers. "
        "**Green bars** indicate a protective/efficacious signal; "
        "**red bars** indicate bone-loss risk or insufficient drug effect. "
        "Threshold badges show whether each biomarker is penalized at its low end, "
        "high end, or both extremes."
    )

    # PROTEOMICS
    prot_map = {
        "BGLAP (Osteocalcin)":             get_logfc(pp, 'BGLAP'),
        "SPARC (Osteonectin)":             get_logfc(pp, 'SPARC'),
        "SPP1 (Osteopontin — proteomics)": get_logfc(pp, 'SPP1'),
        "SOST (Sclerostin)":               get_logfc(pp, 'SOST'),
        "POSTN (Periostin)":               get_logfc(pp, 'POSTN'),
        "BGN (Biglycan)":                  get_logfc(pp, 'BGN'),
        "DCN (Decorin)":                   get_logfc(pp, 'DCN'),
        "COL1A1 (Collagen I α1)":          get_logfc(pp, 'COL1A1'),
        "COL1A2 (Collagen I α2)":          get_logfc(pp, 'COL1A2'),
        "SFRP2 (Wnt modulator)":           get_logfc(pp, 'SFRP2'),
        "SFRP4 (Wnt modulator)":           get_logfc(pp, 'SFRP4'),
        "MGP (Matrix Gla Protein)":        get_logfc(pp, 'MGP'),
        "ADIPOQ (Adiponectin)":            get_logfc(pp, 'ADIPOQ'),
    }

    # CMP
    ca = get_cmp_per_crew(cmp, 'calcium_value_milligram_per_deciliter', crew_id)
    ap = get_cmp_per_crew(cmp, 'alkaline_phosphatase_value_units_per_liter', crew_id)

    def post_pre_ratio(tps_dict):
        pre  = [v for k, v in tps_dict.items() if k.startswith('L') and v is not None]
        post = [v for k, v in tps_dict.items() if k.startswith('R') and v is not None]
        if pre and post and np.mean(pre) != 0:
            return np.mean(post) / np.mean(pre)
        return None

    cmp_map = {
        "Calcium (CMP ratio)":              post_pre_ratio(ca),
        "Alkaline Phosphatase (CMP ratio)": post_pre_ratio(ap),
    }

    # URINE
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
        "Vitamin D2 (Ergocalciferol)": get_met_logfc(met, 'Ergocalciferol'),
        "Cortisol (metabolomics)":      get_met_logfc(met, 'Cortisol'),
        "Proline":                      get_met_logfc(met, 'Proline'),
        "Glycine":                      get_met_logfc(met, 'Glycine'),
        "Lysine":                       get_met_logfc(met, 'Lysine'),
        "Citric Acid":                  get_met_logfc(met, 'Citric Acid'),
    }

    all_raw = {**prot_map, **cmp_map, **urine_map, **met_map}

    scores = {}
    for name, params in BONE_BIOMARKER_PARAMS.items():
        raw = all_raw.get(name)
        scores[name] = score_biomarker(
            raw,
            params["low"],
            params["high"],
            params["higher_is_better"],
            params.get("threshold_type", "both"),
        )

    total_weight = 0.0
    weighted_sum = 0.0
    for name, params in BONE_BIOMARKER_PARAMS.items():
        s = scores.get(name)
        if s is not None:
            weighted_sum += s * params["weight"]
            total_weight += params["weight"]

    total_score = (weighted_sum / total_weight) if total_weight > 0 else 50.0

    render_total_score_bar(total_score)

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
                    threshold_type=params.get("threshold_type", "both"),
                    data_value=raw_val,
                    data_label=val_label,
                )
                any_data = True
            if not any_data:
                st.write("*No data available for this section.*")


# ============================================================
# MODULE 2 — CARDIOTOXICITY SAFETY
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
# MODULE 3 — NEUROLOGICAL RESILIENCE
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
# UI HELPERS
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
# SIDEBAR — CREW MEMBER SELECTOR (colored buttons)
# ============================================================
st.sidebar.title("Torchlight Health")
st.sidebar.markdown("---")
st.sidebar.markdown("### Select Crew Member")

# Inject CSS for the colored crew buttons
st.sidebar.markdown(
    """
    <style>
    div[data-testid="stSidebar"] .crew-btn-row {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Render one button per crew member; highlight the active one with a border/opacity change
for crew_id, cfg in CREW_CONFIG.items():
    is_active = st.session_state.selected_crew == crew_id
    border = "3px solid #fff" if is_active else "3px solid transparent"
    opacity = "1.0" if is_active else "0.65"
    checkmark = " ✓" if is_active else ""

    # Use st.button but wrap in styled HTML via markdown before it for spacing
    btn_label = f"{cfg['label']}{checkmark}"

    # We style the Streamlit button by injecting a scoped CSS class keyed to the crew id
    btn_key = f"crew_btn_{crew_id}"
    st.sidebar.markdown(
        f"""
        <style>
        div[data-testid="stSidebar"] div:has(> div > button[kind="secondary"]#btn_{crew_id}) button {{
            background-color: {cfg['color']} !important;
            color: {cfg['text']} !important;
            border: {border} !important;
            opacity: {opacity};
            font-weight: {'800' if is_active else '500'};
            width: 100%;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    clicked = st.sidebar.button(
        btn_label,
        key=btn_key,
        use_container_width=True,
        type="secondary",
    )
    if clicked:
        st.session_state.selected_crew = crew_id
        st.rerun()

# Apply per-button color via nth-child targeting (more reliable across Streamlit versions)
# Build one combined style block for all 4 buttons
button_styles = ""
for i, (crew_id, cfg) in enumerate(CREW_CONFIG.items(), start=1):
    is_active = st.session_state.selected_crew == crew_id
    border = "3px solid #ffffff" if is_active else "3px solid rgba(255,255,255,0.3)"
    opacity = "1.0" if is_active else "0.7"
    font_weight = "800" if is_active else "500"
    button_styles += f"""
    div[data-testid="stSidebar"] div[data-testid="stVerticalBlock"]
      > div:nth-child({i}) button {{
        background-color: {cfg['color']} !important;
        color: {cfg['text']} !important;
        border: {border} !important;
        opacity: {opacity} !important;
        font-weight: {font_weight} !important;
        border-radius: 8px !important;
        transition: all 0.15s ease !important;
    }}
    div[data-testid="stSidebar"] div[data-testid="stVerticalBlock"]
      > div:nth-child({i}) button:hover {{
        background-color: {cfg['hover']} !important;
        opacity: 1.0 !important;
    }}
    """

st.sidebar.markdown(f"<style>{button_styles}</style>", unsafe_allow_html=True)

# Show currently selected crew info
selected_cfg = CREW_CONFIG[st.session_state.selected_crew]
st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div style="
        background-color: {selected_cfg['color']};
        color: {selected_cfg['text']};
        padding: 10px 14px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 15px;
        text-align: center;
        margin-top: 4px;
    ">
        📡 Viewing: {selected_cfg['label']}<br>
        <span style="font-size:12px; font-weight:400; opacity:0.9;">ID: {st.session_state.selected_crew}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

if not DATA_LOADED:
    st.sidebar.markdown("---")
    st.sidebar.error(f"⚠️ Could not load CSV data from:\n`{DATA_DIR}`\n\nError: {DATA_ERROR}")
    st.sidebar.info("Adjust `DATA_DIR` at the top of `app.py` to point to your `data/processed/` folder.")

# Active crew for this render cycle
crew = st.session_state.selected_crew


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
            st.caption(f"Data source: 9 cardiac cytokine markers (Eve) · 3 proteomics targets — {selected_cfg['label']} ({crew})")

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
                f"6 metabolomics targets — {selected_cfg['label']} ({crew})"
            )

    for section, vals in biomarkers.items():
        with st.expander(section):
            st.json(vals)
