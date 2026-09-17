# THƯ TRẢ LỜI PHẢN BIỆN — VNICT 2026, PAPER ID 6546

> **Hướng dẫn nội bộ (không nộp phần này).** Phần nộp là toàn bộ đoạn tiếng Anh từ dòng "RESPONSE TO REVIEWERS" trở xuống — copy sang file .docx/.pdf hoặc dán vào ô response của hệ thống nộp bài.
>
> - Mọi con số trong thư đã được đối chiếu lại từ `bang_doi_chieu_so_lieu.md` (126 claim đã kiểm, 106 khớp ngay, 20 lỗi đã sửa, 2 tồn nhỏ: M2 thẩm mỹ, M4 đã trả lời trong thư). **Nếu sửa bất kỳ số nào trong paper thì phải sửa lại số đó ở đây.**
> - Hạn: bản nội bộ 24/9, thư 25/9, nộp 26/9/2026.
> - Nộp kèm: PDF 6 trang, file .tex, thư mục `figures/` — `fig13_ablation.png` **đã xóa khỏi `figures/` ngày 17/9** (không được dùng trong bài; bản gốc vẫn còn trong `code/output_paper/`).
> - Tiêu đề mỗi mục Comment dưới đây là **bản tóm lược ý của reviewer** (bản gốc tiếng Việt), không phải trích nguyên văn.
> - Hai reviewer cùng mức weak accept và nêu gần như trùng nhau 4 ý, nên trả lời **gộp một bản** (đã được duyệt ở mục VI của kế hoạch).
> - Số dùng trong thư (nguồn: bảng đối chiếu): 0.0077 · 0.0086 · 0.0105 · 0.0157 · 0.0125 · 0.0226 · 19.1% · RMSE 0.0248→0.0219 · R2 0.9989→0.9992 · 6/9, 8/9, 7/9 · Wilson [0.354, 0.879] · accuracy 0.9945/0.9958/0.9945 · precision 1.000/0.974/0.974 · 37/38 ngày nguy hiểm · bias −0.005 đến −0.026 m (RF/XGBoost/Stacking) · ngưỡng P95/P99 = 1.06/1.24 m trên chuỗi train 28 năm.

---

## RESPONSE TO REVIEWERS

**Paper ID:** 6546

**Revised title:** Feature-Engineering-Driven Machine Learning as a Surrogate of Hydrodynamic Simulation for Multi-Step Water Level Forecasting in the Quang Ha Estuary

**Submitted title:** Multi-step Water Level Forecasting in the Quang Ha Estuarine Area Using Ensemble Machine Learning and Interpretable Feature Analysis

**Authors:** Hieu Ta, Thao Nguyen Thi — Faculty of Information Technology, Thuyloi University, Hanoi, Vietnam

**Decision:** weak accept (both reviewers) — accept after revision

Dear Editors and Reviewers,

We thank both reviewers for a careful and constructive reading. The two reviews converge on the same four substantive points: every series in the study is an output of a hydrodynamic simulator, the very high R-squared values and centimeter-level MAE need cautious interpretation, the risk-zone accuracy rests on a strongly imbalanced test set, and the contribution should be framed as feature engineering rather than as an advantage of ensemble models. We respond to them jointly below. We agree with every point raised, and we would add that acting on them improved the paper more than we expected: none of the changes below required us to withdraw a result, but they did require us to state the scope of each result much more precisely.

The revision makes six structural changes:

1. **The title has been changed.** The submitted title led with "Ensemble Machine Learning", which the results do not support at short lead times, where a linear model on the engineered features is the most accurate. The revised title leads with feature engineering and names the surrogate role of the model explicitly.
2. **The surrogate framing is now stated from the outset** — in the Abstract, in a dedicated paragraph of the Introduction, in the Discussion, and as the fourth and most important limitation in Section V — instead of appearing only in the Limitations.
3. **A new experiment and section quantify the simulator-to-field gap** (Section IV-G and Table IV): additive Gaussian measurement noise on the input series, two scenarios, three noise seeds per configuration. This converts a qualitative caveat into a measured degradation curve and shows that the model ranking itself changes under noise.
4. **The risk-zone evaluation has been rebuilt** (Table II and Section IV-C): a single accuracy figure is replaced by accuracy, precision, recall and F1 with Wilson 95 per cent score intervals, per-zone MAE, the full sample counts, and an explicit separation of the favourable and the unfavourable readings of the result.
5. **Every number in the paper was re-derived from the frozen result artifacts and checked cell by cell** — all 60 cells of Table I against the result files, and all of Table II re-derived from the raw 3x3 confusion matrices rather than from the aggregated metrics file. Where two tables necessarily come from different fitting configurations, the difference is now disclosed in a table note. This check also uncovered one data-leakage bug in the script that generated the naive baselines of the submitted version; it is described under Comment 7 below, together with the other corrections we made on our own initiative.
6. **The paper fits the six-page limit** with references included. To make room for the new material we merged the model-comparison tables into a single Table I and removed the feature-ablation figure, reporting its numbers in the text instead. We did not change the font, the margins, or the header and footer of the template.

