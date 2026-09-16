# Reproducibility and Code Materials

## Study

**Title:** Does Trajectory Improve Peer-Country Selection?  
**Subtitle:** Evidence from Annual Ragged-Edge GDP Nowcasting

This document accompanies the manuscript and records the implementation details needed to reproduce the reported experiments. The eight-page manuscript contains the core methodological description; this file provides the fuller variable-level, split-level, preprocessing, implementation, and output information requested by the reviewers.

> **Important:** This document is intended to describe the **final manuscript experiment**. Earlier exploratory/internal reports may contain different sample sizes, fusion weights, metrics, or preprocessing choices. Those earlier settings are not part of the final confirmatory experiment unless explicitly confirmed by the final code.

---

## 1. Final-study specification

### 1.1 Research question

The confirmatory question is:

> Does information contained in development trajectories provide incremental predictive power beyond economic-level similarity for peer-country selection in annual GDP nowcasting?

### 1.2 Panel and study period

- Annual observations: **2004–2023**
- Initial panel: **197 economies** [VERIFY FROM CURRENT DATA BUILD]
- Final evaluation panel: **176 economies** [VERIFY EXCLUSION RULE AND COMPLETE LIST]
- Data source: **World Bank Data360 / World Bank Indicators** [VERIFY EXACT ENDPOINT USED BY CURRENT CODE]

### 1.3 Forecasting target

The target variable is:

- **`GDPC_2015`** — GDP per capita, PPP [VERIFY EXACT DATABASE LABEL/DEFINITION]
- Target transformation in model space: **`log1p(GDPC_2015)`**, i.e.

  y(i,t) = log(1 + GDPC(i,t))

  [VERIFY THIS MATCHES THE CURRENT CONFIRMATORY TRAINING CODE]

Predictions generated in transformed space are inverse-transformed before final level-scale MAE calculation:

  GDP_hat(i,t) = exp(y_hat(i,t)) - 1

The final confirmatory MAE reported in the manuscript is therefore calculated in **USD GDP-per-capita levels**, not in log space.

### 1.4 Predictor variables

The six macroeconomic indicators used in the study are:

1. `Agri_GDP`
2. `Indus_GDP`
3. `Serv_GDP`
4. `Elec_Access`
5. `Internet_Usage`
6. `FDI_GDP`

These variables provide the information used to construct the economic-level and trajectory representations and to implement the ragged-edge availability scenarios.

### 1.5 Baselines and experimental approaches

The final confirmatory experiment compares five approaches:

1. **Level**
2. **Trajectory**
3. **Level–Trajectory Fusion**
4. **NoPeerRidge**
5. **Persistence**

Only the approach/peer-representation factor is varied in the confirmatory comparison. The forecasting model, preprocessing, temporal evaluation protocol, and primary metric are held constant.

---

## 2. Data processing

### 2.1 Missing-data treatment

Missing indicator observations are handled by **within-economy forward filling** [VERIFY EXACT ORDER RELATIVE TO TRANSFORMATION AND SPLITTING].

Document in the implementation:

- whether forward filling is permitted only from observations already available by the forecast origin;
- what happens when no prior observation exists;
- whether target GDP values are treated differently from predictor indicators;
- whether missingness after the forecast origin is ever used.

### 2.2 Feature-specific transformations

The current implementation specification to be verified against `preprocessor.py` is:

| Variable | Transformation | Purpose / note |
|---|---|---|
| `Agri_GDP` | `log1p` | Reduce skew / stabilize small values |
| `FDI_GDP` | Winsorization (1%–99%) + RobustScaler | Reduce influence of extreme outliers |
| `Elec_Access` | MinMaxScaler to [0,1] | Place bounded percentage variable on common scale |
| `Indus_GDP` | StandardScaler (z-score) | Standardize scale |
| `Serv_GDP` | StandardScaler (z-score) | Standardize scale |
| `Internet_Usage` | No additional transformation | Already bounded on a common scale |

> **Verification required:** confirm that this table describes the **current final code** and not an earlier experiment. If the current implementation differs, replace this table with the actual pipeline.

### 2.3 Leakage control for preprocessing

All transformation/scaling parameters must be fit only on information permitted by the final confirmatory design.

The final manuscript specifies that normalization parameters used in peer-distance calculations are fitted using the **early 2004–2016 period** and then frozen for subsequent test years.

> **Verification required:** confirm whether feature preprocessors are also fit globally on 2004–2016 or separately within each split's training data. The manuscript and code must use the same description.

---

## 3. Ragged-edge design

### 3.1 Availability scenarios

The final manuscript uses three intra-year information-availability scenarios based on six indicators:

