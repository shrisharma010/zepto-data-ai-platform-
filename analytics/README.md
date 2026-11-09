# Titanic analytics

This module contains an exploratory analysis and modeling workflow built from the local Titanic snapshot in `titanic.csv` (891 rows, 15 columns). Run the notebooks from the repository root or from `analytics/`; each resolves its data and artifact paths for either working directory.

## Part 1: Exploratory data analysis

Run [`01_eda.ipynb`](./01_eda.ipynb) for data profiling, missing-value inspection, univariate and bivariate plots, and descriptive survival findings.

Highlights from the 891 passenger records:

- `deck` is missing for 688 records (77.2%), `age` for 177 (19.9%), and `embarked` / `embark_town` for 2 each.
- The notebook retains a cabin/deck-presence indicator, fills missing ages using passenger-class-and-sex medians (with an overall-median fallback), and fills missing `embarked` values with its mode. The original `deck` field and the two missing `embark_town` values remain visible in the analysis frame.
- Overall survival is 38.4%. Survival was 74.2% among women and 18.9% among men; first class had the highest class rate (63.0%), and third class the lowest (24.2%).
- Median fare was 26.00 among survivors and 10.50 among non-survivors.

These are descriptive associations in historical passenger data, not causal estimates.

## Part 2: Classification and fare regression

Run [`02_modeling.ipynb`](./02_modeling.ipynb) to train three survival classifiers, tune a random forest, evaluate a separate fare-regression pipeline, and verify model serialization. The classifier uses a stratified 80/20 split (712 training and 179 test records). Imputers, scaling, and one-hot encoding are fitted inside scikit-learn pipelines on training data only; the selected feature lists exclude target-derived columns such as `alive`.

Held-out classification metrics:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8212 | 0.8136 | 0.6957 | 0.7500 | 0.8664 |
| Decision Tree (max depth 4) | 0.8268 | 0.8167 | 0.7101 | 0.7597 | 0.8543 |
| Random Forest (200 trees) | 0.8212 | 0.7937 | 0.7246 | 0.7576 | 0.8391 |

Five-fold `GridSearchCV`, scored on F1, selected `max_depth=10`, `min_samples_split=5`, and `n_estimators=100`. Its best cross-validation F1 was 0.7581; the fitted forest's out-of-bag score was 0.8230.

The Ridge fare-regression pipeline scored MAE 18.68, RMSE 30.82, R² 0.3860, and adjusted R² 0.3211 on its held-out test set. Adjusted R² counts the 17 predictor columns after one-hot encoding.

The tuned classification pipeline is saved as [`titanic_pipeline.joblib`](./titanic_pipeline.joblib). The final notebook cell reloads it and confirms its prediction matches the in-memory fitted pipeline on a test sample.
