# -*- coding: utf-8 -*-
"""
Doc va chuan bi du lieu tu file CSV (output MIKE11).
"""
import pandas as pd
import numpy as np
import yaml
from pathlib import Path


def load_config():
    """Load cau hinh tu file config.yaml."""
    config_path = Path(__file__).parent.parent.parent / "configs" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_raw_data(filepath=None):
    """
    Doc du lieu tu file CSV.
    
    Du lieu goc la output mo phong MIKE11, bao gom:
    - Bien tren 1: dong song Ha Coi (m3/s)
    - Bien tren 2: dong song Tai Chi (m3/s)
    - Bien duoi: muc nuoc bien/muc nuoc duoi (m)
    - Ket qua HACOI: muc nuoc tai Quang Ha (m)
    
    Returns:
        pd.DataFrame voi cac cot: date, river_flow_a, river_flow_b, 
                                   sea_level, water_level
    """
    if filepath is None:
        config = load_config()
        filepath = config["data"]["raw_path"]
    
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(
            f"Khong tim thay file du lieu: {filepath}\n"
            "Hay chac chan ban da copy file CSV vao thu muc data/raw/"
        )
    
    df = pd.read_csv(filepath)
    
    # Doi ten cot sang tieng Anh cho de su dung
    col_map = {
        "Date Time": "date",
        "Bien tren 1 (m3/s)": "river_flow_a",
        "Bien tren 2(m3/s)": "river_flow_b",
        "Bien duoi (m)": "sea_level",
        "Ket qua HACOI 4985.68 (m)": "water_level",
    }
    df = df.rename(columns=col_map)
    
    # Chuyen cot date sang datetime
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y %H:%M")
    df = df.set_index("date").sort_index()
    
    # Chuyen sang daily (trung binh theo ngay)
    df = df.resample("D").mean()
    
    # Xu ly gia tri thieu (neu co)
    df = df.dropna()
    
    return df


def create_temporal_split(df, train_end=None, val_end=None):
    """
    Chia du lieu theo thoi gian (temporal split) de tranh data leakage.
    
    Tap train: 1990 - 2017 (28 nam)
    Tap val:   2018 - 2019 (2 nam)
    Tap test:  2020 - 2021 (2 nam)
    
    Ly do khong dung random split: du lieu thoi gian co tinh lien tuc,
    random split se gay data leakage (leak tuong lai vao huan luyen).
    
    Args:
        df: DataFrame voi datetime index
        train_end: ngay ket thuc tap train
        val_end: ngay ket thuc tap val
        
    Returns:
        dict voi cac key: train, val, test
    """
    config = load_config()
    
    if train_end is None:
        train_end = config["split"]["train_end"]
    if val_end is None:
        val_end = config["split"]["val_end"]
    
    train = df.loc[:train_end].copy()
    val = df.loc[train_end:val_end].copy()
    test = df.loc[val_end:].copy()
    
    # Loai bo dong overlap giua cac tap (do inclusive indexing)
    val = val.iloc[1:]  # bo dong dau tien (trung voi train_end)
    test = test.iloc[1:]  # bo dong dau tien (trung voi val_end)
    
    return {"train": train, "val": val, "test": test}


def prepare_targets(df, horizons=None):
    """
    Tao cot target cho moi horizon: water_level_t1, water_level_t3, water_level_t7.
    
    Args:
        df: DataFrame voi cot water_level
        horizons: list cac buoc nhin truoc (mac dinh: [1, 3, 7])
        
    Returns:
        DataFrame voi cac cot target moi
    """
    if horizons is None:
        config = load_config()
        horizons = config["horizons"]
    
    result = df.copy()
    for h in horizons:
        result[f"water_level_t{h}"] = result["water_level"].shift(-h)
    
    return result