| Scenario | Available indicators |
|---|---|
| **EARLY** | 0/6 |
| **MID** | `Elec_Access`, `Internet_Usage` (2/6) |
| **LATE** | all except `FDI_GDP` (5/6) |

### 3.2 Revised data vs real-time vintages

Historical real-time vintages are unavailable for the full global panel. The final experiment therefore uses:

> **Artificial availability masks applied to revised historical data to simulate the ragged-edge information problem.**

This is a simulation of publication availability, not a reconstruction of actual historical data vintages.

### 3.3 Publication-lag implementation

The reproducibility package should include a machine-readable scenario map specifying, for every indicator:

- scenario availability;
- assumed delay/mask rule;
- whether the mask is applied by year, forecast origin, or another rule;
- whether the same rule is applied to every economy.

> **Verification required:** do not describe these as historical indicator-specific publication lags unless the current code actually implements observed/assumed lag values. If the design is only an availability-mask experiment, label it as such.

---

## 4. Temporal validation

### 4.1 32 evaluation splits

The final study uses 32 temporal evaluation splits:

| Split family | Number | Definition |
|---|---:|---|
| One-year expanding window | 7 | Train from 2004; test 2017–2023 one year at a time |
| Multi-year expanding window | 2 | Train 2004–2016 -> test 2017–2019; train 2004–2019 -> test 2020–2023 |
| Five-year sliding window | 7 | Five-year training window; test following year, 2017–2023 |
| Ten-year sliding window | 7 | Ten-year training window; test following year, 2017–2023 |
| Fixed-length | 5 | Train on 5/8/10/12/15 years; test 2023 |
| Era/parity | 4 | Additional prespecified temporal partitions; exact definitions below |

No separate validation set is used because the confirmatory hyperparameters are fixed a priori.

### 4.2 Complete split definition file

The package should include:

`train_test_splits.csv`

with at least:

- `split_id`
- `split_family`
- `train_start`
- `train_end`
- `validation_start` = `NA`
- `validation_end` = `NA`
- `test_start`
- `test_end`

### 4.3 Era/parity splits

The final package must explicitly define all four era/parity splits, including their exact years and the meaning of “parity.”

> **Verification required:** this information is not sufficiently specified by the manuscript alone.

---

## 5. Peer representations

### 5.1 Level

For economy i at forecast origin t, x(i,t,L) is the vector of historical-average values of the macroeconomic indicators used for peer selection.

The exact indicator list and averaging window are recorded in:

`config/level_features.yml`

> **Verification required:** record the exact averaging window and whether GDP itself enters the Level vector.

### 5.2 Trajectory

For economy i at forecast origin t, x(i,t,T) contains the growth-dynamics representation of the same indicators.

The final manuscript currently specifies that the trajectory is based on temporal slopes using historical observations available before the forecast origin.

> **Verification required:** record the exact slope implementation:
>
> - OLS slope against year, first-to-last change, or another definition;
> - exact historical window;
> - minimum required observations;
> - whether slope estimation occurs before or after normalization.

### 5.3 Distance functions

For candidate peer j:

d(L) = ||x(i,t,L) - x(j,t,L)||_2

d(T) = ||x(i,t,T) - x(j,t,T)||_2

and the fusion distance is:

d(F) = alpha * d(L) + (1-alpha) * d(T)

### 5.4 Fusion weight

The final confirmatory manuscript specifies:

**alpha = 0.5**

This value is fixed a priori and is not optimized using test-period outcomes.

> **Verification required:** confirm the current experiment uses **0.5**, not an earlier exploratory/internal value.

### 5.5 Peer count

The final confirmatory manuscript specifies:

**k = 8**

At each forecast origin, the eight nearest eligible peers are selected according to the relevant distance.

### 5.6 Peer eligibility

The implementation documentation must specify:

- whether the target economy is excluded from its own peer set;
- minimum data availability required for peers;
- whether eligibility is scenario-specific;
- whether peer GDP must be observed at the relevant forecast origin;
- how ties are handled.

### 5.7 Inverse-distance weighting

Missing target GDP information is reconstructed using inverse-distance weighting across the selected peers.

The code/materials should provide the exact weight equation and explicitly define the zero-distance case.

---

## 6. Leakage safeguards

The final pipeline must document:

1. temporal separation of training and test data;
2. no use of future observations in peer construction;
3. normalization fitted only on permitted historical data;
4. fixed k = 8;
5. fixed alpha = 0.5;
6. no test-period hyperparameter tuning;
7. ragged-edge masking applied using only allowed information.

A dedicated automated check should be included:

`tests/test_no_lookahead.py`

