# -*- coding: utf-8 -*-
"""
Tao du lieu gia lap (synthetic data) co cau trung giong du lieu MIKE11.
Su dung khi sinh vien khong co du lieu that.

Du lieu that co cau truc:
- Date, river_flow_a (m3/s), river_flow_b (m3/s), sea_level (m), water_level (m)
- 32 nam (1990-2021), daily resolution

Du lieu gia lap nay tao ra chuoi thoi gian voi:
- Chu ky trieu ~14.76 ngay (spring-neap cycle)
- Mua lu (thang 6-10) co dong chay cao hon
- Tuong quan giua bien trieu va muc nuoc dia phuong
"""
import numpy as np
import pandas as pd
from pathlib import Path


def generate_synthetic_data(start_date="1990-01-01", end_date="2021-12-31", seed=42):
    """
    Tao du lieu gia lap co cau trung giong MIKE11.
    
    Args:
        start_date: ngay bat dau
        end_date: ngay ket thuc
        seed: random seed
        
    Returns:
        pd.DataFrame voi cac cot: river_flow_a, river_flow_b, sea_level, water_level
    """
    rng = np.random.default_rng(seed)
    
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    n = len(dates)
    t = np.arange(n)
    
    # === 1. Sea level (muc nuoc bien/trieu) ===
    # Chu ky trieu chinh: ~14.76 ngay (spring-neap)
    tidal_main = 0.8 * np.sin(2 * np.pi * t / 14.76)
    # Chu ky nua ngay (~12.42 gio) - aggregate thanh daily nen nho hon
    tidal_semi = 0.15 * np.sin(2 * np.pi * t / 0.52)
    # Mua: muc nuoc bien cao hon vao mua he
    month = dates.month
    seasonal_sea = 0.1 * np.sin(2 * np.pi * (month - 6) / 12)
    # Nhieu
    noise_sea = rng.normal(0, 0.02, n)
    sea_level = tidal_main + tidal_semi + seasonal_sea + noise_sea + 0.3
    
    # === 2. River flow A (Ha Coi - nhanh chinh) ===
    # Dong chay co ban
    base_flow_a = 5.0
    # Mua lu (thang 6-10): tang dong chay
    seasonal_flow_a = 3.0 * np.maximum(0, np.sin(2 * np.pi * (month - 4) / 12))
    # Nhieu ngau nhien (dac biet vao mua lu)
    noise_flow_a = rng.exponential(1.0, n) * (1 + 0.5 * (month >= 6) * (month <= 10))
    river_flow_a = base_flow_a + seasonal_flow_a + noise_flow_a
    river_flow_a = np.maximum(river_flow_a, 0.1)  # khong am
    
    # === 3. River flow B (Tai Chi - nhanh phu) ===
    base_flow_b = 2.0
    seasonal_flow_b = 1.5 * np.maximum(0, np.sin(2 * np.pi * (month - 4) / 12))
    noise_flow_b = rng.exponential(0.5, n) * (1 + 0.3 * (month >= 6) * (month <= 10))
    river_flow_b = base_flow_b + seasonal_flow_b + noise_flow_b
    river_flow_b = np.maximum(river_flow_b, 0.0)
    
    # === 4. Water level (muc nuoc tai Quang Ha) ===
    # Phu thuoc vao: dong chay, trieu, mua
    # Mo hinh don gian: WL = alpha * sea_level + beta * flow + seasonal + noise
    water_level = (
        0.6 * sea_level  # anh huong trieu (chinh)
        + 0.002 * river_flow_a  # anh huong dong chay
        + 0.001 * river_flow_b
        + 0.05 * np.sin(2 * np.pi * (month - 7) / 12)  # mua
        + rng.normal(0, 0.01, n)  # nhieu
        + 0.2  # baseline
    ).copy()
    
    # Them su kien cuc tri (extreme events) - it xay ra
    n_extreme = int(0.003 * n)  # ~0.3% ngay la extreme
    extreme_idx = rng.choice(n, n_extreme, replace=False)
    water_level = np.array(water_level, dtype=float)
    water_level[extreme_idx] += rng.uniform(0.3, 0.8, n_extreme)
    
    # Tao DataFrame
    df = pd.DataFrame({
        "river_flow_a": river_flow_a,
        "river_flow_b": river_flow_b,
        "sea_level": sea_level,
        "water_level": water_level,
    }, index=dates)
    df.index.name = "date"
    
    return df


def save_synthetic_csv(output_path, start_date="1990-01-01", end_date="2021-12-31"):
    """
    Tao va luu du lieu gia lap thanh file CSV.
    Cau truc giong du lieu MIKE11 that.
    
    Args:
        output_path: duong dan file CSV output
    """
    df = generate_synthetic_data(start_date, end_date)
    
    # Dinh dang giong du lieu that
    df_out = df.copy()
    df_out.index = df_out.index.strftime("%m/%d/%Y %H:%M")
    df_out.index.name = "Date Time"
    df_out = df_out.rename(columns={
        "river_flow_a": "Bien tren 1 (m3/s)",
        "river_flow_b": "Bien tren 2(m3/s)",
        "sea_level": "Bien duoi (m)",
        "water_level": "Ket qua HACOI 4985.68 (m)",
    })
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(output_path)
    
    print(f"Da tao du lieu gia lap: {output_path}")
    print(f"  So ngay: {len(df_out)}")
    print(f"  Thoi gian: {df_out.index[0]} -> {df_out.index[-1]}")
    print(f"  Cot: {list(df_out.columns)}")
    
    return df_out


if __name__ == "__main__":
    # Tao du lieu va luu vao data/raw/
    output_path = Path(__file__).parent.parent / "data" / "raw" / "Dulieughep.csv"
    save_synthetic_csv(output_path)
