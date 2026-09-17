# -*- coding: utf-8 -*-
"""
Cac ham ve bieu do phuc vu phan tich va trinh bay.
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # Khong can GUI
import numpy as np
import pandas as pd


def plot_mae_comparison(results_df, title="So sanh MAE theo horizon", save_path=None):
    """
    Ve bieu do cot so sanh MAE cua cac mo hinh theo horizon.
    
    Args:
        results_df: DataFrame voi cot: model, horizon, mae
        title: tieu de bieu do
        save_path: duong dan luu hinh (None = hien thi)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    horizons = sorted(results_df["horizon"].unique())
    models = results_df["model"].unique()
    n_models = len(models)
    
    x = np.arange(len(horizons))
    width = 0.8 / n_models
    
    for i, model in enumerate(models):
        model_data = results_df[results_df["model"] == model]
        mae_values = [model_data[model_data["horizon"] == h]["mae"].values[0] 
                      for h in horizons]
        bars = ax.bar(x + i * width, mae_values, width, label=model)
    
    ax.set_xlabel("Horizon")
    ax.set_ylabel("MAE (m)")
    ax.set_title(title)
    ax.set_xticks(x + width * (n_models - 1) / 2)
    ax.set_xticklabels(horizons)
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def plot_feature_importance(importances, feature_names, title="Feature Importance", 
                           top_n=10, save_path=None):
    """
    Ve bieu do cot feature importance.
    
    Args:
        importances: array importance scores
        feature_names: ten cac feature
        title: tieu de
        top_n: so luong feature hien thi
        save_path: duong dan luu hinh
    """
    # Sap xep theo importance giam dan
    indices = np.argsort(importances)[::-1][:top_n]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(range(top_n), importances[indices][::-1])
    ax.set_yticks(range(top_n))
    ax.set_yticklabels([feature_names[i] for i in indices][::-1])
    ax.set_xlabel("Importance")
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def plot_mae_by_noise(noise_results, title="Anh huong nhieu den MAE", save_path=None):
    """
    Ve bieu do so sanh MAE theo muc do nhieu (noise experiment).
    
    Args:
        noise_results: DataFrame voi cot: sigma, model, horizon, mae
        title: tieu de
        save_path: duong dan luu hinh
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)
    horizons = sorted(noise_results["horizon"].unique())
    
    for ax, horizon in zip(axes, horizons):
        h_data = noise_results[noise_results["horizon"] == horizon]
        for model in h_data["model"].unique():
            m_data = h_data[h_data["model"] == model]
            ax.plot(m_data["sigma"], m_data["mae"], marker="o", label=model)
        ax.set_xlabel("Noise σ (m)")
        ax.set_ylabel("MAE (m)")
        ax.set_title(f"t+{horizon}")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
    
    plt.suptitle(title, fontsize=13)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def plot_risk_zone_summary(risk_metrics, save_path=None):
    """
    Ve bieu do tom ket risk-zone evaluation.
    
    Args:
        risk_metrics: dict tu compute_risk_zone_metrics
        save_path: duong dan luu hinh
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Bieu do 1: So mau moi vung
    zones = list(risk_metrics["zone_counts"].keys())
    counts = list(risk_metrics["zone_counts"].values())
    colors = ["#2ecc71", "#f39c12", "#e74c3c"]
    axes[0].bar(zones, counts, color=colors[:len(zones)])
    axes[0].set_ylabel("So ngay")
    axes[0].set_title("Phan bo vung nguy hiem (test set)")
    for i, v in enumerate(counts):
        axes[0].text(i, v + 10, str(v), ha="center", fontsize=11)
    
    # Bieu do 2: MAE theo vung
    mae_vals = [risk_metrics["zone_mae"][z] for z in zones]
    axes[1].bar(zones, mae_vals, color=colors[:len(zones)])
    axes[1].set_ylabel("MAE (m)")
    axes[1].set_title("MAE theo vung")
    for i, v in enumerate(mae_vals):
        axes[1].text(i, v + 0.001, f"{v:.4f}", ha="center", fontsize=10)
    
    plt.suptitle("Risk-Zone Evaluation", fontsize=13)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
    else:
        plt.show()