---

### Comment 1 — The temporal split and the walk-forward validation are reasonably designed

We thank the reviewers for this. We would nevertheless point out, and the revised paper now states explicitly, that the walk-forward experiment is narrower than the submitted text implied. It covers a single year, 2020, giving 366 evaluation days per horizon; it is run for the Stacking model only; it retrains every four weeks; and the trailing *h* rows of each window are dropped so that no target used in training overlaps an evaluation date. Sections III-D and IV-B now say this directly.

The reported walk-forward MAPE ranges from 3.4 per cent at t+1 to 7.2 per cent at t+3. The t+3 and t+7 errors closely match the static split, while the t+1 MAE rises slightly, from 0.0105 m to 0.0110 m, which may indicate that short-term forecasts benefit from more frequent updating. We state in Section IV-B that these figures, rather than the static ones, indicate more realistically how the pipeline would behave if driven forward in time. Extending the backtest to the full 2020-2021 test period and to the remaining candidate models is the obvious next step, and we record it here as future work.

### Comment 2 — All data are MIKE11 simulation outputs, so the machine learning model mainly approximates a simulator, and field forecasting ability is not demonstrated

We agree completely, and this comment changed the framing of the whole paper. The revised version states in the Abstract that, because no observed water-level record was available, the resulting model should be read as a fast surrogate of the hydrodynamic simulator rather than as a validated field forecasting tool. The Introduction carries a dedicated paragraph to the same effect, the Discussion draws only the conclusion the data support — that the pipeline reproduces the behavior of the simulator accurately enough to be used in place of it — and Section V states this as the fourth and most important limitation.

We would also record what we checked before writing this. The largest raw file in the project contains only the daily MIKE11 output at the Ha Coi section, the two upstream discharge series and the hourly downstream sea-level boundary for 1990-2021. There is no observed water-level series anywhere in the dataset, so no analysis in the submitted version could have been a field validation, and the revised text no longer suggests otherwise.

### Comment 3 — R-squared above 0.998 and centimeter-level MAE need cautious interpretation

We agree, and we now quantify the caveat instead of only stating it. The new Section IV-G and Table IV report the result of injecting additive Gaussian noise, with standard deviation of 1, 2 and 5 cm, into the input series only — water level and downstream sea level — while the targets are kept as the clean simulation values and act as ground truth. Features are recomputed with the same engineering code after the noise is added, so the perturbation propagates through the pipeline exactly as gauge error would. Each noisy configuration is averaged over three noise seeds. Two scenarios are run: S1, trained clean and tested noisy, which isolates distribution mismatch; and S2, trained and tested at the same noise level, which isolates the effect of noise as such.

The main results, all in meters of MAE:

- At t+1 the Stacking model degrades from 0.0105 m at zero noise to 0.0147 m at one centimeter, an increase of 40 per cent, and to 0.0212 m at two centimeters, a factor of two.
- At t+3 the unregularized linear model degrades severely, from 0.0086 m to 0.0693 m at one centimeter and to 0.3291 m at five centimeters, whereas XGBoost degrades far more gracefully over the same range, 0.0247 m and 0.0818 m, and becomes the most accurate model at that horizon from two centimeters onward.
- At t+1 the tree ensembles overtake the linear model from two centimeters onward, 0.039 m against 0.051 m at five centimeters. At t+7 Ridge is the most robust model once the noise reaches two centimeters.
- Under scenario S2 the degradation is much smaller: at t+3 with two centimeters of noise the linear model falls from 0.136 m in S1 to 0.030 m, comparable to XGBoost at 0.028 m. The collapse observed in S1 is therefore caused by the mismatch between a clean training distribution and a noisy test distribution, not by the linear model as such.

The conclusion we draw in the paper is that the centimeter-level accuracy and the advantage of a simple linear model are properties of the noise-free simulation data, and that regularization and model diversity matter once measurement error is present. The Abstract and the Conclusion now carry this caveat together with the headline numbers, and the R-squared values are reported as a range, 0.9984 to 0.9996 for the learned models, rather than as a single impressive figure.

