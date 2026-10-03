# TransitPulse AI — ML & Data Pipeline

Machine Learning module containing trajectory processing, baseline predictors, XGBoost training pipelines, and model registry artifacts.

## Structure
- `src/data/`: Data ingestion, GPS trajectory cleaning, stop detection, and feature engineering.
- `src/models/`: Baseline Current Speed, Historical Segment Average, and XGBoost ETA models.
- `src/training/`: Model training scripts and evaluation routines.
- `notebooks/`: Exploration & evaluation Jupyter notebooks.
- `artifacts/`: Serialized model binaries (excluded from Git).
