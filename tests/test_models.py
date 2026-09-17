# -*- coding: utf-8 -*-
"""
Test mo hinh huan luyen.
"""
import sys
sys.path.insert(0, '.')

import numpy as np
import pandas as pd
import pytest


def _make_sample_data(n=200):
    """Tao du lieu mau de test."""
    rng = np.random.default_rng(42)
    X = rng.normal(0, 1, (n, 5))
    y = X @ np.array([1.0, 0.5, -0.3, 0.2, 0.1]) + rng.normal(0, 0.1, n)
    return X, y


class TestModels:
    """Test cac mo hinh huan luyen."""

    def test_linear_regression_shape(self):
        """Linear Regression tra ve so luong output dung."""
        from sklearn.linear_model import LinearRegression

        X, y = _make_sample_data(100)
        model = LinearRegression()
        model.fit(X[:80], y[:80])
        preds = model.predict(X[80:])

        assert preds.shape == (20,), f"Shape sai: {preds.shape}"

    def test_random_forest_no_nan(self):
        """Random Forest khong duoc tra ve NaN."""
        from sklearn.ensemble import RandomForestRegressor

        X, y = _make_sample_data(200)
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X[:150], y[:150])
        preds = model.predict(X[150:])

        assert not np.any(np.isnan(preds)), "Co gia tri NaN trong predictions"

    def test_xgboost_import(self):
        """XGBoost co the import va huan luyen."""
        import xgboost as xgb

        X, y = _make_sample_data(200)
        model = xgb.XGBRegressor(n_estimators=50, max_depth=3, verbosity=0, random_state=42)
        model.fit(X[:150], y[:150])
        preds = model.predict(X[150:])

        assert preds.shape == (50,)
        assert not np.any(np.isnan(preds))

    def test_train_all_models_returns_dict(self):
        """train_all_models tra ve dict."""
        from src.models.train import train_all_models

        X, y = _make_sample_data(200)
        models = train_all_models(X[:150], y[:150], X[150:], y[150:])

        assert isinstance(models, dict)
        assert len(models) >= 3, f"Can it nhat 3 mo hinh, hien co: {len(models)}"

    def test_adaptive_stack_predict(self):
        """AdaptiveStack co the predict."""
        from src.models.train import build_adaptive_stack

        X, y = _make_sample_data(300)
        # Mo hinh MLP can it nhat ~100 mau de huan luyen
        model, _ = build_adaptive_stack(X[:200], y[:200], X[200:250], y[200:250])
        preds = model.predict(X[250:])

        assert preds.shape[0] == 50
        assert not np.any(np.isnan(preds))
