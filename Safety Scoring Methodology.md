# Cardiotoxicity Safety Scoring Methodology

## What Is This Score?

The **Cardiotoxicity Safety Score** is a single number between **0 and 100** that summarizes how much evidence there is for cardiovascular stress, inflammation, endothelial dysfunction, coagulation activation, and systemic cardiac risk during and after spaceflight.

Unlike the bone efficacy score (where higher is better), this is a **risk score**:

- **0–34** → Low cardiovascular concern (**Nominal / Green**)
- **35–64** → Moderate concern (**Caution / Yellow**)
- **65–100** → High concern (**Critical / Red**)

A higher score means the astronaut is showing stronger biological evidence of cardiovascular strain or cardiotoxicity-related processes.

---

# Where Does the Data Come From?

The cardiotoxicity system combines measurements from two biological datasets:

## 1. Cardiac Cytokine / Plasma Inflammation Panel
These are longitudinal biomarkers measured across multiple mission timepoints.

Examples:
- CRP
- Fibrinogen
- PF4
- Haptoglobin
- Alpha-2-Macroglobulin
- AGP
- L-Selectin
- Fetuin-A
- SAP

For these markers, the app calculates:

```text
Postflight Average / Preflight Average
```

This produces a **post/pre ratio**:

- `1.0` → no change
- `1.5` → 50% higher postflight
- `0.7` → 30% lower postflight

---

## 2. Plasma Proteomics
Proteomics biomarkers are measured as:

```text
logFC (flight vs preflight)
```

Examples:
- VWF
- SERPINE1 (PAI-1)

A:
- positive logFC = increased expression during flight
- negative logFC = decreased expression during flight

---

# How Is Each Biomarker Scored?

Every biomarker receives an individual score between:

```text
0 = minimal concern
100 = maximum concern
```

Each biomarker is independently normalized using:
- threshold values
- desired biological direction
- threshold type
- weighting

---

# Step 1 — Define Thresholds

Every biomarker has editable thresholds:

```python
{
    "low": value,
    "high": value,
}
```

These define the biologically meaningful operating range.

Example:

```python
"CRP": {
    "low": 1.0,
    "high": 2.0
}
```

Meaning:
- ratios below 1.0 are considered low concern
- ratios above 2.0 are considered high concern

These are currently **placeholder thresholds** and are intended to be refined using:
- astronaut cohort distributions
- clinical literature
- NASA flight datasets
- cardiovascular biomarker studies

---

# Step 2 — Desired Direction

Each biomarker is assigned a biological interpretation:

| Direction | Meaning |
|---|---|
| `high_bad` | Elevated values are dangerous |
| `low_bad` | Suppressed values are dangerous |
| `balanced` | Both extremes are dangerous |

Examples:

| Biomarker | Direction |
|---|---|
| CRP | high_bad |
| PF4 | high_bad |
| Fetuin-A | low_bad |
| Calcium-like homeostatic markers | balanced |

---

# Step 3 — Threshold Type Logic

The scoring engine supports three threshold modes.

---

## 1. High Threshold Only (`high`)

Only elevated values are penalized.

Used when:
- inflammation increases risk
- coagulation increases risk
- endothelial activation increases risk

Examples:
- CRP
- PF4
- SAP
- AGP
- L-Selectin

Behavior:
- safe below threshold
- progressively worse above threshold

---

## 2. Low Threshold Only (`low`)

Only suppressed values are penalized.

Used when:
- protective proteins decrease during stress
- loss of anti-inflammatory signaling is harmful

Examples:
- Fetuin-A

Behavior:
- safe above threshold
- progressively worse below threshold

---

## 3. Both Thresholds (`both`)

Both extremes are penalized.

Used when:
- biomarkers must remain physiologically balanced
- both depletion and overactivation are dangerous

Examples:
- Fibrinogen
- Alpha-2-Macroglobulin

Behavior:
- optimal inside range
- risk increases outside range

---

