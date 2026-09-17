# -*- coding: utf-8 -*-
"""
Test evaluation metrics va risk zone.
"""
import sys
sys.path.insert(0, '.')

import numpy as np
import pytest


class TestMetrics:
    """Test tinh metrics."""

    def test_mae_non_negative(self):
        """MAE khong duoc am."""
        from src.evaluation.metrics import compute_metrics

        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.1, 1.9, 3.2, 3.8, 5.1])

        metrics = compute_metrics(y_true, y_pred)
        assert metrics["mae"] >= 0, f"MAE am: {metrics['mae']}"

    def test_mae_zero_for_perfect(self):
        """MAE = 0 khi du bao hoan hao."""
        from src.evaluation.metrics import compute_metrics

        y = np.array([1.0, 2.0, 3.0])
        metrics = compute_metrics(y, y)
        assert abs(metrics["mae"]) < 1e-10

    def test_r2_perfect(self):
        """R2 = 1 khi du bao hoan hao."""
        from src.evaluation.metrics import compute_metrics

        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        metrics = compute_metrics(y, y)
        assert abs(metrics["r2"] - 1.0) < 1e-10

    def test_rmse_gte_mae(self):
        """RMSE luon >= MAE."""
        from src.evaluation.metrics import compute_metrics

        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.1, 1.9, 3.2, 3.8, 5.1])

        metrics = compute_metrics(y_true, y_pred)
        assert metrics["rmse"] >= metrics["mae"], \
            f"RMSE ({metrics['rmse']}) < MAE ({metrics['mae']})"

    def test_mape_range(self):
        """MAPE phai nam trong [0, 100] hoac NaN."""
        from src.evaluation.metrics import compute_metrics

        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.1, 1.9, 3.2, 3.8, 5.1])

        metrics = compute_metrics(y_true, y_pred)
        assert 0 <= metrics["mape"] <= 100 or np.isnan(metrics["mape"])


class TestRiskZone:
    """Test risk zone classification."""

    def test_classify_returns_three_values(self):
        """Risk zone chi co 3 gia tri hop le: Normal, Warning, Exceedance."""
        from src.evaluation.risk_zone import classify_risk_zones

        water_levels = np.array([0.5, 0.8, 1.06, 1.1, 1.24, 1.5])
        zones = classify_risk_zones(water_levels, 1.06, 1.24)

        valid_zones = {"Normal", "Warning", "Exceedance"}
        for z in zones:
            assert z in valid_zones, f"Zone khong hop le: {z}"

    def test_classify_correct_mapping(self):
        """Phan loai dung voi nguong."""
        from src.evaluation.risk_zone import classify_risk_zones

        levels = np.array([0.5, 1.06, 1.24, 1.5])
        zones = classify_risk_zones(levels, 1.06, 1.24)

        assert zones[0] == "Normal"
        assert zones[1] == "Warning"
        assert zones[2] == "Exceedance"
        assert zones[3] == "Exceedance"

    def test_risk_metrics_structure(self):
        """compute_risk_zone_metrics tra ve dict day du."""
        from src.evaluation.risk_zone import compute_risk_zone_metrics

        y_true = np.array([0.5, 0.8, 1.1, 1.3])
        y_pred = np.array([0.55, 0.85, 1.15, 1.25])

        metrics = compute_risk_zone_metrics(y_true, y_pred, 1.06, 1.24)

        required_keys = [
            "zone_accuracy", "precision_dangerous", "recall_dangerous",
            "f1_dangerous", "exceedance_recall", "wilson_ci",
            "zone_mae", "zone_counts", "n_total"
        ]
        for key in required_keys:
            assert key in metrics, f"Thieu key: {key}"

    def test_wilson_interval_bounds(self):
        """Wilson CI phai nam trong [0, 1]."""
        from src.evaluation.risk_zone import _wilson_interval

        for k in range(0, 11):
            for n in [10, 50, 100]:
                if k > n:
                    continue
                lo, hi = _wilson_interval(k, n)
                assert 0 <= lo <= 1, f"Wilson lower out of bound: {lo}"
                assert 0 <= hi <= 1, f"Wilson upper out of bound: {hi}"
                assert lo <= hi, f"Wilson lower > upper: {lo} > {hi}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
