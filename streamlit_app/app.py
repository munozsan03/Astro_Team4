import streamlit as st
import pandas as pd
import numpy as np
import os

# ============================================================
# FONT SIZE LIBRARY
# Edit any value here to change that font size across the app.
# ============================================================
FONT_SIZES = {
    # ── Global / base ─────────────────────────────────────
    "base":                     "16px",   # Root body / default text

    # ── Page headings ─────────────────────────────────────
    "heading_h1":               "72px",   # st.title() / <h1>
    # Bone Density Loss Inhibitor Efficacy
    "heading_h2":               "22px",   # Section headings / <h2>4
    # Unused?
    "heading_h3":               "48px",   # Sub-section headings / <h3>
    # Proteomics (logFC)

    # ── Sidebar ───────────────────────────────────────────
    "sidebar_body":             "24px",   # General sidebar text
    # Done Density Loss, Cardiotoxicity Safety selctor
    "sidebar_heading":          "32px",   # Sidebar h1/h2/h3
    # View Module
    "sidebar_active_crew":      "15px",   # Active-crew badge label
    # Unused?
    "sidebar_active_crew_sub":  "12px",   # Active-crew badge sub-line (ID)
    # Unused?

    # ── Crew selector buttons ──────────────────────────────
    "crew_selector_heading":    "48px",   # "Select Crew Member" label
    # Select Crew Member label
    "crew_button":              "15px",   # Crew selector button text
    # Unused?

    # ── Crew info card ─────────────────────────────────────
    "crew_card_name":           "24px",   # Crew member name
    # Crew Member 1
    "crew_card_id":             "18px",   # "(ID: C001)" label
    # ID: C001
    "crew_card_demographics":   "18px",   # Age / Sex line
    # Age: 43
    "crew_card_bio":            "18px",   # Bio paragraph
    # Mission Command.

    # ── Tab / radio labels ────────────────────────────────
    "tab_label":                "15px",   # Tab button text
    # Unused?
    "radio_label":              "15px",   # Sidebar radio options
    # Unused?

    # ── Score bar — label row ─────────────────────────────
    "score_bar_label":          "32px",   # Biomarker name
    # BGLAP (Osteocalcin)
    "score_bar_score":          "32px",   # "XX.X/100" number
    # 100.0/100
    "score_bar_raw_value":      "24px",   # "(logFC: +0.123)" inline note
    # (logFC: -0.001)

    # ── Score bar — badge chips ───────────────────────────
    "score_bar_badge":          "24px",   # "⬆ high threshold" chip
    # low threshold
    "score_bar_avg_tag":        "24px",   # "⚠️ group avg" chip
    # group avg

    # ── Score bar — sub-text beneath the bar ─────────────
    "score_bar_note":           "18px",   # Italic explanatory note
    # Primary osteoblast-secreted bone ...

    # ── Neuro score bar extras ────────────────────────────
    "neuro_crew_ref":           "16px",   # "📊 Crew mean = …" line
    # Shared value across crew (in Neuro section only)

    # ── Total score summary card ──────────────────────────
    "total_score_heading":      "64px",   # "Total Score" label
    # Total score
    "total_score_number":       "48px",   # Big score number
    # 99.8/100
    "total_score_verdict":      "32px",   # "✅ Drug Efficacy Signal: POSITIVE"
    # Drug Efficacy Signal: ...
    "total_score_footnote":     "24px",   # Weighted composite footnote
    # Weighted composite across ...

    # ── Warning / alert banners ───────────────────────────
    "warning_banner":           "15px",   # st.warning() text
    # Unused?
    "averaged_warning":         "32px",   # ⚠️ "group avg" section banner
    # Data averaged across all crew members
    "alert_text":               "28px",   # Generic [data-testid="stAlert"] text
    # Dataset Notice: The current cohort ...

    # ── "Data not available" fallback line ────────────────
    "unavailable_label":        "64px",   # "biomarker — data not available"
    # BDNF urine ratio, data not available (Neuro only)
}


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="Astronaut Therapeutic Testing", layout="wide")