This should verify that no feature value, scaler parameter, peer distance, or peer outcome is constructed using information after the relevant forecast origin.

---

## 7. Ridge forecasting model

### 7.1 Confirmatory model

The forecasting model is Ridge regression.

The final manuscript currently specifies:

- Ridge regression;
- fixed regularization parameter lambda = 1;
- identical model specification across the five confirmatory approaches;
- no test-period hyperparameter tuning.

> **Verification required:** confirm that the current implementation actually uses lambda = 1 and record the exact library implementation and intercept setting.

### 7.2 Model configuration file

Store the full fixed configuration in:

`config/model.yml`

Example fields:

```yaml
model: Ridge
regularization: 1.0
fit_intercept: true
random_state: null
hyperparameter_tuning: none
```

Replace values as required by the actual implementation.

### 7.3 Randomness

Record explicitly whether the current pipeline is deterministic.

If deterministic:

> `random_state: null` and “No stochastic fitting procedure is used.”

If any preprocessing, ordering, or sampling is stochastic, record the exact seed.

---

## 8. Confirmatory evaluation

### 8.1 Primary metric

The primary confirmatory metric is **Mean Absolute Error (MAE)**.

Predictions produced in log1p-GDP space are inverse-transformed to GDP levels before calculating MAE:

MAE = mean(|GDP_hat - GDP|)

The reported main MAE is therefore in **USD GDP-per-capita units**.

### 8.2 Main evaluation subset

Table 1 uses a balanced evaluation subset/common-support intersection.

The reproducibility package should define this subset explicitly and save it as:

`outputs/confirmatory_common_support.csv`

including:

- country;
- year;
- scenario;
- split;
- valid prediction flags for all five approaches.

> **Verification required:** use the term **balanced evaluation subset** for Table 1 if the post-hoc analyses use different approach-specific intersections.

### 8.3 Adjusted marginal means

The main results report adjusted marginal mean MAE with 95% confidence intervals.

The reproducibility package should record:

- adjustment factors;
- exact model/formula used for adjustment;
- CI calculation method.

> **Verification required:** the current manuscript does not fully document how the 95% CIs are constructed.

---

## 9. Confirmatory statistical inference

### 9.1 Dependence structure

The five approaches are evaluated on matched country–year–scenario instances across temporal splits, so errors are treated as paired repeated measurements rather than independent observations.

### 9.2 Omnibus test

The manuscript uses the **Friedman test** as the omnibus non-parametric repeated-measures test across the five approaches.

Store the exact result:

