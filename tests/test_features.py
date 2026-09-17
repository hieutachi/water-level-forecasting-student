# -*- coding: utf-8 -*-
"""
Test feature engineering.
"""
import sys
sys.path.insert(0, '.')

import numpy as np
import pandas as pd
import pytest


def _make_sample_data(n=100):
    """Tao du lieu mau de test."""
    dates = pd.date_range("2020-01-01", periods=n, freq="D")
    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "river_flow_a": rng.uniform(1, 10, n),
        "river_flow_b": rng.uniform(0, 5, n),
        "sea_level": rng.normal(0.3, 0.2, n),
        "water_level": rng.normal(0.5, 0.3, n),
    }, index=dates)


class TestFeatureEngineering:
    """Test cac ham tao feature."""

    def test_build_all_features_output_shape(self):
        """Ma tran feature phai nhieu hon cot goc."""
        from src.features.engineering import build_all_features

        df = _make_sample_data(200)
        result = build_all_features(df)

        # Sau khi build feature, so cot phai lon hon nhieu
        assert result.shape[1] > df.shape[1], (
            f"So cot sau feature ({result.shape[1]}) phai lon hon cot goc ({df.shape[1]})"
        )

    def test_build_all_features_no_inf(self):
        """Khong duoc co gia tri inf trong feature."""
        from src.features.engineering import build_all_features

        df = _make_sample_data(200)
        result = build_all_features(df).dropna()

        assert not np.any(np.isinf(result.select_dtypes(include=[np.number]).values)), \
            "Ton tai gia tri inf trong feature matrix"

    def test_lag_features_count(self):
        """So luong lag feature dung nhu dinh nghia."""
        from src.features.engineering import create_lag_features

        df = _make_sample_data(100)
        result = create_lag_features(df, columns=["water_level"], lag_periods=[1, 7, 14])

        expected_new = 3  # 3 lag periods * 1 column
        actual_new = result.shape[1] - df.shape[1]
        assert actual_new == expected_new

    def test_rolling_features_positive_window(self):
        """Rolling mean khong duoc am khi du lieu khong am."""
        from src.features.engineering import create_rolling_features

        df = _make_sample_data(100)
        df["water_level"] = np.abs(df["water_level"])  # dam bao khong am
        result = create_rolling_features(df, windows=[7])

        col = "rolling_mean_7"
        valid = result[col].dropna()
        assert (valid >= 0).all(), "Rolling mean co gia tri am"

    def test_risk_features_binary_flag(self):
        """is_rising chi co gia tri 0 hoac 1."""
        from src.features.engineering import create_risk_features

        df = _make_sample_data(200)
        result = create_risk_features(df)

        unique = result["is_rising"].dropna().unique()
        assert set(unique).issubset({0, 1}), f"is_rising co gia tri la: {unique}"

    def test_seasonal_features_range(self):
        """month_sin va month_cos phai nam trong [-1, 1]."""
        from src.features.engineering import create_seasonal_features

        df = _make_sample_data(365)
        result = create_seasonal_features(df)

        assert result["month_sin"].between(-1, 1).all()
        assert result["month_cos"].between(-1, 1).all()

    def test_feature_selection_returns_list(self):
        """Feature selection tra ve list."""
        from src.features.engineering import select_features_by_correlation

        df = _make_sample_data(200)
        X = pd.DataFrame({
            "a": np.random.randn(200),
            "b": np.random.randn(200),
            "c": np.random.randn(200),
        })
        y = np.random.randn(200)

        result = select_features_by_correlation(X, y)
        assert isinstance(result, list)
