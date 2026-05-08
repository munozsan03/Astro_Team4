# Neurological Resilience Scoring Methodology

## What Is This Score?

The **Neurological Resilience Score** is a number between 0 and 100 that summarizes how well a given crew member's nervous system appears to be holding up — and recovering — relative to the rest of the crew. A higher score means the biological evidence points toward preserved neurological integrity and lower neuro-inflammatory burden. A lower score means that crew member is showing signs of greater stress, damage signaling, or impaired recovery compared to their crewmates.

- **≥ 60** → Positive resilience signal (neurological markers are within or better than crew norms)
- **40–59** → Uncertain (some markers diverge from crew norms; warrants monitoring)
- **< 40** → Concern signal (notable divergence from crew norms across multiple markers)

---

## Why Crew-Relative Scoring — Not Fixed Thresholds?

The bone efficacy module uses fixed biological thresholds (e.g. "RANKL logFC above +0.75 is harmful") because those thresholds are grounded in clinical reference ranges and published drug efficacy literature — they represent a known, mission-independent standard.

Neurological resilience is different in two important ways:

**1. There are no established "normal" logFC or ratio values for spaceflight neurology.**
Markers like BDNF, S100B, and kynurenine:tryptophan ratio shift meaningfully in response to microgravity, radiation, isolation, and circadian disruption — but the field does not have a consensus reference range for *how much* shift is acceptable in this specific context. Applying fixed clinical thresholds (designed for ground-based neurology patients) to astronauts mid-mission would produce misleading scores.

**2. The crew shares the same environmental exposure.**
All four crew members flew the same mission under the same physical stressors. This means the crew's collective response is itself the best available reference frame for what is "typical" under these specific conditions. A crew member who diverges meaningfully from their crewmates is genuinely unusual — not just different from a ground-based population.

**The chosen approach: deviation from the crew median, expressed in units of crew variability (a modified z-score).**

This is preferred over using the crew *mean* because with only four crew members, a single outlier would distort the mean and create a circular comparison (the outlier pulls the reference toward themselves, softening their own apparent deviation). The **median** is resistant to that effect. The spread is measured as the **median absolute deviation (MAD)**, which is similarly robust. Together, median + MAD produce a reference distribution that is not contaminated by the very outlier it is trying to detect.

---

## Where Does the Data Come From?

Three data sources contribute to the Neurological Resilience Score:

| Source | Format | Per-Crew? | Notes |
|--------|--------|-----------|-------|
| **Plasma Proteomics** | logFC (log2 fold-change, flight vs. pre-flight) | ❌ Cohort-wide | Single logFC value per gene across all crew |
| **Urine Inflammation Panel** | Post/pre ratio (NPQ concentration) | ✅ Yes | Each crew member has their own timepoint rows |
| **Plasma Metabolomics** | logFC (flight vs. pre-flight) | ❌ Cohort-wide | Single logFC value per metabolite across all crew |

Because proteomics and metabolomics are cohort-wide (one value per gene/metabolite, not one per crew member), they contribute to the score differently than the urine panel. This distinction is explained in detail below.

---

## Biomarkers Included

### Plasma Proteomics (cohort-wide logFC)

| Biomarker | Direction | Role |
|-----------|-----------|------|
| BDNF | Higher is better | Primary neurotrophin; supports synaptic plasticity and neuronal survival |
| S100B | Lower is better | Astrocyte stress/damage marker; elevated levels indicate glial injury |
| NRGN (Neurogranin) | Higher is better | Synaptic marker of cognitive function; loss associated with neurodegeneration |
| CLU (Clusterin) | Contextual | Neuroprotective chaperone at moderate levels; extreme elevation may indicate stress response |
| APOE | Lower is better | Elevated APOE in plasma is associated with neuroinflammation and lipid dysregulation |

### Urine Inflammation Panel (per-crew post/pre ratio)

| Biomarker | Direction | Role |
|-----------|-----------|------|
| BDNF | Higher is better | Peripheral BDNF secretion reflects central trophic support |
| GFAP | Lower is better | Glial fibrillary acidic protein; urinary elevation signals astrocyte activation or injury |
| NGF (Nerve Growth Factor) | Higher is better | Supports neuronal maintenance and peripheral nerve integrity |
| CXCL10 (IP-10) | Lower is better | Pro-inflammatory chemokine; elevated in neuroinflammatory states and CNS stress |

### Plasma Metabolomics (cohort-wide logFC)

