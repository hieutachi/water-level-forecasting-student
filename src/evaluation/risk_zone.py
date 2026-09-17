# -*- coding: utf-8 -*-
"""
Phan loai va danh gia theo vung nguy hiem (Risk-zone evaluation).
Phan loai: Normal / Warning / Exceedance.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def classify_risk_zones(water_levels, warning_threshold=1.06, exceedance_threshold=1.24):
    """
    Phan loai muc nuoc thanh 3 vung nguy hiem.
    
    Dinh nghia:
    - Normal:     WL < warning_threshold (P95 = 1.06 m)
    - Warning:    warning_threshold <= WL < exceedance_threshold
    - Exceedance: WL >= exceedance_threshold (P99 = 1.24 m)
    
    Nguong duoc tinh tren tap train 28 nam (1990-2017).
    
    Args:
        water_levels: array gia tri muc nuoc
        warning_threshold: nguong canh bao (P95)
        exceedance_threshold: nguong vuot (P99)
        
    Returns:
        array: labels ["Normal", "Warning", "Exceedance"]
    """
    water_levels = np.asarray(water_levels, dtype=float)
    zones = np.full(len(water_levels), "Normal", dtype=object)
    zones[water_levels >= warning_threshold] = "Warning"
    zones[water_levels >= exceedance_threshold] = "Exceedance"
    return zones


def compute_risk_zone_metrics(y_true, y_pred, warning_threshold=1.06, exceedance_threshold=1.24):
    """
    Tinh cac metric danh gia cho vung nguy hiem.
    
    Bao gom:
    - Accuracy 3 vung (3-zone accuracy)
    - Precision, Recall, F1 cho lop "dangerous" (Warning + Exceedance)
    - Recall rieng cho lop "Exceedance"
    - Wilson 95% CI cho Exceedance recall
    - MAE theo tung vung
    - So mau moi vung
    
    Args:
        y_true: gia tri muc nuoc thuc te
        y_pred: gia tri muc nuoc du bao
        warning_threshold: nguong canh bao
        exceedance_threshold: nguong vuot
        
    Returns:
        dict chua cac metric
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    
    # Phan loai theo vung
    true_zones = classify_risk_zones(y_true, warning_threshold, exceedance_threshold)
    pred_zones = classify_risk_zones(y_pred, warning_threshold, exceedance_threshold)
    
    # 3-zone accuracy
    zone_accuracy = accuracy_score(true_zones, pred_zones)
    
    # Tao label binary: "dangerous" (Warning hoac Exceedance) vs "Normal"
    true_dangerous = np.isin(true_zones, ["Warning", "Exceedance"]).astype(int)
    pred_dangerous = np.isin(pred_zones, ["Warning", "Exceedance"]).astype(int)
    
    # Precision, Recall, F1 cho lop dangerous
    precision = precision_score(true_dangerous, pred_dangerous, zero_division=0)
    recall = recall_score(true_dangerous, pred_dangerous, zero_division=0)
    f1 = f1_score(true_dangerous, pred_dangerous, zero_division=0)
    
    # Recall rieng cho lop Exceedance
    true_exceed = (true_zones == "Exceedance").astype(int)
    pred_exceed = (pred_zones == "Exceedance").astype(int)
    exceedance_recall = recall_score(true_exceed, pred_exceed, zero_division=0)
    
    # Wilson 95% CI cho Exceedance recall
    n_exceed = true_exceed.sum()
    k_exceed = (true_exceed & pred_exceed).sum()
    wilson_low, wilson_high = _wilson_interval(k_exceed, n_exceed)
    
    # MAE theo tung vung
    zone_mae = {}
    zone_counts = {}
    for zone in ["Normal", "Warning", "Exceedance"]:
        mask = true_zones == zone
        zone_counts[zone] = int(mask.sum())
        if mask.sum() > 0:
            zone_mae[zone] = np.mean(np.abs(y_true[mask] - y_pred[mask]))
        else:
            zone_mae[zone] = np.nan
    
    return {
        "zone_accuracy": zone_accuracy,
        "precision_dangerous": precision,
        "recall_dangerous": recall,
        "f1_dangerous": f1,
        "exceedance_recall": exceedance_recall,
        "wilson_ci": (wilson_low, wilson_high),
        "zone_mae": zone_mae,
        "zone_counts": zone_counts,
        "n_total": len(y_true),
    }


def _wilson_interval(k, n, z=1.96):
    """
    Wilson score interval cho binomial proportion.
    
    Args:
        k: so lan thanh cong
        n: tong so mau
        z: z-score cho CI (1.96 cho 95%)
        
    Returns:
        (lower, upper)
    """
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    spread = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return (max(0, center - spread), min(1, center + spread))
