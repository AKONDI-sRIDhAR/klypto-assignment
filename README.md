# NIFTY Quantitative Research (Clean Architecture)

This project implements a compliance-ready quantitative research pipeline for NSE NIFTY 50 trading pairs.
It is built strictly for offline, historical analysis using a clean, reproducible architecture.

## Architecture

- **`src/`**: Pure Python logic. No data state.
- **`notebooks/`**: Execution environment. One notebook per task.
- **`data/`**: State. `raw` is immutable. `processed` is the artifact store.

## Execution Guide

### 1. Setup
Ensure your raw data files are inside `data/raw/` with these exact names:
- `nifty_spot_5min.csv`
- `nifty_futures_raw.csv`
- `nifty_options_raw.csv`

(If you have originals like `nifty50.csv`, run `src/data_utils.py` logic or rename manually. The system expects these canonical names.)

### 2. Run Pipeline
Launch Jupyter Lab:
```bash
jupyter lab
```

Execute notebooks in strict order:

| Notebook | Logic | Input | Output |
| :--- | :--- | :--- | :--- |
| **01_data_validation** | `src.data_io` | Raw CSVs | Validation Logs |
| **02_data_cleaning** | `src.cleaning` | Raw CSVs | `*_clean.csv` |
| **03_data_merging** | `src.merging` | `*_clean.csv` | `nifty_merged_5min.csv` |
| **04_feature_engineering** | `src.features`, `src.greeks` | `nifty_merged_5min.csv` | `nifty_features_5min.csv` |
| **05_regime_detection** | `src.regime` | `nifty_features_5min.csv` | `models/regime_hmm.joblib` |
| **06_strategy_backtest** | `src.strategy` | Features + Model | Metrics |
| **07_ml_enhancement** | `src.ml` | Features | ML Metrics |
| **08_outlier_analysis** | - | Results | Plots |

## Troubleshooting

- **Missing Files**: Check `data/raw/`.
- **Import Errors**: Ensure you define `PROJECT_ROOT` (handled automatically by notebooks).
- **Environment**: Use `python 3.8+` and `requirements.txt`.
