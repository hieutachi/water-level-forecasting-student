# -*- coding: utf-8 -*-
"""
Feature engineering cho bai toan du bao muc nuoc.
Tao 5 nhom dac trung: lag, rolling, seasonal, interaction, risk.
"""
import pandas as pd
import numpy as np


def create_lag_features(df, columns=None, lag_periods=None):
    """
    Nhom 1: Lag features - Gia tri muc nuoc/dong chay truoc do.
    
    Y nghia thuy van:
    - water_level_lag_1: tinh tru luc (persistence) cua muc nuoc
    - water_level_lag_7/14: nho chu ky trieu nua thang (~14.76 ngay)
    - river_flow_lag: thoi gian di chuyen dong chay tu dau nguon
    - sea_level_lag: anh huong trieu cham
    """
    if columns is None:
        columns = ["water_level", "river_flow_a", "river_flow_b", "sea_level"]
    if lag_periods is None:
        lag_periods = [1, 2, 3, 5, 7, 10, 14, 21, 28, 30, 35, 42, 60]
    
    result = df.copy()
    for col in columns:
        for lag in lag_periods:
            result[f"{col}_lag_{lag}"] = result[col].shift(lag)
    
    return result


def create_rolling_features(df, windows=None, stats=None):
    """
    Nhom 2: Rolling features - Trung binh/truong binh/don bay cua cua so truot.
    
    Y nghia thuy van:
    - rolling_mean: xu huong ngan han (3, 7 ngay)
    - rolling_std: bien dong muc nuoc (do khong on dinh)
    - rolling_min/max: cuc tri trong cua so
    - cumulative_flow: tong luong luu luuy 7 ngay (phan anh lu luong)
    """
    if windows is None:
        windows = [3, 7, 14, 30]
    if stats is None:
        stats = ["mean", "std", "min", "max"]
    
    result = df.copy()
    
    for w in windows:
        for stat in stats:
            result[f"rolling_{stat}_{w}"] = result["water_level"].rolling(window=w).agg(stat)
    
    # Rolling features cho sea_level
    for w in windows:
        result[f"sea_rolling_mean_{w}"] = result["sea_level"].rolling(window=w).mean()
        result[f"sea_rolling_std_{w}"] = result["sea_level"].rolling(window=w).std()
    
    # Cumulative flow (tong dong chay 7 ngay)
    result["cumulative_flow_7d"] = (
        (result["river_flow_a"] + result["river_flow_b"]).rolling(window=7).sum()
    )
    
    return result


def create_seasonal_features(df, tidal_period=14.76):
    """
    Nhom 3: Seasonal features - Mua va chu ky trieu.
    
    Y nghia thuy van:
    - month_sin/cos: phan anh mua (mua lu vs mua kho)
    - day_of_year_sin/cos: phan anh chu ky nam
    - tidal_cycle_sin/cos: ma hoa chu ky trieu (~14.76 ngay)
      Dung de giup mo hinh hieu chu ky spring-neap
    """
    result = df.copy()
    
    # Encode mua bang sin/cos (de giu tinh lien tuc)
    result["month"] = result.index.month
    result["month_sin"] = np.sin(2 * np.pi * result["month"] / 12)
    result["month_cos"] = np.cos(2 * np.pi * result["month"] / 12)
    
    # Encode ngay trong nam
    result["day_of_year"] = result.index.dayofyear
    result["day_of_year_sin"] = np.sin(2 * np.pi * result["day_of_year"] / 365.25)
    result["day_of_year_cos"] = np.cos(2 * np.pi * result["day_of_year"] / 365.25)
    
    # Encode chu ky trieu (dung so ngay tu dau du lieu de ma hoa)
    days_since_start = (result.index - result.index[0]).days
    result["tidal_cycle_sin"] = np.sin(2 * np.pi * days_since_start / tidal_period)
    result["tidal_cycle_cos"] = np.cos(2 * np.pi * days_since_start / tidal_period)
    
    return result


def create_interaction_features(df):
    """
    Nhom 4: Interaction features - Tuong tac song - trieu.
    
    Y nghia thuy van:
    - total_flow: tong luong luu 2 nhanh song (Ha Coi + Tai Chi)
    - flow_A_ratio: ty le dong chay Ha Coi (phan anh nguon chinh)
    - sea_river_diff: hieu muc nuoc bien - muc nuoc song (ap luc trieu)
    - flood_pressure: ap luc luu khi cao dong chay + cao trieu
    """
    result = df.copy()
    
    result["total_flow"] = result["river_flow_a"] + result["river_flow_b"]
    result["flow_A_ratio"] = result["river_flow_a"] / (result["total_flow"] + 1e-8)
    result["sea_river_diff"] = result["sea_level"] - result["water_level"]
    
    # Ap luc luu: dong chay cao va muc nuoc bien cao
    result["flood_pressure"] = (
        (result["total_flow"] - result["total_flow"].mean()) / (result["total_flow"].std() + 1e-8)
    ) + (
        (result["sea_level"] - result["sea_level"].mean()) / (result["sea_level"].std() + 1e-8)
    )
    
    return result