# ============================================================
# GLOBAL TYPOGRAPHY & COLOR OVERRIDES
# ============================================================
st.markdown(
    f"""
    <style>
    /* ── Force light background + dark text everywhere ─── */
    html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"] {{
        background-color: #f2f4f7 !important;
        color: #111111 !important;
        font-size: {FONT_SIZES["base"]} !important;
    }}

    /* Main content block */
    [data-testid="stMainBlockContainer"],
    [data-testid="block-container"],
    .main .block-container {{
        background-color: #f2f4f7 !important;
    }}

    /* ── White card behind every vertical block ───────── */
    [data-testid="stVerticalBlock"],
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: #ffffff !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        margin-bottom: 8px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
    }}

    /* ── Expander ─────────────────────────────────────── */
    [data-testid="stExpander"] {{
        background: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #e0e3e8 !important;
        margin-bottom: 10px !important;
    }}
    [data-testid="stExpander"] summary {{
        background: #ffffff !important;
        border-radius: 12px !important;
    }}
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {{
        color: #111111 !important;
        font-size: {FONT_SIZES["heading_h3"]} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stExpander"] [data-testid="stVerticalBlock"] {{
        background: #ffffff !important;
        box-shadow: none !important;
        padding: 8px 4px !important;
    }}

    /* ── All text elements → dark ─────────────────────── */
    p, span, div, label, li, td, th, h1, h2, h3, h4, h5, h6,
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] div,
    [data-testid="stMarkdownContainer"] span {{
        color: #111111 !important;
    }}

    h1 {{ font-size: {FONT_SIZES["heading_h1"]} !important; font-weight: 800 !important; }}
    h2 {{ font-size: {FONT_SIZES["heading_h2"]} !important; font-weight: 700 !important; }}
    h3 {{ font-size: {FONT_SIZES["heading_h3"]} !important; font-weight: 700 !important; }}

    /* ── Alert / warning banners ──────────────────────── */
    [data-testid="stAlert"] {{
        background: #fffbeb !important;
        border-color: #f59e0b !important;
        border-radius: 10px !important;
    }}
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div {{
        color: #7d4e00 !important;
        font-size: {FONT_SIZES["alert_text"]} !important;
        font-weight: 600 !important;
    }}

    /* ── Sidebar ──────────────────────────────────────── */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div {{
        background-color: #1a1d2e !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #e8e8e8 !important;
        font-size: {FONT_SIZES["sidebar_body"]} !important;
    }}
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: #111111 !important;
        font-size: {FONT_SIZES["sidebar_heading"]} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stRadio"] label {{
        font-size: {FONT_SIZES["radio_label"]} !important;
        font-weight: 600 !important;
        color: #111111 !important;
    }}

    /* ── Tab labels ───────────────────────────────────── */
    button[data-baseweb="tab"] p {{
        font-size: {FONT_SIZES["tab_label"]} !important;
        font-weight: 600 !important;
        color: #111111 !important;
    }}

    /* ── Custom inline background cards ── */
    div[style*="background:#f8f9fc"],
    div[style*="background: #f8f9fc"],
    div[style*="background:#f0f2f6"],
    div[style*="background: #f0f2f6"],
    div[style*="background:#f8f8f8"],
    div[style*="background: #f8f8f8"] {{
        background: #ffffff !important;
        color: #111111 !important;
    }}

    /* ── Warning card (yellow) ────────────────────────── */
    div[style*="background:#fff3cd"],
    div[style*="background: #fff3cd"] {{
        background: #fff8e1 !important;
        color: #7d4e00 !important;
        border-color: #f59e0b !important;
    }}

    div[style*="background:#f8f8f8"] {{
        background: #ffffff !important;
    }}

    /* ── Metric / number text ─────────────────────────── */
    [data-testid="stMetric"] * {{
        color: #111111 !important;
    }}

    /* ── Remove any dark overlay on main area ─────────── */
    [data-theme="dark"] .stApp,
    [data-theme="dark"] [data-testid="stAppViewContainer"],
    [data-theme="dark"] [data-testid="stMainBlockContainer"],
    [data-theme="dark"] .main .block-container {{
        background-color: #f2f4f7 !important;
    }}
    [data-theme="dark"] [data-testid="stVerticalBlock"],
    [data-theme="dark"] [data-testid="stVerticalBlockBorderWrapper"],
    [data-theme="dark"] [data-testid="stExpander"],
    [data-theme="dark"] [data-testid="stExpander"] summary,
    [data-theme="dark"] [data-testid="stExpander"] [data-testid="stVerticalBlock"] {{
        background: #ffffff !important;
        color: #111111 !important;
    }}
    [data-theme="dark"] p,
    [data-theme="dark"] span,
    [data-theme="dark"] div,
    [data-theme="dark"] label,
    [data-theme="dark"] h1,
    [data-theme="dark"] h2,
    [data-theme="dark"] h3,
    [data-theme="dark"] .stMarkdown p,
    [data-theme="dark"] .stMarkdown div,
    [data-theme="dark"] [data-testid="stMarkdownContainer"] p,
    [data-theme="dark"] [data-testid="stMarkdownContainer"] div,
    [data-theme="dark"] [data-testid="stMarkdownContainer"] span {{
        color: #111111 !important;
    }}
    [data-theme="dark"] [data-testid="stAlert"] p,
    [data-theme="dark"] [data-testid="stAlert"] div,
    [data-theme="dark"] [data-testid="stAlert"] span {{
        color: #7d4e00 !important;
    }}
    /* Dark mode sidebar stays dark */
    [data-theme="dark"] [data-testid="stSidebar"],
    [data-theme="dark"] [data-testid="stSidebar"] > div {{
        background-color: #1a1d2e !important;
    }}
    [data-theme="dark"] [data-testid="stSidebar"] * {{
        color: #e8e8e8 !important;
    }}
    [data-theme="dark"] [data-testid="stSidebar"] h1,
    [data-theme="dark"] [data-testid="stSidebar"] h2,
    [data-theme="dark"] [data-testid="stSidebar"] h3 {{
        color: #111111 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATA LOADING
# ============================================================
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

@st.cache_data
def load_data():
    pp    = pd.read_csv(os.path.join(DATA_DIR, "plasma_proteomics.csv"))
    met   = pd.read_csv(os.path.join(DATA_DIR, "plasma_metabolomics.csv"))
    cmp   = pd.read_csv(os.path.join(DATA_DIR, "cmp_metabolic_panel.csv"))
    card  = pd.read_csv(os.path.join(DATA_DIR, "cardiac_cytokines_eve.csv"))
    urine = pd.read_csv(os.path.join(DATA_DIR, "urine_inflammation_panel.csv"))
    return pp, met, cmp, card, urine

try:
    pp, met, cmp, card, urine = load_data()
    DATA_LOADED = True
except Exception as e:
    DATA_LOADED = False
    DATA_ERROR = str(e)

# ============================================================
# CREW CONFIGURATION
# ============================================================
CREW_CONFIG = {
    "C001": {
        "label": "Crew Member 1",
        "color": "#3b82f6", "hover": "#2563eb", "text": "#ffffff",
        "age": 43, "sex": "Male",
        "bio": (
            "Mission Command. "
            "Current NASA Administrator."
        ),
        "photo": "crew_C001.png",
    },
    "C002": {
        "label": "Crew Member 2",
        "color": "#10b981", "hover": "#059669", "text": "#ffffff",
        "age": 34, "sex": "Female",
        "bio": (
            "Medical Officer. "
            "Physician Assistant at St. Jude's."
        ),
        "photo": "crew_C002.png",
    },
    "C003": {
        "label": "Crew Member 3",
        "color": "#f59e0b", "hover": "#d97706", "text": "#ffffff",
        "age": 56, "sex": "Female",
        "bio": (
            "Pilot. "
            "Professor (PhD), Envoy for the State Department."
        ),
        "photo": "crew_C003.png",
    },
    "C004": {
        "label": "Crew Member 4",
        "color": "#ef4444", "hover": "#dc2626", "text": "#ffffff",
        "age": 29, "sex": "Male",
        "bio": (
            "Misison Specialist. "
            "Data Engineer, Air Force Veteran."
        ),
        "photo": "crew_C004.png",
    },
}

# ============================================================
# SESSION STATE — crew selection
# ============================================================
if "selected_crew" not in st.session_state:
    st.session_state.selected_crew = "C001"


# ============================================================
# DATASETS THAT ARE AVERAGED (no per-crew differentiation)
# ============================================================
AVERAGED_DATASETS_NOTE = (
    "⚠️ <b>Data averaged across all crew members</b> — "
    "values shown here are group-level averages and do <b>not</b> change between crew members. "
    "Per-individual proteomics/metabolomics were not available in this dataset."
)


# ============================================================
# BONE EFFICACY PARAMETERS
# ============================================================
BONE_BIOMARKER_PARAMS = {
    "BGLAP (Osteocalcin)": {
        "low": -0.5, "high": 2.0, "weight": 8, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Primary osteoblast-secreted bone matrix protein. Upregulation signals active bone formation. Only penalized when logFC drops below -0.5.",
        "averaged": True,
    },
    "SPARC (Osteonectin)": {
        "low": -0.5, "high": 2.0, "weight": 6, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Bone mineralization scaffolding protein. Higher expression supports matrix deposition. Only penalized when logFC drops below -0.5.",
        "averaged": True,
    },
    "SPP1 (Osteopontin — proteomics)": {
        "low": -2.0, "high": 0.75, "weight": 4, "higher_is_better": False,
        "threshold_type": "high",
        "note": "Osteopontin promotes osteoclast activity. Only penalized when logFC rises above +0.75.",
        "averaged": True,
    },
    "SOST (Sclerostin)": {
        "low": -2.0, "high": 0.5, "weight": 8, "higher_is_better": False,
        "threshold_type": "high",
        "note": "Sclerostin inhibits Wnt signaling and suppresses bone formation. Only penalized when logFC rises above +0.5.",
        "averaged": True,
    },
    "POSTN (Periostin)": {
        "low": -0.5, "high": 2.0, "weight": 5, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Periosteal bone formation marker. Only penalized when logFC drops below -0.5.",
        "averaged": True,
    },
    "BGN (Biglycan)": {
        "low": -0.75, "high": 2.0, "weight": 4, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Bone matrix proteoglycan regulating collagen fibrillogenesis. Only penalized when logFC drops below -0.75.",
        "averaged": True,
    },
    "DCN (Decorin)": {
        "low": -0.75, "high": 2.0, "weight": 3, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Collagen-binding proteoglycan supporting structural bone matrix. Only penalized when logFC drops below -0.75.",
        "averaged": True,
    },
    "COL1A1 (Collagen I α1)": {
        "low": -0.5, "high": 2.0, "weight": 7, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Primary structural collagen of bone. Only penalized when logFC drops below -0.5.",
        "averaged": True,
    },
    "COL1A2 (Collagen I α2)": {
        "low": -0.5, "high": 2.0, "weight": 5, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Partners with COL1A1 to form mature type-I collagen triple helix. Only penalized when logFC drops below -0.5.",
        "averaged": True,
    },
    "SFRP2 (Wnt modulator)": {
        "low": -1.0, "high": 1.5, "weight": 4, "higher_is_better": True,
        "threshold_type": "both",
        "note": "SFRP2 facilitates Wnt signaling in bone; mild upregulation is supportive but excessive dysregulation becomes inhibitory. Penalized below -1.0 and above +1.5.",
        "averaged": True,
    },
    "SFRP4 (Wnt modulator)": {
        "low": -2.0, "high": 0.5, "weight": 3, "higher_is_better": False,
        "threshold_type": "high",
        "note": "SFRP4 inhibits Wnt signaling and is associated with osteoporosis. Only penalized when logFC rises above +0.5.",
        "averaged": True,
    },
    "MGP (Matrix Gla Protein)": {
        "low": -2.0, "high": 0.75, "weight": 3, "higher_is_better": False,
        "threshold_type": "high",
        "note": "MGP inhibits mineralization when elevated. Only penalized when logFC rises above +0.75.",
        "averaged": True,
    },
    "ADIPOQ (Adiponectin)": {
        "low": -1.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "threshold_type": "both",
        "note": "Adiponectin promotes osteoblast differentiation. Moderate elevation is protective; penalized below -1.0 and above +2.0.",
        "averaged": True,
    },
    "Calcium (CMP ratio)": {
        "low": 0.90, "high": 1.10, "weight": 6, "higher_is_better": True,
        "threshold_type": "both",
        "note": "Serum calcium must stay balanced. Ratio < 0.90 suggests hypocalcemia; ratio > 1.10 may indicate hypercalcemia. Penalized at both extremes.",
        "averaged": False,
    },
    "Alkaline Phosphatase (CMP ratio)": {
        "low": 0.80, "high": 1.40, "weight": 5, "higher_is_better": True,
        "threshold_type": "both",
        "note": "Alk Phos reflects osteoblast activity. Modest elevation is favorable; ratio > 1.4 may indicate liver stress or excessive turnover; ratio < 0.80 suggests suppressed osteoblasts.",
        "averaged": False,
    },
    "RANKL (urine ratio)": {
        "low": 0.80, "high": 1.25, "weight": 7, "higher_is_better": False,
        "threshold_type": "high",
        "note": "RANKL drives osteoclastogenesis. Elevated post-flight ratio signals continued bone resorption stimulus. Only penalized when ratio rises above 1.25.",
        "averaged": False,
    },
    "RANK (urine ratio)": {
        "low": 0.80, "high": 1.25, "weight": 4, "higher_is_better": False,
        "threshold_type": "high",
        "note": "RANK receptor expression on osteoclast precursors. Only penalized when ratio rises above 1.25.",
        "averaged": False,
    },
    "BMP7 (urine ratio)": {
        "low": 0.90, "high": 2.0, "weight": 5, "higher_is_better": True,
        "threshold_type": "low",
        "note": "BMP7 promotes osteoblast differentiation. Higher post-flight ratio is protective. Only penalized when ratio drops below 0.90.",
        "averaged": False,
    },
    "WNT16 (urine ratio)": {
        "low": 0.90, "high": 2.0, "weight": 5, "higher_is_better": True,
        "threshold_type": "low",
        "note": "WNT16 suppresses osteoclastogenesis and supports cortical bone integrity. Only penalized when ratio drops below 0.90.",
        "averaged": False,
    },
    "FGF23 (urine ratio)": {
        "low": 0.80, "high": 1.20, "weight": 4, "higher_is_better": False,
        "threshold_type": "high",
        "note": "FGF23 inhibits Vitamin D activation and phosphate reabsorption. Only penalized when ratio rises above 1.20.",
        "averaged": False,
    },
    "IL-6 (urine ratio)": {
        "low": 0.80, "high": 1.30, "weight": 5, "higher_is_better": False,
        "threshold_type": "high",
        "note": "IL-6 activates osteoclasts and drives bone loss. Only penalized when ratio rises above 1.30.",
        "averaged": False,
    },
    "IL-17A (urine ratio)": {
        "low": 0.80, "high": 1.25, "weight": 4, "higher_is_better": False,
        "threshold_type": "high",
        "note": "IL-17A stimulates osteoclast differentiation and inflammatory bone loss. Only penalized when ratio rises above 1.25.",
        "averaged": False,
    },
    "TGF-β1 (urine ratio)": {
        "low": 0.80, "high": 1.60, "weight": 3, "higher_is_better": True,
        "threshold_type": "both",
        "note": "TGF-β1 is pleiotropic: modest elevation supports bone formation coupling, but very high levels can promote resorption/fibrosis imbalance. Penalized below 0.80 and above 1.60.",
        "averaged": False,
    },
    "Vitamin D2 (Ergocalciferol)": {
        "low": -0.5, "high": 2.0, "weight": 6, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Vitamin D is essential for calcium absorption and bone mineralization. Only penalized when logFC drops below -0.5.",
        "averaged": True,
    },
    "Cortisol (metabolomics)": {
        "low": -2.0, "high": 0.75, "weight": 5, "higher_is_better": False,
        "threshold_type": "high",
        "note": "Chronic cortisol elevation suppresses osteoblasts and promotes bone loss. Only penalized when logFC rises above +0.75.",
        "averaged": True,
    },
    "Proline": {
        "low": -1.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Proline is a primary amino acid in collagen. Only penalized when logFC drops below -1.0.",
        "averaged": True,
    },
    "Glycine": {
        "low": -1.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Glycine is the most abundant amino acid in collagen. Only penalized when logFC drops below -1.0.",
        "averaged": True,
    },
    "Lysine": {
        "low": -1.0, "high": 2.0, "weight": 3, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Lysine is essential for collagen cross-linking. Only penalized when logFC drops below -1.0.",
        "averaged": True,
    },
    "Citric Acid": {
        "low": -1.0, "high": 2.0, "weight": 2, "higher_is_better": True,
        "threshold_type": "low",
        "note": "Citrate is incorporated into bone mineral crystals. Only penalized when logFC drops below -1.0.",
        "averaged": True,
    },
}


# ============================================================
# NEURO RESILIENCE PARAMETERS
# ============================================================
NEURO_BIOMARKER_PARAMS = {
    "BDNF (Brain-Derived Neurotrophic Factor)": {
        "weight": 8, "higher_is_better": True, "threshold_type": "low",
        "averaged": True,
        "note": (
            "BDNF is the primary neuroprotective growth factor, supporting neuronal survival, "
            "synaptic plasticity, and cognitive resilience. Suppression during spaceflight indicates "
            "impaired neurotrophin signaling. Scored against crew average: penalized when logFC falls "
            "more than 1 SD below the crew mean."
        ),
    },
    "S100B (Astrocyte Damage Marker)": {
        "weight": 7, "higher_is_better": False, "threshold_type": "high",
        "averaged": True,
        "note": (
            "S100B is released by astrocytes upon cellular stress or damage, indicating neuroglial "
            "injury and blood-brain barrier disruption. Scored against crew average: penalized when "
            "logFC rises more than 1 SD above the crew mean."
        ),
    },
    "NRGN (Neurogranin — Synaptic Marker)": {
        "weight": 6, "higher_is_better": False, "threshold_type": "high",
        "averaged": True,
        "note": (
            "Neurogranin is released from dendritic spines during synaptic damage. Elevated plasma "
            "neurogranin indicates loss of synaptic integrity. Scored against crew average: penalized "
            "when logFC rises more than 1 SD above the crew mean."
        ),
    },
    "CLU (Clusterin — Neuroprotective Chaperone)": {
        "weight": 4, "higher_is_better": True, "threshold_type": "low",
        "averaged": True,
        "note": (
            "Clusterin clears misfolded proteins and supports neuronal survival under stress. Mild "
            "upregulation is a neuroprotective compensatory response. Scored against crew average: "
            "penalized when logFC falls more than 1 SD below the crew mean."
        ),
    },
    "APOE (Apolipoprotein E — CNS Lipid Transport)": {
        "weight": 4, "higher_is_better": True, "threshold_type": "both",
        "averaged": True,
        "note": (
            "APOE mediates lipid transport and synaptic membrane repair. Moderate upregulation is "
            "beneficial; excessive dysregulation in either direction reflects abnormal lipid metabolism. "
            "Scored against crew average: penalized when logFC deviates more than 1 SD in either "
            "direction from the crew mean."
        ),
    },
    "BDNF (urine ratio)": {
        "weight": 7, "higher_is_better": True, "threshold_type": "low",
        "averaged": False,
        "note": (
            "Urinary BDNF reflects ongoing neurotrophin secretion. A maintained or elevated post-flight "
            "ratio indicates a preserved neurotrophic response. Scored against crew average: penalized "
            "when ratio falls more than 1 SD below the crew mean."
        ),
    },
    "GFAP (Glial Fibrillary Acidic Protein — urine ratio)": {
        "weight": 6, "higher_is_better": False, "threshold_type": "high",
        "averaged": False,
        "note": (
            "GFAP is released by reactive astrocytes following CNS injury or neuroinflammation. "
            "Elevated post-flight GFAP signals sustained glial activation. Scored against crew average: "
            "penalized when ratio rises more than 1 SD above the crew mean."
        ),
    },
    "NGF (Nerve Growth Factor — urine ratio)": {
        "weight": 5, "higher_is_better": True, "threshold_type": "low",
        "averaged": False,
        "note": (
            "NGF is essential for neuron survival and axonal maintenance. Higher post-flight NGF "
            "supports regenerative processes. Scored against crew average: penalized when ratio falls "
            "more than 1 SD below the crew mean."
        ),
    },
    "CXCL10 (IP-10 — Neuroinflammatory Chemokine — urine ratio)": {
        "weight": 5, "higher_is_better": False, "threshold_type": "high",
        "averaged": False,
        "note": (
            "CXCL10 drives neuroinflammatory T-cell recruitment and microglial activation. Elevated "
            "post-flight CXCL10 reflects ongoing CNS inflammatory signaling. Scored against crew "
            "average: penalized when ratio rises more than 1 SD above the crew mean."
        ),
    },
    "Kynurenine (Neuro-Inflammatory Pathway)": {
        "weight": 6, "higher_is_better": False, "threshold_type": "high",
        "averaged": True,
        "note": (
            "Kynurenine is a neurotoxic tryptophan catabolite that drives neuroinflammation. High "
            "kynurenine diverts tryptophan away from serotonin synthesis toward quinolinic acid, an "
            "excitotoxin. Scored against crew average: penalized when logFC rises more than 1 SD above "
            "the crew mean."
        ),
    },
    "Tryptophan (Serotonin Precursor)": {
        "weight": 5, "higher_is_better": True, "threshold_type": "low",
        "averaged": True,
        "note": (
            "Tryptophan is the sole precursor for serotonin and melatonin. Depletion indicates shunting "
            "toward the inflammatory kynurenine pathway and impaired mood/sleep neurochemistry. Scored "
            "against crew average: penalized when logFC falls more than 1 SD below the crew mean."
        ),
    },
    "5-HIAA (Serotonin Metabolite)": {
        "weight": 5, "higher_is_better": True, "threshold_type": "low",
        "averaged": True,
        "note": (
            "5-HIAA is the primary serotonin metabolite, reflecting active serotonergic "
            "neurotransmission. Suppressed 5-HIAA indicates reduced serotonin turnover and potential "
            "mood dysregulation. Scored against crew average: penalized when logFC falls more than 1 SD "
            "below the crew mean."
        ),
    },
    "Kynurenine:Tryptophan Ratio (K:T Ratio)": {
        "weight": 7, "higher_is_better": False, "threshold_type": "high",
        "averaged": True,
        "note": (
            "The K:T ratio is the gold-standard index of IDO1 enzyme activation and neuroinflammatory "
            "tryptophan shunting. An elevated ratio indicates preferential routing into the neurotoxic "
            "kynurenine pathway over serotonin synthesis. Scored against crew average: penalized when "
            "the ratio rises more than 1 SD above the crew mean."
        ),
    },
    "N-Acetylaspartic Acid (NAA — Neuronal Viability)": {
        "weight": 6, "higher_is_better": True, "threshold_type": "low",
        "averaged": True,
        "note": (
            "NAA is synthesized exclusively in neurons. Circulating NAA reduction reflects neuronal "
            "metabolic compromise and impaired mitochondrial function. Scored against crew average: "
            "penalized when logFC falls more than 1 SD below the crew mean."
        ),
    },
    "Cortisol (Neuro — HPA Axis Activation)": {
        "weight": 6, "higher_is_better": False, "threshold_type": "high",
        "averaged": True,
        "note": (
            "Chronic HPA axis activation suppresses hippocampal neurogenesis, impairs synaptic "
            "plasticity, and downregulates BDNF. Elevated flight cortisol is a key driver of "
            "spaceflight-associated neuro-cognitive risk. Scored against crew average: penalized when "
            "logFC rises more than 1 SD above the crew mean."
        ),
    },
    "Nicotinamide (NAD+ Precursor — Neuroprotection)": {
        "weight": 4, "higher_is_better": True, "threshold_type": "low",
        "averaged": True,
        "note": (
            "Nicotinamide supports NAD+ biosynthesis, essential for neuronal energy metabolism, DNA "
            "repair, and sirtuin-mediated neuroprotection. Depletion indicates impaired NAD+ "
            "availability under metabolic stress. Scored against crew average: penalized when logFC "
            "falls more than 1 SD below the crew mean."
        ),
    },
}


# ============================================================
# CARDIOTOXICITY PARAMETERS
# ============================================================
CARDIO_BIOMARKER_PARAMS = {
    "CRP (C-Reactive Protein)": {
        "low": 1.0, "high": 1.5, "weight": 15,
        "threshold_type": "high", "averaged": False,
        "note": (
            "Canonical systemic inflammation marker directly linked to endothelial dysfunction "
            "and cardiovascular risk. A post/pre ratio above 1.5 (50% elevation) represents "
            "clinically meaningful persistent inflammation. Weight 15 — highest priority marker."
        ),
    },
    "PF4 (Platelet Factor 4)": {
        "low": 1.0, "high": 1.5, "weight": 15,
        "threshold_type": "high", "averaged": False,
        "note": (
            "Platelet activation marker directly linked to thrombotic activity and clotting potential. "
            "PF4 elevation during spaceflight indicates platelet hyper-reactivity and elevated "
            "thromboembolism risk. Weight 15 — co-primary marker alongside CRP."
        ),
    },
    "Fibrinogen": {
        "low": 1.0, "high": 1.5, "weight": 12,
        "threshold_type": "high", "averaged": False,
        "note": (
            "Coagulation-associated acute phase protein. Elevated fibrinogen increases blood viscosity "
            "and thrombosis risk, compounding cardiovascular strain in microgravity. "
            "Ratio above 1.5 reflects sustained coagulation activation."
        ),
    },
    "Fetuin-A": {
        "low": 0.75, "high": 1.30, "weight": 12,
        "threshold_type": "both", "averaged": False,
        "note": (
            "Modulates vascular calcification and metabolic regulation. Both depletion (loss of "
            "calcification inhibition, risk of vascular mineralization) and elevation (impaired "
            "insulin signaling, metabolic cardiovascular stress) are concerning. "
            "Penalized when ratio falls below 0.75 or rises above 1.30."
        ),
    },
    "Haptoglobin": {
        "low": 1.0, "high": 1.5, "weight": 10,
        "threshold_type": "high", "averaged": False,
        "note": (
            "Hemoglobin scavenging protein reflecting oxidative vascular stress and radiation "
            "response. Elevated haptoglobin post-flight indicates increased hemolysis and "
            "oxidative burden on the vascular endothelium."
        ),
    },
    "L-Selectin (CD62L)": {
        "low": 0.70, "high": 1.40, "weight": 10,
        "threshold_type": "both", "averaged": False,
        "note": (
            "Regulates leukocyte adhesion and immune-endothelial activation. Both shedding "
            "(loss of immune surveillance, ratio < 0.70) and excessive upregulation "
            "(systemic endothelial activation, ratio > 1.40) indicate vascular dysfunction. "
            "Penalized at both extremes."
        ),
    },
    "SAP (Serum Amyloid P Component)": {
        "low": 1.0, "high": 1.5, "weight": 10,
        "threshold_type": "high", "averaged": False,
        "note": (
            "Reflects persistent systemic inflammatory burden and tissue remodeling activity. "
            "Elevated SAP is associated with chronic inflammation and extracellular matrix "
            "pathology relevant to vascular wall integrity."
        ),
    },
    "Alpha-2-Macroglobulin (A2M)": {
        "low": 0.75, "high": 1.40, "weight": 8,
        "threshold_type": "both", "averaged": False,
        "note": (
            "Regulates protease activity across multiple vascular and inflammatory cascades. "
            "Both suppression (unregulated protease activity, endothelial degradation) and "
            "excessive elevation (impaired protease clearance, chronic signaling dysregulation) "
            "negatively affect vascular homeostasis. Penalized at both extremes."
        ),
    },
    "AGP (Alpha-1-Acid Glycoprotein)": {
        "low": 1.0, "high": 1.5, "weight": 8,
        "threshold_type": "high", "averaged": False,
        "note": (
            "Correlates with chronic systemic inflammation and cardiovascular risk. AGP is an "
            "acute phase reactant that rises with sustained inflammatory activation, indicating "
            "ongoing vascular and immune stress."
        ),
    },
    "VWF (Von Willebrand Factor — proteomics)": {
        "low": -2.0, "high": 0.75, "weight": 9,
        "threshold_type": "high", "averaged": True,
        "note": (
            "VWF is a key mediator of platelet adhesion and endothelial stress response. "
            "Elevated VWF logFC reflects endothelial activation and dysfunction, directly "
            "increasing thrombosis risk. Only penalized when logFC rises above +0.75."
        ),
    },
    "SERPINE1 / PAI-1 (Fibrinolysis Inhibitor — proteomics)": {
        "low": -2.0, "high": 0.75, "weight": 7,
        "threshold_type": "high", "averaged": True,
        "note": (
            "PAI-1 is the primary inhibitor of fibrinolysis (clot dissolution). Elevated "
            "SERPINE1 logFC means clots are less efficiently cleared, increasing risk of "
            "sustained thrombosis and cardiovascular events. Only penalized when logFC rises above +0.75."
        ),
    },
}


# ============================================================
# SCORE ENGINES
# ============================================================

def score_biomarker(value, low, high, higher_is_better, threshold_type="both"):
    if value is None:
        return None
    span = max(high - low, 1e-9)

    if threshold_type == "low":
        if value >= low:
            return 100.0
        return float(np.clip((value - (low - span)) / span * 100, 0, 100))

    elif threshold_type == "high":
        if value <= high:
            return 100.0
        return float(np.clip(((high + span) - value) / span * 100, 0, 100))

    else:  # "both"
        if low <= value <= high:
            return 100.0
        elif value < low:
            return float(np.clip((value - (low - span)) / span * 100, 0, 100))
        else:
            return float(np.clip(((high + span) - value) / span * 100, 0, 100))


def score_cardio_biomarker(value, low, high, threshold_type="high"):
    if value is None:
        return None
    span = max(high - low, 1e-9)

    if threshold_type == "high":
        if value <= low:
            return 0.0
        elif value >= high:
            return 100.0
        return float((value - low) / span * 100)

    elif threshold_type == "low":
        if value >= high:
            return 0.0
        elif value <= low:
            return 100.0
        return float((high - value) / span * 100)

    else:  # "both"
        if low <= value <= high:
            return 0.0
        elif value < low:
            return float(np.clip((low - value) / span * 100, 0, 100))
        else:
            return float(np.clip((value - high) / span * 100, 0, 100))


# ============================================================
# RENDER HELPERS
# ============================================================

def _averaged_warning_html():
    return (
        f"<div style='background:#fff8e1; border:2px solid #f59e0b; border-radius:8px; "
        f"padding:10px 14px; margin:10px 0 14px 0; font-size:{FONT_SIZES['averaged_warning']}; "
        f"color:#7d4e00; font-weight:600;'>"
        f"⚠️ <b>Data averaged across all crew members</b> — values in this section are "
        f"group-level averages from <code>plasma_proteomics.csv</code> or "
        f"<code>plasma_metabolomics.csv</code> and do <b>not</b> change between crew members."
        f"</div>"
    )


def render_score_bar(label, score, note, threshold_type="both", data_value=None,
                     data_label="value", is_averaged=False):
    if score is None:
        st.markdown(
            f"<div style='font-size:{FONT_SIZES['unavailable_label']}; color:#555555; margin-bottom:8px;'>"
            f"<b>{label}</b> — <i>data not available</i></div>",
            unsafe_allow_html=True,
        )
        return

    if score >= 60:
        bar_color, text_color = "#1db954", "#0a4522"
    elif score >= 40:
        bar_color, text_color = "#f59e0b", "#5c3800"
    else:
        bar_color, text_color = "#dc2626", "#5c0a0a"

    raw_display = ""
    if data_value is not None:
        raw_display = (
            f"<span style='font-size:{FONT_SIZES['score_bar_raw_value']}; "
            f"color:#444444; font-weight:500;'>"
            f"({data_label}: {data_value:+.3f})</span>"
        )

    badge_styles = {
        "low":  ("⬇ low threshold",   "#cce5ff", "#003d7a"),
        "high": ("⬆ high threshold",  "#ffd5d9", "#6b0a12"),
        "both": ("↕ both thresholds", "#e8d5f7", "#3d0070"),
    }
    badge_text, badge_bg, badge_fg = badge_styles.get(threshold_type, ("threshold", "#eeeeee", "#333333"))
    badge_html = (
        f"<span style='font-size:{FONT_SIZES['score_bar_badge']}; background:{badge_bg}; "
        f"color:{badge_fg}; border-radius:4px; padding:2px 6px; margin-left:6px; "
        f"font-weight:700; vertical-align:middle;'>{badge_text}</span>"
    )

    avg_tag = ""
    if is_averaged:
        avg_tag = (
            f"<span style='font-size:{FONT_SIZES['score_bar_avg_tag']}; background:#fff8e1; "
            f"color:#7d4e00; border-radius:4px; padding:2px 6px; margin-left:6px; "
            f"font-weight:700; vertical-align:middle;'>⚠️ group avg</span>"
        )

    st.markdown(
        f"""
        <div style="margin-bottom:12px; background:#ffffff; border-radius:8px; padding:10px 14px; border:1px solid #e8eaed;">
          <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
            <span style="font-weight:700; font-size:{FONT_SIZES['score_bar_label']}; color:#111111;">{label}{badge_html}{avg_tag}</span>
            <span style="font-weight:800; color:{text_color}; font-size:{FONT_SIZES['score_bar_score']};">
              {score:.1f}/100 &nbsp; {raw_display}
            </span>
          </div>
          <div style="background:#d8dce3; border-radius:6px; height:16px; width:100%;">
            <div style="background:{bar_color}; width:{score}%; height:16px; border-radius:6px; transition:width 0.4s;"></div>
          </div>
          <div style="font-size:{FONT_SIZES['score_bar_note']}; color:#444444; margin-top:3px; font-style:italic; line-height:1.5;">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_cardio_score_bar(label, score, note, threshold_type, data_value,
                             data_label, is_averaged=False):
    if score is None:
        st.markdown(
            f"<div style='font-size:{FONT_SIZES['unavailable_label']}; color:#555555; margin-bottom:8px;'>"
            f"<b>{label}</b> — <i>data not available</i></div>",
            unsafe_allow_html=True,
        )
        return

    if score < 35:
        bar_color, text_color = "#1db954", "#0a4522"
    elif score < 65:
        bar_color, text_color = "#f59e0b", "#5c3800"
    else:
        bar_color, text_color = "#dc2626", "#5c0a0a"

    raw_display = ""
    if data_value is not None:
        raw_display = (
            f"<span style='font-size:{FONT_SIZES['score_bar_raw_value']}; "
            f"color:#444444; font-weight:500;'>"
            f"({data_label}: {data_value:+.3f})</span>"
        )

    badge_styles = {
        "low":  ("⬇ low threshold",   "#cce5ff", "#003d7a"),
        "high": ("⬆ high threshold",  "#ffd5d9", "#6b0a12"),
        "both": ("↕ both thresholds", "#e8d5f7", "#3d0070"),
    }
    badge_text, badge_bg, badge_fg = badge_styles.get(threshold_type, ("threshold", "#eeeeee", "#333333"))
    badge_html = (
        f"<span style='font-size:{FONT_SIZES['score_bar_badge']}; background:{badge_bg}; "
        f"color:{badge_fg}; border-radius:4px; padding:2px 6px; margin-left:6px; "
        f"font-weight:700; vertical-align:middle;'>{badge_text}</span>"
    )

    avg_tag = ""
    if is_averaged:
        avg_tag = (
            f"<span style='font-size:{FONT_SIZES['score_bar_avg_tag']}; background:#fff8e1; "
            f"color:#7d4e00; border-radius:4px; padding:2px 6px; margin-left:6px; "
            f"font-weight:700; vertical-align:middle;'>⚠️ group avg</span>"
        )

    st.markdown(
        f"""
        <div style="margin-bottom:12px; background:#ffffff; border-radius:8px; padding:10px 14px; border:1px solid #e8eaed;">
          <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
            <span style="font-weight:700; font-size:{FONT_SIZES['score_bar_label']}; color:#111111;">{label}{badge_html}{avg_tag}</span>
            <span style="font-weight:800; color:{text_color}; font-size:{FONT_SIZES['score_bar_score']};">
              {score:.1f}/100 risk &nbsp; {raw_display}
            </span>
          </div>
          <div style="background:#d8dce3; border-radius:6px; height:16px; width:100%;">
            <div style="background:{bar_color}; width:{score}%; height:16px;
                        border-radius:6px; transition:width 0.4s;"></div>
          </div>
          <div style="font-size:{FONT_SIZES['score_bar_note']}; color:#444444; margin-top:3px; font-style:italic; line-height:1.5;">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_total_score_bar(score, n_biomarkers, domain_label="Drug Efficacy"):
    if score >= 60:
        bar_color, label_color = "#1db954", "#0a4522"
        verdict = f"✅ {domain_label} Signal: POSITIVE"
        verdict_color = "#0a4522"
    elif score >= 40:
        bar_color, label_color = "#f59e0b", "#5c3800"
        verdict = f"⚠️ {domain_label} Signal: UNCERTAIN"
        verdict_color = "#5c3800"
    else:
        bar_color, label_color = "#dc2626", "#5c0a0a"
        verdict = f"🚨 {domain_label} Signal: INSUFFICIENT"
        verdict_color = "#5c0a0a"

    st.markdown(
        f"""
        <div style="border:2px solid {bar_color}; border-radius:12px; padding:20px 24px;
                    margin-bottom:24px; background:#ffffff;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:{FONT_SIZES['total_score_heading']}; font-weight:800; color:#111111;">Total Score</span>
            <span style="font-size:{FONT_SIZES['total_score_number']}; font-weight:900; color:{label_color};">{score:.1f} / 100</span>
          </div>
          <div style="background:#d8dce3; border-radius:8px; height:24px; width:100%; margin-bottom:10px;">
            <div style="background:{bar_color}; width:{score}%; height:24px; border-radius:8px;"></div>
          </div>
          <div style="font-size:{FONT_SIZES['total_score_verdict']}; font-weight:800; color:{verdict_color};">{verdict}</div>
          <div style="font-size:{FONT_SIZES['total_score_footnote']}; color:#444444; margin-top:5px; font-weight:500;">
            Weighted composite across {n_biomarkers} biomarkers.
            Score ≥ 60 = positive signal &nbsp;|&nbsp; 40–59 = uncertain &nbsp;|&nbsp; &lt; 40 = insufficient evidence.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_cardio_total_score_bar(score):
    n = len(CARDIO_BIOMARKER_PARAMS)
    if score < 35:
        bar_color, label_color = "#1db954", "#0a4522"
        verdict = "✅ Cardiotoxicity Risk: NOMINAL"
        verdict_color = "#0a4522"
    elif score < 65:
        bar_color, label_color = "#f59e0b", "#5c3800"
        verdict = "⚠️ Cardiotoxicity Risk: CAUTION"
        verdict_color = "#5c3800"
    else:
        bar_color, label_color = "#dc2626", "#5c0a0a"
        verdict = "🚨 Cardiotoxicity Risk: CRITICAL"
        verdict_color = "#5c0a0a"

    st.markdown(
        f"""
        <div style="border:2px solid {bar_color}; border-radius:12px; padding:20px 24px;
                    margin-bottom:24px; background:#ffffff;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:{FONT_SIZES['total_score_heading']}; font-weight:800; color:#111111;">Total Cardiotoxicity Risk Score</span>
            <span style="font-size:{FONT_SIZES['total_score_number']}; font-weight:900; color:{label_color};">{score:.1f} / 100</span>
          </div>
          <div style="background:#d8dce3; border-radius:8px; height:24px; width:100%; margin-bottom:10px;">
            <div style="background:{bar_color}; width:{score}%; height:24px; border-radius:8px;"></div>
          </div>
          <div style="font-size:{FONT_SIZES['total_score_verdict']}; font-weight:800; color:{verdict_color};">{verdict}</div>
          <div style="font-size:{FONT_SIZES['total_score_footnote']}; color:#444444; margin-top:5px; font-weight:500;">
            Weighted composite across {n} biomarkers (cytokine panel + proteomics). &nbsp;
            Score 0–34 = Nominal &nbsp;|&nbsp; 35–64 = Caution &nbsp;|&nbsp; 65–100 = Critical.
            Higher score = greater cardiovascular concern.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DATA HELPERS
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


def post_pre_ratio(tps_dict):
    pre  = [v for k, v in tps_dict.items() if k.startswith('L') and v is not None]
    post = [v for k, v in tps_dict.items() if k.startswith('R') and v is not None]
    if pre and post and np.mean(pre) != 0:
        return np.mean(post) / np.mean(pre)
    return None


# ============================================================
# NEURO CREW STATS
# ============================================================

_NEURO_PER_CREW_MARKERS = {
    "BDNF (urine ratio)",
    "GFAP (Glial Fibrillary Acidic Protein — urine ratio)",
    "NGF (Nerve Growth Factor — urine ratio)",
    "CXCL10 (IP-10 — Neuroinflammatory Chemokine — urine ratio)",
}


def _neuro_raw_for_crew(target_crew_id):
    prot_map = {
        "BDNF (Brain-Derived Neurotrophic Factor)":       get_logfc(pp, 'BDNF'),
        "S100B (Astrocyte Damage Marker)":                get_logfc(pp, 'S100B'),
        "NRGN (Neurogranin — Synaptic Marker)":           get_logfc(pp, 'NRGN'),
        "CLU (Clusterin — Neuroprotective Chaperone)":    get_logfc(pp, 'CLU'),
        "APOE (Apolipoprotein E — CNS Lipid Transport)":  get_logfc(pp, 'APOE'),
    }

    urine_col_map = {
        "BDNF (urine ratio)":                                         'bdnf_concentration_npq',
        "GFAP (Glial Fibrillary Acidic Protein — urine ratio)":       'gfap_concentration_npq',
        "NGF (Nerve Growth Factor — urine ratio)":                    'ngf_concentration_npq',
        "CXCL10 (IP-10 — Neuroinflammatory Chemokine — urine ratio)": 'cxcl10_concentration_npq',
    }
    urine_map = {}
    for label, col in urine_col_map.items():
        tps = get_urine_per_crew(urine, col, target_crew_id)
        urine_map[label] = post_pre_ratio(tps)

    kyn_logfc = get_met_logfc(met, 'Kynurenine')
    trp_logfc = get_met_logfc(met, 'Tryptophan')
    kt_ratio  = None
    if kyn_logfc is not None and trp_logfc is not None and trp_logfc != 0:
        kt_ratio = round(kyn_logfc / trp_logfc, 3)

    met_map = {
        "Kynurenine (Neuro-Inflammatory Pathway)":          kyn_logfc,
        "Tryptophan (Serotonin Precursor)":                 trp_logfc,
        "5-HIAA (Serotonin Metabolite)":                    get_met_logfc(met, '5-Hydroxyindoleacetic Acid'),
        "Kynurenine:Tryptophan Ratio (K:T Ratio)":          kt_ratio,
        "N-Acetylaspartic Acid (NAA — Neuronal Viability)": get_met_logfc(met, 'N-Acetylaspartic Acid'),
        "Cortisol (Neuro — HPA Axis Activation)":           get_met_logfc(met, 'Cortisol'),
        "Nicotinamide (NAD+ Precursor — Neuroprotection)":  get_met_logfc(met, 'Nicotinamide'),
    }

    return {**prot_map, **urine_map, **met_map}


@st.cache_data
def _build_neuro_crew_stats():
    all_crew_ids = list(CREW_CONFIG.keys())
    per_marker = {}
    for cid in all_crew_ids:
        raw = _neuro_raw_for_crew(cid)
        for name, val in raw.items():
            per_marker.setdefault(name, {})[cid] = val

    stats = {}
    for name, crew_vals in per_marker.items():
        valid = [(cid, v) for cid, v in crew_vals.items() if v is not None]
        vals_only = [v for _, v in valid]
        if len(vals_only) >= 2:
            mu = float(np.mean(vals_only))
            sd = float(np.std(vals_only, ddof=1))
        elif len(vals_only) == 1:
            mu = float(vals_only[0])
            sd = 0.0
        else:
            mu, sd = 0.0, 1.0
        stats[name] = {"mean": mu, "sd": sd, "values": crew_vals}
    return stats


def _neuro_dynamic_thresholds(name, stats, n_sd=1.0):
    s  = stats.get(name, {})
    mu = s.get("mean", 0.0)
    sd = s.get("sd",   1.0)
    is_per_crew = name in _NEURO_PER_CREW_MARKERS
    if is_per_crew and sd > 1e-9:
        return mu - n_sd * sd, mu + n_sd * sd, mu, sd
    return mu - 1.0, mu + 1.0, mu, 1.0


def render_neuro_score_bar(label, score, note, threshold_type, data_value,
                           data_label, crew_mean, crew_sd, is_per_crew, is_averaged=False):
    if score is None:
        st.markdown(
            f"<div style='font-size:{FONT_SIZES['unavailable_label']}; color:#555555; margin-bottom:8px;'>"
            f"<b>{label}</b> — <i>data not available</i></div>",
            unsafe_allow_html=True,
        )
        return

    if score >= 60:
        bar_color, text_color = "#1db954", "#0a4522"
    elif score >= 40:
        bar_color, text_color = "#f59e0b", "#5c3800"
    else:
        bar_color, text_color = "#dc2626", "#5c0a0a"

    raw_display = ""
    if data_value is not None:
        raw_display = (
            f"<span style='font-size:{FONT_SIZES['score_bar_raw_value']}; "
            f"color:#444444; font-weight:500;'>"
            f"({data_label}: {data_value:+.3f})</span>"
        )

    badge_styles = {
        "low":  ("⬇ low threshold",   "#cce5ff", "#003d7a"),
        "high": ("⬆ high threshold",  "#ffd5d9", "#6b0a12"),
        "both": ("↕ both thresholds", "#e8d5f7", "#3d0070"),
    }
    badge_text, badge_bg, badge_fg = badge_styles.get(threshold_type, ("threshold", "#eeeeee", "#333333"))
    badge_html = (
        f"<span style='font-size:{FONT_SIZES['score_bar_badge']}; background:{badge_bg}; "
        f"color:{badge_fg}; border-radius:4px; padding:2px 6px; margin-left:6px; "
        f"font-weight:700; vertical-align:middle;'>{badge_text}</span>"
    )

    avg_tag = ""
    if is_averaged:
        avg_tag = (
            f"<span style='font-size:{FONT_SIZES['score_bar_avg_tag']}; background:#fff8e1; "
            f"color:#7d4e00; border-radius:4px; padding:2px 6px; margin-left:6px; "
            f"font-weight:700; vertical-align:middle;'>⚠️ group avg</span>"
        )

    if is_per_crew and crew_sd > 1e-9:
        ref_html = (
            f"<div style='font-size:{FONT_SIZES['neuro_crew_ref']}; color:#333333; "
            f"margin-top:2px; font-weight:500;'>"
            f"📊 Crew mean = {crew_mean:+.3f} &nbsp;|&nbsp; "
            f"±1 SD band = [{crew_mean - crew_sd:+.3f}, {crew_mean + crew_sd:+.3f}]</div>"
        )
    else:
        ref_html = (
            f"<div style='font-size:{FONT_SIZES['neuro_crew_ref']}; color:#666666; margin-top:2px;'>"
            f"📊 Shared value across crew &nbsp;|&nbsp; scored against ±1.0 symmetric window</div>"
        )

    st.markdown(
        f"""
        <div style="margin-bottom:14px; background:#ffffff; border-radius:8px; padding:10px 14px; border:1px solid #e8eaed;">
          <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
            <span style="font-weight:700; font-size:{FONT_SIZES['score_bar_label']}; color:#111111;">{label}{badge_html}{avg_tag}</span>
            <span style="font-weight:800; color:{text_color}; font-size:{FONT_SIZES['score_bar_score']};">
              {score:.1f}/100 &nbsp; {raw_display}
            </span>
          </div>
          <div style="background:#d8dce3; border-radius:6px; height:16px; width:100%;">
            <div style="background:{bar_color}; width:{score}%; height:16px;
                        border-radius:6px; transition:width 0.4s;"></div>
          </div>
          {ref_html}
          <div style="font-size:{FONT_SIZES['score_bar_note']}; color:#444444; margin-top:3px; font-style:italic; line-height:1.5;">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DATASET WARNING BANNER
# ============================================================

def show_averaged_section_warning():
    st.markdown(
        f"<div style='background:#fff8e1; border:2px solid #f59e0b; border-radius:8px; "
        f"padding:12px 16px; margin:6px 0 16px 0; font-size:{FONT_SIZES['averaged_warning']}; "
        f"color:#5c3800; font-weight:600;'>"
        f"⚠️ <b>Data averaged across all crew members</b> — "
        f"The values shown in this section are group-level averages and do <b>not</b> "
        f"change when switching crew members. "
        f"Per-individual proteomics/metabolomics were not available in this dataset."
        f"</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# MODULE 1 — BONE TAB
# ============================================================

def render_bone_tab(crew_id):
    st.title("🦴 Bone Density Loss Inhibitor Efficacy")

    st.warning(
        "⚕️ **Dataset Notice:** The current cohort does not include astronauts taking any "
        "therapeutic medications. Subjects were healthy and not in space long enough to exhibit "
        "massive changes to bone density, muscle atrophy, or brain degradation. Biomarker levels "
        "should therefore appear relatively normal and extreme signals are not expected."
    )

    st.write(
        "Each biomarker is scored 0–100 based on calibrated thresholds. "
        "The **Total Efficacy Score** is a weighted average across all biomarkers. "
        "**Green bars** indicate a protective/efficacious signal; "
        "**red bars** indicate bone-loss risk or insufficient drug effect. "
        "Markers tagged **⚠️ group avg** come from datasets averaged across all crew members."
    )

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

    ca = get_cmp_per_crew(cmp, 'calcium_value_milligram_per_deciliter', crew_id)
    ap = get_cmp_per_crew(cmp, 'alkaline_phosphatase_value_units_per_liter', crew_id)

    cmp_map = {
        "Calcium (CMP ratio)":              post_pre_ratio(ca),
        "Alkaline Phosphatase (CMP ratio)": post_pre_ratio(ap),
    }

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
    urine_map = {
        label: post_pre_ratio(get_urine_per_crew(urine, col, crew_id))
        for label, col in urine_col_map.items()
    }

    met_map = {
        "Vitamin D2 (Ergocalciferol)": get_met_logfc(met, 'Ergocalciferol'),
        "Cortisol (metabolomics)":      get_met_logfc(met, 'Cortisol'),
        "Proline":                      get_met_logfc(met, 'Proline'),
        "Glycine":                      get_met_logfc(met, 'Glycine'),
        "Lysine":                       get_met_logfc(met, 'Lysine'),
        "Citric Acid":                  get_met_logfc(met, 'Citric Acid'),
    }

    all_raw = {**prot_map, **cmp_map, **urine_map, **met_map}

    scores = {
        name: score_biomarker(
            all_raw.get(name),
            p["low"], p["high"], p["higher_is_better"], p.get("threshold_type", "both")
        )
        for name, p in BONE_BIOMARKER_PARAMS.items()
    }

    total_weight = sum(p["weight"] for name, p in BONE_BIOMARKER_PARAMS.items() if scores.get(name) is not None)
    weighted_sum = sum(scores[name] * p["weight"] for name, p in BONE_BIOMARKER_PARAMS.items() if scores.get(name) is not None)
    total_score = (weighted_sum / total_weight) if total_weight > 0 else 50.0
    render_total_score_bar(total_score, len(BONE_BIOMARKER_PARAMS), domain_label="Drug Efficacy")

    sections = [
        ("🔬 Proteomics (logFC — flight vs. pre-flight)", prot_map, "logFC", True),
        ("🧪 CMP Serum Chemistry (post/pre ratio)", cmp_map, "ratio", False),
        ("💧 Urine Inflammation Panel (post/pre ratio)", urine_map, "ratio", False),
        ("⚗️ Metabolomics (logFC — flight vs. pre-flight)", met_map, "logFC", True),
    ]

    for section_title, raw_dict, val_label, section_averaged in sections:
        with st.expander(section_title, expanded=True):
            if section_averaged:
                show_averaged_section_warning()
            for name, raw_val in raw_dict.items():
                params = BONE_BIOMARKER_PARAMS.get(name)
                if params is None:
                    continue
                render_score_bar(
                    label=name, score=scores.get(name), note=params["note"],
                    threshold_type=params.get("threshold_type", "both"),
                    data_value=raw_val, data_label=val_label,
                    is_averaged=params.get("averaged", False),
                )


# ============================================================
# MODULE 2 — CARDIOTOXICITY SAFETY
# ============================================================

def render_cardio_tab(crew_id):
    st.title("❤️ Cardiotoxicity Safety")

    st.warning(
        "⚕️ **Dataset Notice:** The current cohort does not include astronauts taking any "
        "therapeutic medications. Subjects were healthy and not in space long enough to exhibit "
        "massive changes to bone density, muscle atrophy, or brain degradation. Biomarker levels "
        "should therefore appear relatively normal — extreme signals are not expected."
    )

    st.write(
        "Each biomarker is scored **0–100 as a risk score** — higher means greater cardiovascular "
        "concern. The **Total Cardiotoxicity Risk Score** is a weighted average across all markers. "
        "**Green bars** indicate low concern; **red bars** indicate elevated cardiovascular risk. "
        "Markers tagged **⚠️ group avg** come from datasets averaged across all crew members."
    )

    cytokine_col_map = {
        "CRP (C-Reactive Protein)":         'crp_concentration_picogram_per_milliliter',
        "PF4 (Platelet Factor 4)":          'pf4_concentration_nanogram_per_milliliter',
        "Fibrinogen":                       'fibrinogen_concentration_nanogram_per_milliliter',
        "Fetuin-A":                         'fetuin_a36_concentration_nanogram_per_milliliter',
        "Haptoglobin":                      'haptoglobin_concentration_nanogram_per_milliliter',
        "L-Selectin (CD62L)":              'l_selectin_concentration_picogram_per_milliliter',
        "SAP (Serum Amyloid P Component)":  'sap_concentration_picogram_per_milliliter',
        "Alpha-2-Macroglobulin (A2M)":      'a2_macroglobulin_concentration_nanogram_per_milliliter',
        "AGP (Alpha-1-Acid Glycoprotein)":  'agp_concentration_nanogram_per_milliliter',
    }
    cytokine_map = {
        label: post_pre_ratio(get_cardiac_per_crew(card, row_name, crew_id))
        for label, row_name in cytokine_col_map.items()
    }

    prot_map = {
        "VWF (Von Willebrand Factor — proteomics)":              get_logfc(pp, 'VWF'),
        "SERPINE1 / PAI-1 (Fibrinolysis Inhibitor — proteomics)": get_logfc(pp, 'SERPINE1'),
    }

    all_raw = {**cytokine_map, **prot_map}

    scores = {
        name: score_cardio_biomarker(
            all_raw.get(name), p["low"], p["high"], p.get("threshold_type", "high")
        )
        for name, p in CARDIO_BIOMARKER_PARAMS.items()
    }

    total_weight = sum(p["weight"] for name, p in CARDIO_BIOMARKER_PARAMS.items() if scores.get(name) is not None)
    weighted_sum = sum(scores[name] * p["weight"] for name, p in CARDIO_BIOMARKER_PARAMS.items() if scores.get(name) is not None)
    total_score = (weighted_sum / total_weight) if total_weight > 0 else 0.0
    render_cardio_total_score_bar(total_score)

    sections = [
        ("🩸 Cardiac Cytokine / Plasma Panel (post/pre ratio)", cytokine_map, "ratio", False),
        ("🔬 Proteomics (logFC — flight vs. pre-flight)",        prot_map,    "logFC", True),
    ]

    for section_title, raw_dict, val_label, section_averaged in sections:
        with st.expander(section_title, expanded=True):
            if section_averaged:
                show_averaged_section_warning()
            for name, raw_val in raw_dict.items():
                params = CARDIO_BIOMARKER_PARAMS.get(name)
                if params is None:
                    continue
                render_cardio_score_bar(
                    label=name, score=scores.get(name), note=params["note"],
                    threshold_type=params.get("threshold_type", "high"),
                    data_value=raw_val, data_label=val_label,
                    is_averaged=params.get("averaged", False),
                )


# ============================================================
# MODULE 3 — NEUROLOGICAL RESILIENCE
# ============================================================

def render_neuro_tab(crew_id):
    st.title("🧠 Neurological Resilience")

    st.warning(
        "⚕️ **Dataset Notice:** The current cohort does not include astronauts taking any "
        "therapeutic medications. Subjects were healthy and not in space long enough to exhibit "
        "massive changes to bone density, muscle atrophy, or brain degradation. Biomarker levels "
        "should therefore appear relatively normal — extreme signals are not expected."
    )

    st.write(
        "Each biomarker is scored 0–100 relative to the **crew average**. "
        "Thresholds are set at **crew mean ± 1 SD** for per-crew markers (urine panel), "
        "and at a **±1.0 symmetric window** around the shared value for proteomics and metabolomics. "
        "Markers tagged **⚠️ group avg** come from datasets averaged across all crew members."
    )

    crew_stats     = _build_neuro_crew_stats()
    raw_this_crew  = _neuro_raw_for_crew(crew_id)

    prot_map = {k: raw_this_crew[k] for k in [
        "BDNF (Brain-Derived Neurotrophic Factor)",
        "S100B (Astrocyte Damage Marker)",
        "NRGN (Neurogranin — Synaptic Marker)",
        "CLU (Clusterin — Neuroprotective Chaperone)",
        "APOE (Apolipoprotein E — CNS Lipid Transport)",
    ]}
    urine_map = {k: raw_this_crew[k] for k in [
        "BDNF (urine ratio)",
        "GFAP (Glial Fibrillary Acidic Protein — urine ratio)",
        "NGF (Nerve Growth Factor — urine ratio)",
        "CXCL10 (IP-10 — Neuroinflammatory Chemokine — urine ratio)",
    ]}
    met_map = {k: raw_this_crew[k] for k in [
        "Kynurenine (Neuro-Inflammatory Pathway)",
        "Tryptophan (Serotonin Precursor)",
        "5-HIAA (Serotonin Metabolite)",
        "Kynurenine:Tryptophan Ratio (K:T Ratio)",
        "N-Acetylaspartic Acid (NAA — Neuronal Viability)",
        "Cortisol (Neuro — HPA Axis Activation)",
        "Nicotinamide (NAD+ Precursor — Neuroprotection)",
    ]}

    scores     = {}
    thresholds = {}

    for name, params in NEURO_BIOMARKER_PARAMS.items():
        raw = raw_this_crew.get(name)
        low, high, mu, sd = _neuro_dynamic_thresholds(name, crew_stats)
        thresholds[name] = (low, high, mu, sd)
        scores[name] = score_biomarker(raw, low, high, params["higher_is_better"],
                                       params.get("threshold_type", "both"))

    total_weight = sum(p["weight"] for name, p in NEURO_BIOMARKER_PARAMS.items() if scores.get(name) is not None)
    weighted_sum = sum(scores[name] * p["weight"] for name, p in NEURO_BIOMARKER_PARAMS.items() if scores.get(name) is not None)
    total_score = (weighted_sum / total_weight) if total_weight > 0 else 50.0
    render_total_score_bar(total_score, len(NEURO_BIOMARKER_PARAMS), domain_label="Neurological Resilience")

    sections = [
        ("🔬 Proteomics (logFC — flight vs. pre-flight)", prot_map, "logFC", True),
        ("💧 Urine Inflammation Panel (post/pre ratio)",   urine_map, "ratio", False),
        ("⚗️ Metabolomics (logFC — flight vs. pre-flight)", met_map, "logFC", True),
    ]

    for section_title, raw_dict, val_label, section_averaged in sections:
        with st.expander(section_title, expanded=True):
            if section_averaged:
                show_averaged_section_warning()
            for name, raw_val in raw_dict.items():
                params = NEURO_BIOMARKER_PARAMS.get(name)
                if params is None:
                    continue
                _, _, mu, sd = thresholds.get(name, (0, 0, 0, 1))
                render_neuro_score_bar(
                    label=name, score=scores.get(name), note=params["note"],
                    threshold_type=params.get("threshold_type", "both"),
                    data_value=raw_val, data_label=val_label,
                    crew_mean=mu, crew_sd=sd,
                    is_per_crew=(name in _NEURO_PER_CREW_MARKERS),
                    is_averaged=params.get("averaged", False),
                )


# ============================================================
# TOP-OF-PAGE CREW SELECTOR
# ============================================================

def render_crew_selector():
    st.markdown(
        f"""
        <div style="background:#e8eaed; border-radius:12px; padding:16px 20px; margin-bottom:20px;">
          <div style="font-size:{FONT_SIZES['crew_selector_heading']}; font-weight:700; margin-bottom:10px;
                      text-transform:uppercase; letter-spacing:0.08em; color:#111111;">
            Select Crew Member
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(CREW_CONFIG))
    for col, (crew_id, cfg) in zip(cols, CREW_CONFIG.items()):
        is_active = st.session_state.selected_crew == crew_id
        with col:
            label_str = f"{'✓ ' if is_active else ''}{cfg['label']}"
            if st.button(
                label_str,
                key=f"top_crew_{crew_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.selected_crew = crew_id
                st.rerun()

    button_css = ""
    for i, (crew_id, cfg) in enumerate(CREW_CONFIG.items(), start=1):
        is_active = st.session_state.selected_crew == crew_id
        opacity   = "1.0" if is_active else "0.65"
        border    = f"3px solid {cfg['color']}" if is_active else "2px solid #ccc"
        button_css += f"""
        div[data-testid="stHorizontalBlock"] > div:nth-child({i})
          button {{
            background-color: {cfg['color']} !important;
            color: {cfg['text']} !important;
            border: {border} !important;
            opacity: {opacity} !important;
            font-weight: {'800' if is_active else '600'} !important;
            font-size: {FONT_SIZES['crew_button']} !important;
            border-radius: 8px !important;
            transition: all 0.15s ease !important;
        }}
        div[data-testid="stHorizontalBlock"] > div:nth-child({i})
          button:hover {{
            background-color: {cfg['hover']} !important;
            opacity: 1.0 !important;
        }}
        """
    st.markdown(f"<style>{button_css}</style>", unsafe_allow_html=True)


def render_crew_card(crew_id):
    cfg   = CREW_CONFIG[crew_id]
    photo = cfg.get("photo", "")
    app_dir = os.path.dirname(os.path.abspath(__file__))
    photo_path = os.path.join(app_dir, photo)

    col_img, col_info = st.columns([1, 4])
    with col_img:
        if photo and os.path.exists(photo_path):
            st.image(photo_path, width=110)
        else:
            st.markdown(
                f"""
                <div style="
                    width:100px; height:100px; border-radius:50%;
                    background:{cfg['color']}; display:flex;
                    align-items:center; justify-content:center;
                    font-size:36px; color:{cfg['text']}; font-weight:900;
                    border:3px solid #ddd;">
                  {cfg['label'][0]}
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_info:
        st.markdown(
            f"""
            <div style="background:#ffffff; border-left:4px solid {cfg['color']};
                        border-radius:0 10px 10px 0; padding:12px 16px;
                        box-shadow:0 1px 4px rgba(0,0,0,0.08);">
              <div style="font-size:{FONT_SIZES['crew_card_name']}; font-weight:800; color:#111111;">
                {cfg['label']}
                <span style="font-size:{FONT_SIZES['crew_card_id']}; color:#666666; font-weight:500; margin-left:8px;">
                  ID: {crew_id}
                </span>
              </div>
              <div style="font-size:{FONT_SIZES['crew_card_demographics']}; color:#333333; margin-top:2px; font-weight:600;">
                Age: {cfg['age']} &nbsp;|&nbsp; Sex: {cfg['sex']}
              </div>
              <div style="font-size:{FONT_SIZES['crew_card_bio']}; color:#444444; margin-top:6px; line-height:1.55;">
                {cfg['bio']}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='margin:14px 0 4px 0; border:1px solid #d0d4db;'>", unsafe_allow_html=True)


# ============================================================
# SIDEBAR — MODULE NAVIGATION
# ============================================================

st.sidebar.title("Astronaut Therapeutic Testing")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 View Module")

module_options = [
    "🦴 Bone Density Loss Inhibitor Efficacy",
    "❤️ Cardiotoxicity Safety",
    "🧠 Neurological Resilience",
]

selected_module = st.sidebar.radio(
    label="",
    options=module_options,
    index=0,
    label_visibility="collapsed",
)

st.sidebar.markdown("---")

selected_cfg = CREW_CONFIG[st.session_state.selected_crew]
st.sidebar.markdown(
    f"""
    <div style="
        background-color: {selected_cfg['color']};
        color: {selected_cfg['text']};
        padding: 10px 14px;
        border-radius: 10px;
        font-weight: 700;
        font-size: {FONT_SIZES['sidebar_active_crew']};
        text-align: center;
        margin-top: 4px;
    ">
        📡 Viewing: {selected_cfg['label']}<br>
        <span style="font-size:{FONT_SIZES['sidebar_active_crew_sub']}; font-weight:400; opacity:0.9;">
          ID: {st.session_state.selected_crew}
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

if not DATA_LOADED:
    st.sidebar.markdown("---")
    st.sidebar.error(f"⚠️ Could not load CSV data from:\n`{DATA_DIR}`\n\nError: {DATA_ERROR}")
    st.sidebar.info(
        "Adjust `DATA_DIR` at the top of `app.py` to point to your `data/processed/` folder."
    )

# ============================================================
# MAIN CONTENT
# ============================================================

render_crew_selector()

crew = st.session_state.selected_crew
render_crew_card(crew)

if not DATA_LOADED:
    st.error("⚠️ Data not loaded. Check the sidebar for details.")
    st.stop()

if selected_module == "🦴 Bone Density Loss Inhibitor Efficacy":
    render_bone_tab(crew)
elif selected_module == "❤️ Cardiotoxicity Safety":
    render_cardio_tab(crew)
elif selected_module == "🧠 Neurological Resilience":
    render_neuro_tab(crew)