- Friedman statistic;
- df = 4;
- p-value;
- effect size (e.g., Kendall's W, if used).

### 9.3 Pairwise testing

If and only if the Friedman omnibus test is significant:

- Wilcoxon signed-rank tests are applied to paired approaches;
- Holm correction is applied for multiple comparisons;
- the final package stores paired differences, test statistics, adjusted p-values, and effect sizes.

### 9.4 Confirmatory result file

Store:

`outputs/confirmatory_statistics.csv`

with:

- omnibus statistic;
- p-value;
- effect size;
- pairwise comparison;
- median paired difference;
- Wilcoxon statistic;
- raw p-value;
- Holm-adjusted p-value;
- pairwise effect size.

---

## 10. Post-hoc exploratory analyses

Post-hoc analyses are separate from the confirmatory five-approach comparison.

The current exploratory script includes:

1. Persistence–Level ensemble;
2. fusion-weight sweep;
3. country heterogeneity;
4. country-level case studies.

The exploratory script itself identifies this block as post hoc.

### 10.1 Approach-specific common-support intersections

The post-hoc analyses use different intersections:

- Persistence + Level for the ensemble;
- Level + Trajectory for the alpha sweep.

Therefore, these are **approach-specific common-support subsets**, not one universal post-hoc sample.

### 10.2 Exploratory metric

The post-hoc code calculates **MAPE on back-transformed GDP levels**, not the confirmatory MAE.

MAPE = mean(|GDP_hat - GDP| / |GDP|) * 100

The exact denominator/sign convention must be confirmed against the current evaluation code.

### 10.3 Fusion-weight sweep

The current exploratory script evaluates:

alpha in {0.00, 0.25, 0.50, 0.75, 1.00}.

The lowest exploratory MAPE is identified descriptively; this is **not** treated as confirmatory optimization.

### 10.4 Persistence–Level ensemble

The ensemble combines the predictions of Persistence and Level on the intersection where both are valid.

The current exploratory script averages the two predicted transformed values before inverse transformation. The exact aggregation rule should be retained in the code and documented here.

### 10.5 GDP-level heterogeneity

The exploratory code divides economies into:

- LowGDP
- MediumGDP
- HighGDP

using tertiles of mean GDP.

This is not automatically equivalent to official World Bank income groups.

### 10.6 Volatility heterogeneity

Country volatility is calculated from the standard deviation of percentage changes in `GDPC_2015`, then divided into:

- LowVol
- HighVol

### 10.7 Period analysis

The exploratory code distinguishes:

- PreCOVID
- COVID
- PostCOVID

The exact year membership should be stored in `config/periods.yml`.

### 10.8 Country case studies

The exploratory script currently examines:

- USA
- Vietnam
- Malawi

These are illustrative cases, not population-representative evidence.

---

## 11. Reproducibility outputs

The final package should include, at minimum:

```text
ragged_edge_nowcasting/
├── README.md
├── requirements.txt
├── config/
│   ├── data.yml
│   ├── scenarios.yml
│   ├── model.yml
│   ├── level_features.yml
│   ├── periods.yml
│   └── splits.yml
├── src/
│   ├── data_loader.py
│   ├── preprocessor.py
│   ├── ragged_edge.py
│   ├── feature_engineering.py
│   ├── neighbor_selection.py
│   ├── models.py
│   └── evaluation.py
├── experiments/
│   ├── experiment_train_test_splits.py
│   └── posthoc_analysis.py
├── tests/
│   ├── test_no_lookahead.py
│   ├── test_transformations.py
│   └── test_peer_selection.py
├── split_definitions/
│   └── train_test_splits.csv
├── outputs/
│   ├── confirmatory_common_support.csv
│   ├── confirmatory_statistics.csv
│   ├── ensemble_means.csv
│   ├── alpha_sweep_means.csv
│   ├── country_heterogeneity.csv
│   └── posthoc_summary.json
└── docs/
    └── REPRODUCIBILITY_MATERIALS.md
```

---

## 12. Required metadata for final submission

Record the following in `README.md`:

### Software
- Python version
- package versions
- operating system
- repository commit/tag

### Data
- exact World Bank Data360 endpoint/source
- extraction date
- raw-data file checksum
- cleaned-data file checksum

### Computational reproducibility
- random seed(s), or explicit statement that the pipeline is deterministic;
- exact command used to reproduce the main experiment;
- exact command used to reproduce post-hoc analyses.

### Output mapping
Document which files produce:

- Figure 1;
- Figure 2;
- Figure 3;
- Table 1;
- confirmatory statistical results;
- post-hoc results.

---

## 13. Automated verification checklist

Before submission:

- [ ] Target is exactly `GDPC_2015`.
- [ ] Target transformation is confirmed as `log1p`.
- [ ] Inverse transformation is confirmed as `expm1`.
- [ ] Six predictor variables match the current code.
- [ ] Final economy count = 176, and exclusion rule is documented.
- [ ] EARLY/MID/LATE masks match the manuscript.
- [ ] 32 split definitions exactly match the manuscript.
- [ ] No hidden validation set exists.
- [ ] Trajectory slope/window is documented.
- [ ] Level averaging window is documented.
- [ ] Peer eligibility is documented.
- [ ] Target country is excluded from its own peers.
- [ ] k=8 matches code.
- [ ] alpha=0.5 matches the final confirmatory code.
- [ ] Ridge lambda=1 matches the final confirmatory code.
- [ ] No test-period tuning is performed.
- [ ] MAE is calculated after inverse transformation to USD.
- [ ] 95% CI procedure is documented.
- [ ] Friedman statistic/p-value/effect size are saved.
- [ ] Wilcoxon tests are conditional on the omnibus test.
- [ ] Holm correction is implemented.
- [ ] Post-hoc analyses are clearly separated from confirmatory analyses.
- [ ] Post-hoc MAPE is correctly labeled as MAPE, not MAE.
- [ ] Post-hoc common-support intersections are documented separately.
- [ ] GDP groups are correctly described as tertiles unless formal income groups are actually used.
- [ ] COVID year definitions are documented.
- [ ] Figure numbering and manuscript cross-references are correct.
- [ ] Data/code/declaration statements are consistent with the manuscript.

---

## 14. Version-control note

An earlier internal report described a different experiment using, among other differences, a 196-country panel, alpha=0.7, and RMSE as a primary metric. Those values must **not** be mixed into the final manuscript reproducibility package unless the current final code confirms that they belong to the submitted experiment.

The final package should have one unambiguous source of truth:

> **final manuscript ↔ final code ↔ final split definitions ↔ final outputs**

Earlier exploratory reports should be retained separately as historical/internal documentation, not as the reproducibility specification for the submitted paper.
