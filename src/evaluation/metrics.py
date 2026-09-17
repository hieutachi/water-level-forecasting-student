# -*- coding: utf-8 -*-
"""
Tinh cac metric danh gia: MAE, RMSE, MAPE, R2.
"""
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute_metrics(y_true, y_pred):
    """
    Tinh tat ca metric danh gia.
    
    Args:
        y_true: gia tri thuc te
        y_pred: gia tri du bao
        
    Returns:
        dict: {"mae": float, "rmse": float, "mape": float, "r2": float}
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    
    # MAPE: tranh chia cho 0
    mask = y_true != 0
    if mask.sum() > 0:
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    else:
        mape = np.nan
    
    r2 = r2_score(y_true, y_pred)
    
    return {"mae": mae, "rmse": rmse, "mape": mape, "r2": r2}


def evaluate_all_horizons(y_true_dict, y_pred_dict):
    """
    Danh gia cho tat ca horizon.
    
    Args:
        y_true_dict: {"t+1": array, "t+3": array, "t+7": array}
        y_pred_dict: {"t+1": array, "t+3": array, "t+7": array}
        
    Returns:
        DataFrame voi ket qua cho moi horizon
    """
    import pandas as pd
    
    results = []
    for horizon in sorted(y_true_dict.keys()):
        metrics = compute_metrics(y_true_dict[horizon], y_pred_dict[horizon])
        metrics["horizon"] = horizon
        results.append(metrics)
    
    return pd.DataFrame(results)


def compute_wilcoxon_test(errors_a, errors_b):
    """
    Test Wilcoxon signed-rank de so sanh 2 mo hinh.
    
    Args:
        errors_a: array sai so tuyet doi cua mo hinh A
        errors_b: array sai so tuyet doi cua mo hinh B
        
    Returns:
        (statistic, p_value)
    """
    from scipy.stats import wilcoxon
    try:
        stat, p = wilcoxon(errors_a, errors_b)
        return stat, p
    except ValueError:
        return np.nan, np.nan