| Biomarker | Direction | Role |
|-----------|-----------|------|
| Kynurenine | Lower is better | Neurotoxic tryptophan catabolite when elevated; marker of IDO pathway activation |
| Tryptophan | Higher is better | Precursor to serotonin and neuroprotective kynurenic acid; depletion is adverse |
| Kynurenine:Tryptophan Ratio | Lower is better | Derived index of IDO pathway activation; elevated ratio indicates neuroinflammatory shift |
| 5-HIAA (5-Hydroxyindoleacetic Acid) | Higher is better | Serotonin metabolite; reduced 5-HIAA reflects depleted serotonergic tone |
| N-Acetylaspartic Acid (NAA) | Higher is better | Neuronal integrity marker; NAA depletion is a sensitive indicator of neuronal loss |
| Cortisol | Lower is better | Chronic HPA-axis activation suppresses BDNF, impairs hippocampal plasticity |
| Nicotinamide | Higher is better | Neuroprotective NAD+ precursor; supports mitochondrial function in neurons |

---

## Scoring Algorithm

### Step 1 — Compute the Crew Reference Distribution (Urine Panel Only)

For biomarkers where per-crew data exists (the urine inflammation panel), the reference is built from the crew itself:

1. For each crew member, compute the **post/pre ratio**: mean of all post-flight timepoints (`R+*`) divided by mean of all pre-flight timepoints (`L-*`).
2. Compute the **crew median** and **crew MAD** (median absolute deviation) across the four resulting ratios.
3. Convert any individual MAD of zero (all crew members identical) to a small floor value to avoid division by zero.

```
crew_median  = median([ratio_C001, ratio_C002, ratio_C003, ratio_C004])
crew_MAD     = median(|ratio_Ci - crew_median|)  for i in {C001..C004}
```

### Step 2 — Compute a Robust Z-Score for the Target Crew Member

For the crew member being evaluated:

```
z = (ratio_subject - crew_median) / (crew_MAD × 1.4826)
```

The constant **1.4826** makes the MAD-based scale consistent with a standard deviation under a normal distribution, so the resulting z-score has a familiar interpretation (z = ±1 ≈ one standard deviation from the median).

### Step 3 — Convert the Z-Score to a 0–100 Score

The z-score is mapped to a 0–100 scale using a **sigmoid (logistic) function**, rather than a linear clip. This is intentional:

- A linear mapping would reward/penalize smoothly right from the median, making small typical variations look meaningful.
- A sigmoid mapping keeps scores near 50 when the crew member is close to the crew norm, and only moves decisively toward 0 or 100 when deviation is substantial. This reflects the actual clinical interpretation: being slightly different from the crew median is unremarkable; being 2+ MAD units away is notable.

```
score_raw = 1 / (1 + exp(−k × z_directional))
score_0_to_100 = score_raw × 100
```

Where:
- `z_directional` is z multiplied by +1 if higher values are better, or −1 if lower values are better.
- `k` is a sensitivity parameter (recommended: **k = 0.8**). Higher k makes the score more sensitive to deviations; lower k makes it more tolerant.

| Z-score (directional) | Approximate Score | Interpretation |
|-----------------------|-------------------|----------------|
| +2.5 | ~87 | Substantially better than crew median |
| +1.0 | ~69 | Modestly above crew median |
| 0.0 | 50 | Exactly at crew median |
| −1.0 | ~31 | Modestly below crew median |
| −2.5 | ~13 | Substantially worse than crew median |

### Step 4 — Handle Cohort-Wide Biomarkers (Proteomics and Metabolomics)

Because proteomics and metabolomics produce a single cohort-wide logFC (not a per-crew value), it is not possible to score one crew member against another on these markers — every crew member would get the same score, which carries no individual information.

**These markers are therefore used as a cohort-level modifier**, not as individual crew scores. The approach:

1. For each cohort-wide biomarker, compute a **cohort score** (0–100) using the same fixed threshold logic as the bone module (logFC thresholds appropriate for plasma proteomics and metabolomics).
2. Compute a **weighted cohort modifier** (the weighted average of all cohort-level biomarker scores, normalized to the range [0.7, 1.3]).
3. Multiply the crew-relative urine panel score by this modifier before computing the final total.

This means:
- If the cohort-wide markers look favorable (e.g. BDNF up, cortisol controlled), every crew member's individual score is modestly boosted.
- If the cohort-wide markers look adverse (e.g. high kynurenine:tryptophan ratio, low NAA), every crew member's individual score is modestly penalized.
- The individual crew comparison from the urine panel still drives the primary differentiation between crew members.