One point of transparency: the range of one to five centimeters is a working assumption about gauge error, not a measurement from a specific station, and the paper does not cite a source for it. We chose it to bracket the plausible accuracy of a water-level recorder. It will be replaced by the real observation error once the measured series listed in the validation roadmap of Section V becomes available; the roadmap has three steps, of which obtaining the observed water levels at the Ha Coi gauge from the MIKE11 calibration record is the first.

### Comment 4 — The three-zone risk accuracy of 99.45 to 99.58 per cent rests on a strongly imbalanced test set (684 / 29 / 9 days)

We agree that the imbalance is the central weakness of this evaluation, and the revision now says so in Section IV-C and in Section V. The nine Exceedance days of the test period are not enough to support a strong accuracy claim, and we no longer make one. Table II has been rebuilt to show, for each horizon: three-zone accuracy with a Wilson 95 per cent score interval, precision, recall and F1 for the merged dangerous class (Warning or Exceedance), recall for the Exceedance class alone, and its Wilson interval. The full sample counts and the per-zone MAE are given in the table note, and Section IV-C records that the zone thresholds, 1.06 m and 1.24 m, are the P95 and P99 percentiles of the 28-year training record, so the thresholds are not tuned on the test period.

We separate the two readings of the result explicitly, because they point in opposite directions and a reader should be able to weigh both:

- **The favourable reading.** The Exceedance recall is 6/9 at t+1, 8/9 at t+3 and 7/9 at t+7; the merged dangerous class flags 37 of the 38 dangerous days at every horizon; the per-zone MAE stays within 0.008 to 0.021 m; and, which matters most operationally, no Exceedance day is classified as Normal at any horizon — the Exceedance errors, three at t+1, one at t+3 and two at t+7, are all downgrades to Warning. The precision of the dangerous class is 1.000 at t+1 and 0.974 beyond, so the system does not raise false alarms.
- **The unfavourable reading.** The Exceedance recall of 6/9 has a Wilson 95 per cent interval of [0.35, 0.88], which is too wide to distinguish the model from a coin flip on that class. Section V states this as the fifth limitation and does not soften it.

We also report a finding that emerged while rebuilding this table: all ten models under-predict the peak levels, and for RF, XGBoost and Stacking the mean bias on Exceedance days is between −0.005 m and −0.026 m. This is the unsafe direction for flood warning, and the paper says so, and proposes a cost-weighted loss or an explicit bias correction for the extreme class as the remedy. The submitted version did not report this bias at all.

### Comment 5 — Linear Regression is the best model at t+1 and t+3, so the contribution should be framed as feature engineering rather than as an advantage of the ensemble models

We agree, and this is the reason for the new title. The evidence is now stated in the Abstract, as Contribution 5 of the Introduction, in Section IV-E, and in the Conclusion: Linear Regression on the engineered features is the most accurate model at t+1 (0.0077 m) and at t+3 (0.0086 m), ahead of every ensemble tested; ensemble diversity matters only at t+7, where the proposed AdaptiveStack reaches 0.0125 m against 0.0226 m for Linear Regression, 19.1 per cent below XGBoost, with RMSE improving from 0.0248 m to 0.0219 m and R-squared from 0.9989 to 0.9992.

Two further analyses support this framing. First, the feature-group ablation in Section IV-D: the full feature set gives the lowest MAE at every horizon. At t+1, adding the rolling, seasonal, interaction and risk groups to the lag-only features reduces the RF MAE from 0.0300 m to 0.0162 m; at t+7 the seasonal group is the single most valuable addition, taking the MAE from 0.0340 m to 0.0226 m, with the full set reaching 0.0207 m; and at t+3 Ridge is most accurate with the full set, 0.0149 m. That sweep uses Ridge and a depth-capped RF variant to stay tractable, so its absolute values are not directly comparable to Table I, and the paper says so. Second, the Wilcoxon signed-rank tests on paired daily errors: at t+1 RF and XGBoost are not separable (p = 0.31) and the three ensembles differ by less than 0.0005 m in MAE, while at t+3 and t+7 the differences are significant (XGBoost against Stacking p < 0.001 and p = 0.022; RF against Stacking p = 0.004). The submitted version claimed significance at t+1 where the test does not support it; that claim has been corrected.

The SHAP analysis is reported as an interpretation of which features the model relies on, not as a demonstrated physical mechanism. The strongest attributions are `water_level_lag_14` and `distance_to_threshold` at t+1, `sea_delta_1` at t+3, and `water_level_lag_7` with `acceleration` at t+7. Section IV-F connects these to the tidal structure of the record — the periodogram gives a dominant period of 14.76 days on the training period and 14.73 days on the test period, against the 14.8-day spring-neap cycle, and the normalized autocorrelation is +0.91, +0.33 and −0.86 at lags 1, 3 and 7 with a zero crossing at lag 4; a pure sinusoid of that period would give −0.99 at lag 7 — and states that this is an interpretation rather than a demonstrated cause.