# Step 4 — Convert Values Into a 0–100 Score

The system converts each biomarker into a normalized risk score.

---

## High Threshold Example

For markers where higher values are worse:

```python
score = ((value - low) / (high - low)) * 100
```

Meaning:
- below low threshold → near 0
- above high threshold → near 100

Example:

| CRP Ratio | Score |
|---|---|
| 1.0 | 0 |
| 1.5 | 50 |
| 2.0 | 100 |

---

## Low Threshold Example

For markers where lower values are worse:

```python
score = ((high - value) / (high - low)) * 100
```

Meaning:
- healthy high values → low risk
- suppressed values → high risk

---

## Both Threshold Example

For balanced biomarkers:

- score is best inside the healthy window
- score worsens toward both extremes

Example behavior:

| Ratio | Interpretation |
|---|---|
| 1.0 | ideal |
| 0.5 | concerning |
| 2.0 | concerning |

---

# Biomarker Weighting System

Each biomarker contributes differently to the final score.

Weights represent:
- biological importance
- mechanistic relevance
- literature support
- specificity to cardiovascular stress

The total score is a weighted average.

---

# Total Score Formula

```text
Total Score =
Σ (biomarker_score × weight)
/
Σ (weights)
```

Where:
- Σ means "sum of"
- missing biomarkers are excluded automatically

This prevents missing data from artificially lowering scores.

---

# Example Weight Interpretation

| Weight | Meaning |
|---|---|
| 8–9 | Primary cardiovascular injury markers |
| 6–7 | Strong inflammatory/coagulation signals |
| 4–5 | Secondary supportive indicators |
| 2–3 | Contextual or indirect markers |

---

# Why These Biomarkers Were Chosen

The panel focuses on the major biological systems implicated in astronaut cardiovascular risk:

| System | Biomarkers |
|---|---|
| Systemic inflammation | CRP, AGP, SAP |
| Coagulation / thrombosis | PF4, Fibrinogen |
| Endothelial dysfunction | VWF, L-Selectin |
| Acute phase response | Haptoglobin, Alpha-2-Macroglobulin |
| Metabolic cardiovascular stress | Fetuin-A |
| Impaired fibrinolysis | SERPINE1 (PAI-1) |

These pathways are repeatedly implicated in:
- microgravity adaptation
- endothelial remodeling
- oxidative stress
- thrombosis risk
- chronic inflammation
- cardiovascular deconditioning

---

# Handling Missing Data

If a biomarker:
- was not measured
- failed QC
- contains NaN values

it is skipped automatically:

```python
if value is None:
    continue
```

The denominator also updates automatically so missing biomarkers do not bias the total score.

---

# Visual Risk Classification

The app converts scores into NASA-style operational status indicators.

| Score | Status | Color |
|---|---|---|
| 0–34 | NOMINAL | Green |
| 35–64 | CAUTION | Yellow |
| 65–100 | CRITICAL | Red |

This is applied:
- to each biomarker
- to the overall mission health score

---

# Design Philosophy

Several important design choices were made intentionally:

## Threshold Types Prevent False Penalties
Not every biomarker is dangerous in both directions.

For example:
- high CRP is dangerous
- low CRP is not

So CRP only uses a `"high"` threshold.

---

## Weighted Averaging Improves Biological Accuracy
A major thrombosis signal (PF4) should matter more than a weaker secondary marker.

Weights preserve this hierarchy.

---

## Linear Scaling Keeps Interpretation Intuitive
A score of:
- 80 always means "more concerning"
- 20 always means "less concerning"

across all biomarkers.

---

## The System Is Modular
New biomarkers can be added simply by editing:

```python
CARDIO_THRESHOLDS = {}
```

without changing the scoring engine.

---

# Summary

The Cardiotoxicity Safety Score is a:
- modular
- interpretable
- threshold-driven
- weighted biological risk model

designed to summarize:
- inflammation
- thrombosis
- endothelial dysfunction
- car