# -*- coding: utf-8 -*-
"""Script test pipeline chay tu dau den cuoi."""
import sys
import warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, '.')

from src.data.loader import load_raw_data, create_temporal_split, prepare_targets
from src.features.engineering import build_all_features, select_features_by_correlation
from src.models.train import train_all_models
from src.evaluation.metrics import compute_metrics

# Load and prepare
df = load_raw_data()
df = prepare_targets(df, horizons=[1, 3, 7])
df = build_all_features(df).dropna()
splits = create_temporal_split(df)
train, val, test = splits['train'], splits['val'], splits['test']

target_cols = [c for c in df.columns if c.startswith('water_level_t')]
raw_cols = ['river_flow_a', 'river_flow_b', 'sea_level', 'water_level']
exclude = target_cols + raw_cols + ['month', 'day_of_year']
all_feature_cols = [c for c in df.columns if c not in exclude]

print(f'Data: train={len(train)}, val={len(val)}, test={len(test)}, features={len(all_feature_cols)}')

# Run for each horizon
for horizon in [1, 3, 7]:
    target_col = f'water_level_t{horizon}'
    selected = select_features_by_correlation(train[all_feature_cols], train[target_col])

    X_tr, y_tr = train[selected].values, train[target_col].values
    X_val, y_val = val[selected].values, val[target_col].values
    X_te, y_te = test[selected].values, test[target_col].values

    models = train_all_models(X_tr, y_tr, X_val, y_val)
    print(f'\nt+{horizon} ({len(selected)} features):')
    for name, model in models.items():
        y_pred = model.predict(X_te)
        m = compute_metrics(y_te, y_pred)
        print(f'  {name:20s} MAE={m["mae"]:.4f} R2={m["r2"]:.4f}')

print('\nPipeline completed successfully!')