```
cohort_modifier = 0.7 + (cohort_weighted_score / 100) × 0.6   # maps [0,100] → [0.7, 1.3]
final_score = clip(urine_panel_score × cohort_modifier, 0, 100)
```

### Step 5 — Weighted Average Across Urine Biomarkers

The four urine panel biomarkers are combined into a single crew-relative score using a weighted average:

```
urine_panel_score = Σ (score_i × weight_i) / Σ (weight_i)
```

Weights are assigned based on how directly the marker reflects neurological injury vs. peripheral inflammation:

| Biomarker | Weight | Rationale |
|-----------|--------|-----------|
| GFAP (urine) | 8 | Highly specific astrocyte injury marker; most direct neurological signal available in urine |
| CXCL10 (urine) | 6 | CNS-associated neuroinflammatory chemokine with established spaceflight relevance |
| BDNF (urine) | 5 | Reflects neurotrophic support; partially confounded by peripheral sources |
| NGF (urine) | 4 | Peripheral nerve health marker; less CNS-specific than GFAP or CXCL10 |

### Cohort-Wide Biomarker Weights

| Biomarker | Weight | Rationale |
|-----------|--------|-----------|
| BDNF (proteomics) | 8 | Core neuroplasticity marker; most directly interpretable |
| S100B (proteomics) | 7 | Sensitive glial injury marker in plasma |
| Kynurenine:Tryptophan Ratio | 7 | Established neuroinflammatory index |
| Cortisol (metabolomics) | 6 | Strong suppressor of neuroplasticity pathways |
| 5-HIAA (metabolomics) | 5 | Serotonergic tone indicator |
| N-Acetylaspartic Acid | 5 | Neuronal integrity; sensitive to neuronal metabolic compromise |
| NRGN (proteomics) | 4 | Synaptic marker; valuable but less studied in spaceflight |
| Nicotinamide (metabolomics) | 4 | Neuroprotective; supports interpretation of metabolic resilience |
| Tryptophan (metabolomics) | 4 | Substrate availability for serotonin and neuroprotective pathways |
| Kynurenine (metabolomics) | 4 | Direct neurotoxic risk signal |
| CLU (proteomics) | 3 | Chaperone function; context-dependent interpretation |
| APOE (proteomics) | 3 | Neuroinflammation-linked; indirect signal |

---

## Handling Missing Data

- If a crew member is missing all pre-flight or all post-flight urine timepoints, that biomarker is excluded from the weighted average for that crew member only.
- If fewer than three crew members have data for a given urine biomarker, the crew-relative comparison is unreliable and the biomarker is excluded from scoring entirely for that run (flagged in the output).
- Cohort-wide biomarkers (proteomics/metabolomics) that are missing from the dataset are excluded from the cohort modifier calculation.

---

## Summary of Design Decisions

| Decision | Choice | Justification |
|----------|--------|---------------|
| Reference frame | Crew median (not global norms) | No validated spaceflight-specific reference ranges exist; crew shares identical exposure |
| Robust statistic | Median + MAD (not mean + SD) | Resistant to single outlier distortion with n=4 |
| Score shape | Sigmoid (not linear) | Small deviations from the median should not be penalized; only substantial divergence should move the score |
| Cohort-wide markers | Modifier, not individual score | Proteomics/metabolomics are not per-crew; using them as individual scores would give all four crew members the same value |
| Weights | Literature-based, skewed toward CNS-specific markers | GFAP and S100B have the strongest evidence base for CNS injury specificity in a circulating biofluid context |

---

## Score Interpretation Guide

| Score Range | Label | Meaning |
|-------------|-------|---------|
| 75–100 | Strong Resilience | Crew member shows notably better neuro-inflammatory profile than crew median; cohort-wide markers also favorable |
| 60–74 | Positive Signal | Crew member is at or above crew median on most markers |
| 40–59 | Uncertain | Mixed signals; some markers above, some below crew median |
| 25–39 | Concern | Crew member diverges negatively from crew median on multiple markers |
| 0–24 | Strong Concern | Substantial negative deviation across multiple neuro markers; recommend clinical follow-up |

> **Note:** This score is a research decision-support tool, not a clinical diagnosis. All flagged results should be reviewed in the context of raw biomarker values, timepoint coverage, and individual medical history.