### Comment 6 — Validation against real stations, at multiple locations and for several extreme events, is needed

We cannot add it in this revision, and we do not pretend otherwise. As recorded under Comment 2, no observed water-level series exists in the dataset available to us. Instead of leaving this as a one-sentence caveat, Section V now sets out a three-step validation roadmap, and it is the roadmap that makes the surrogate claim checkable rather than merely honest:

1. obtain the observed water levels at the Ha Coi gauge from the MIKE11 calibration record;
2. quantify the MIKE11-versus-observation error on that record, so that the simulator error and the model error can be separated;
3. extend the study to multiple stations and to storm-tide compound events.

Until step 1 is done, the accuracy figures in the paper describe how well the model reproduces the simulator. In the meantime the noise experiment of Section IV-G is the most useful evidence we can offer, because it measures how much of the reported accuracy survives contact with measurement error; it is also the reason the ranking change under noise is reported in the paper as a finding rather than as a footnote.

### Comment 7 — Corrections we made on our own initiative

While re-deriving every number in the paper we found and fixed the following. We list them here because several of them change results that the reviewers read in the submitted version.

- **Data leakage in the naive baselines (most serious).** The submitted script built the naive forecasts by rolling the target column, which makes the prediction at t+h depend on the observed level at t+h−lag; whenever h exceeds the lag this uses a future value. The script was rewritten to look up the level by date, which is leak-free and gives an essentially constant MAE across horizons, as a naive baseline should. The affected rows were regenerated and relabeled Naive-lag14. The naive configurations now reach MAE between 0.275 m and 1.292 m, with Naive-lag14 the strongest at every horizon (0.2121 to 0.2126 m) and Naive-lag7 by far the weakest (1.289 to 1.292 m). The submitted version also omitted this range from the text; it is now reported, together with Ridge Regression at 0.0089, 0.0149 and 0.0261 m.
- **A wrong claim of statistical significance** at t+1, corrected as described under Comment 5, and the RF-against-Stacking test added.
- **An over-stated improvement** of the AdaptiveStack: 19.4 per cent was reported in four places; the correct figure from the predictions file is 19.1 per cent.
- **A missing tie**: at t+3 XGBoost and ExtraTrees both reach 0.0157 m; the submitted version credited XGBoost alone.
- **A wrong crossover point** in the noise discussion: the tree ensembles overtake the linear model at t+1 from two centimeters of noise, not from five.
- **A wrong threshold span**: the risk-zone thresholds are the P95 and P99 percentiles of the 28-year training record, not of a 31-year record.
- **An inconsistent MAE for the best linear model** at t+1: Table I and five places in the text reported 0.0078 m, which comes from the noise experiment where the model is fitted on train plus validation; the correct value for Table I, whose models are fitted on the training split only, is 0.0077 m. All six places now agree, and the note to Table IV explains that its zero-noise row is its own noise-free reference and differs marginally from Table I.
- **Contradictions between the explainability text and Figure 2**: Section III-E and the caption of Figure 2 stated that the importance analysis was not based on SHAP, while the figure itself is a SHAP plot, and the Limitations repeated the denial. The text and the caption were rewritten to match the figure, and the Table III values are the mean absolute SHAP contributions in meters.
- **Two reference errors**: reference [6] pointed to a different paper and has been replaced by the correct Hai Duong sluice-gate study, and the first author of reference [8] was misnamed in the text; the correct name is Xiong.
- **An unsupported causal claim** about the lag structure, rewritten as the interpretation described under Comment 5, and the phrase "an order of magnitude" replaced by "or more" where the data did not support it.

### Format compliance

The revised paper is six pages including all thirteen references, uses `\documentclass[conference]{IEEEtran}`, and compiles without errors or overfull boxes. No font, margin, header or footer of the template was modified to fit the content; the space was found by merging the two model-comparison tables into Table I and by removing the ablation figure, whose numbers are reported in Section IV-D instead.

We thank the reviewers again. Their comments led to a new experiment, a rebuilt risk-zone evaluation, a corrected baseline implementation and a title that matches what the results actually show.

Sincerely,

Hieu Ta and Thao Nguyen Thi
Faculty of Information Technology, Thuyloi University
175 Tay Son, Kim Lien Ward, Hanoi, Vietnam
hieutc@tlu.edu.vn