def create_risk_features(df, warning_threshold=1.06, exceedance_threshold=1.24):
    """
    Nhom 5: Risk features - Tinh nang lien quan den canh bao.
    
    Y nghia thuy van:
    - distance_to_threshold: khoang cach den nguong canh bao P95
    - delta_1: thay doi muc nuoc trong 1 ngay (tang/giam)
    - acceleration: gia toc thay doi (phat hien xu huong tich cuc)
    - is_rising: muc nuoc dang tang hay giam
    - danger_flag: co canh bao khi gan nguong nguy hiem
    """
    result = df.copy()
    
    result["distance_to_threshold"] = warning_threshold - result["water_level"]
    
    # Delta: thay doi muc nuoc 1 ngay
    result["delta_1"] = result["water_level"].diff(1)
    
    # Acceleration: thay doi cua delta (derivative bac 2)
    result["acceleration"] = result["delta_1"].diff(1)
    
    # Muc nuoc dang tang (1) hay giam (0)
    result["is_rising"] = (result["delta_1"] > 0).astype(int)
    
    # Co canh bao khi gan nguong
    result["danger_flag"] = (result["water_level"] > warning_threshold * 0.9).astype(int)
    
    return result


def build_all_features(df, warning_threshold=1.06, exceedance_threshold=1.24, tidal_period=14.76):
    """
    Xay dung toan bo 5 nhom dac trung va gop lai.
    
    Returns:
        DataFrame voi tat ca cac feature
    """
    result = df.copy()
    result = create_lag_features(result)
    result = create_rolling_features(result)
    result = create_seasonal_features(result, tidal_period=tidal_period)
    result = create_interaction_features(result)
    result = create_risk_features(result, warning_threshold, exceedance_threshold)
    
    # Xoa dong co NaN (do lag/rolling)
    # Khong xoa ngay lap tuc, de viec tach target xu ly
    return result


def get_feature_groups():
    """
    Tra ve dict cac feature theo nhom, dung cho ablation study.
    
    Returns:
        dict: {group_name: [list of feature patterns]}
    """
    return {
        "lag": [f for f in _all_lag_features()],
        "rolling": [f for f in _all_rolling_features()],
        "seasonal": [
            "month_sin", "month_cos", 
            "day_of_year_sin", "day_of_year_cos",
            "tidal_cycle_sin", "tidal_cycle_cos",
        ],
        "interaction": ["total_flow", "flow_A_ratio", "sea_river_diff", "flood_pressure"],
        "risk": ["distance_to_threshold", "delta_1", "acceleration", "is_rising", "danger_flag"],
    }


def _all_lag_features():
    """Danh sach tat ca lag feature."""
    cols = ["water_level", "river_flow_a", "river_flow_b", "sea_level"]
    lags = [1, 2, 3, 5, 7, 10, 14, 21, 28, 30, 35, 42, 60]
    return [f"{c}_lag_{l}" for c in cols for l in lags]


def _all_rolling_features():
    """Danh sach tat ca rolling feature."""
    windows = [3, 7, 14, 30]
    stats = ["mean", "std", "min", "max"]
    feats = [f"rolling_{s}_{w}" for w in windows for s in stats]
    feats += [f"sea_rolling_mean_{w}" for w in windows]
    feats += [f"sea_rolling_std_{w}" for w in windows]
    feats += ["cumulative_flow_7d"]
    return feats


def select_features_by_correlation(X_train, y_train, threshold_high=0.95, threshold_low=0.05):
    """
    Chon feature bang Spearman correlation:
    - Loai bo cap feature co |rho| > 0.95 (giu cai lien quan den target hon)
    - Loai bo feature co |rho voi target| < 0.05
    
    Args:
        X_train: ma tran feature tap train
        y_train: vector target tap train
        threshold_high: nguong loai bo cap tuong quan cao
        threshold_low: nguong loai bo feature yeu
        
    Returns:
        list ten feature duoc giu lai
    """
    # Tinh Spearman correlation giua cac feature va target
    df_corr = X_train.copy()
    df_corr["target"] = y_train
    corr_matrix = df_corr.corr(method="spearman")
    
    # Tinh tuong quan voi target
    target_corr = corr_matrix["target"].drop("target").abs()
    
    # Loai bo feature co tuong quan voi target qua thap
    weak_features = target_corr[target_corr < threshold_low].index.tolist()
    
    # Loai bo cap feature tuong quan cao
    feature_corr = corr_matrix.drop("target", axis=0).drop("target", axis=1).abs()
    to_drop = set()
    for i in range(len(feature_corr.columns)):
        for j in range(i + 1, len(feature_corr.columns)):
            if feature_corr.iloc[i, j] > threshold_high:
                feat_i = feature_corr.columns[i]
                feat_j = feature_corr.columns[j]
                # Giu lai cai co tuong quan cao hon voi target
                if target_corr.get(feat_i, 0) < target_corr.get(feat_j, 0):
                    to_drop.add(feat_i)
                else:
                    to_drop.add(feat_j)
    
    # Ket qua: cac feature con lai
    all_features = X_train.columns.tolist()
    selected = [f for f in all_features if f not in to_drop and f not in weak_features]
    
    return selected
