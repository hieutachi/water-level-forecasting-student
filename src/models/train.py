# -*- coding: utf-8 -*-
"""
Huan luyen va quan ly cac mo hinh du bao.
Bao gom: Linear Regression, Ridge, Random Forest, XGBoost, Stacking, AdaptiveStack.
"""
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import (
    RandomForestRegressor, 
    ExtraTreesRegressor,
    HistGradientBoostingRegressor,
    StackingRegressor,
)
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import xgboost as xgb
import lightgbm as lgb


def train_model(X_train, y_train, model_name="linear", **kwargs):
    """
    Huan luyen mot mo hinh theo ten.
    
    Args:
        X_train: ma tran feature
        y_train: vector target
        model_name: ten mo hinh ("linear", "ridge", "rf", "xgboost", "lgbm")
        **kwargs: tham so bo sung cho mo hinh
        
    Returns:
        mo hinh da huan luyen
    """
    models = {
        "linear": LinearRegression,
        "ridge": Ridge,
        "rf": RandomForestRegressor,
        "xgboost": xgb.XGBRegressor,
        "lgbm": lgb.LGBMRegressor,
        "extratrees": ExtraTreesRegressor,
        "histgb": HistGradientBoostingRegressor,
    }
    
    if model_name not in models:
        raise ValueError(f"Mo hinh '{model_name}' khong duoc ho tro. Chon: {list(models.keys())}")
    
    model_class = models[model_name]
    model = model_class(**kwargs)
    model.fit(X_train, y_train)
    
    return model


def train_all_models(X_train, y_train, X_val, y_val, config=None):
    """
    Huan luyen tat ca mo hinh co ban va tra ve dict.
    
    Args:
        X_train, y_train: du lieu huan luyen
        X_val, y_val: du lieu validation
        config: dict cau hinh mo hinh
        
    Returns:
        dict: {model_name: trained_model}
    """
    if config is None:
        config = {}
    
    models = {}
    
    # 1. Linear Regression (baseline tuyen tinh)
    models["Linear Regression"] = train_model(X_train, y_train, "linear")
    
    # 2. Ridge Regression (tuyen tinh co regularization)
    models["Ridge"] = train_model(
        X_train, y_train, "ridge",
        **config.get("ridge", {"alpha": 1.0, "random_state": 42})
    )
    
    # 3. Random Forest
    rf_params = config.get("rf", {
        "n_estimators": 500, "max_depth": 20,
        "min_samples_split": 5, "random_state": 42, "n_jobs": -1
    })
    models["Random Forest"] = train_model(X_train, y_train, "rf", **rf_params)
    
    # 4. XGBoost
    xgb_params = config.get("xgboost", {
        "n_estimators": 500, "max_depth": 8,
        "learning_rate": 0.05, "subsample": 0.8,
        "random_state": 42, "n_jobs": -1,
        "verbosity": 0
    })
    models["XGBoost"] = train_model(X_train, y_train, "xgboost", **xgb_params)
    
    # 5. LightGBM
    lgbm_params = config.get("lgbm", {
        "n_estimators": 500, "max_depth": 8,
        "learning_rate": 0.05, "random_state": 42, "n_jobs": -1,
        "verbose": -1
    })
    models["LightGBM"] = train_model(X_train, y_train, "lgbm", **lgbm_params)
    
    return models


def build_stacking_ensemble(base_models, X_meta, y_meta):
    """
    Xay dung Stacking Ensemble tu cac mo hinh co ban.
    Su dung Ridge lam meta-learner.
    
    Args:
        base_models: dict {name: model} cac mo hinh base
        X_meta: du lieu meta (out-of-fold predictions hoac validation)
        y_meta: target cho meta-learner
        
    Returns:
        tuple: (meta_model, meta_predictions)
    """
    # Tao meta features tu predictions cua cac base model
    meta_features = np.column_stack([
        model.predict(X_meta) for model in base_models.values()
    ])
    
    # Huan luyen meta-learner (Ridge Regression)
    meta_model = Ridge(alpha=1.0)
    meta_model.fit(meta_features, y_meta)
    
    return meta_model


def build_adaptive_stack(X_train, y_train, X_val, y_val, config=None):
    """
    Xay dung AdaptiveStack: ket hop LightGBM, ExtraTrees, HistGB, MLP
    bang Ridge meta-learner (tinh tien cua paper).
    
    Pipeline:
    1. Huan luyen 4 base learner tren tap train
    2. Lay predictions tren tap val
    3. Huan luyen Ridge meta-learner tren val predictions
    4. Danh gia tren tap test
    
    Args:
        X_train, y_train: du lieu huan luyen
        X_val, y_val: du lieu validation
        config: cau hinh mo hinh
        
    Returns:
        tuple: (adaptive_stack_model, base_models_dict)
    """
    if config is None:
        config = {}
    
    # 4 base learner
    base_models = {}
    
    # LightGBM
    lgbm_params = config.get("lgbm", {
        "n_estimators": 500, "max_depth": 8, "learning_rate": 0.05,
        "random_state": 42, "n_jobs": -1, "verbose": -1
    })
    base_models["LightGBM"] = lgb.LGBMRegressor(**lgbm_params)
    base_models["LightGBM"].fit(X_train, y_train)
    
    # ExtraTrees
    et_params = config.get("extratrees", {
        "n_estimators": 500, "max_depth": 20, "random_state": 42, "n_jobs": -1
    })
    base_models["ExtraTrees"] = ExtraTreesRegressor(**et_params)
    base_models["ExtraTrees"].fit(X_train, y_train)
    
    # HistGradientBoosting
    hgb_params = config.get("histgb", {
        "max_depth": 8, "learning_rate": 0.05, "random_state": 42
    })
    base_models["HistGradientBoosting"] = HistGradientBoostingRegressor(**hgb_params)
    base_models["HistGradientBoosting"].fit(X_train, y_train)
    
    # MLP (can standardize input)
    mlp_params = config.get("mlp", {
        "hidden_layer_sizes": (128, 64), "activation": "relu",
        "solver": "adam", "max_iter": 500, "random_state": 42,
        "early_stopping": True
    })
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    base_models["MLP"] = MLPRegressor(**mlp_params)
    base_models["MLP"].fit(X_train_scaled, y_train)
    
    # Lay predictions tren tap val de huan luyen meta-learner
    val_preds = np.column_stack([
        base_models["LightGBM"].predict(X_val),
        base_models["ExtraTrees"].predict(X_val),
        base_models["HistGradientBoosting"].predict(X_val),
        base_models["MLP"].predict(X_val_scaled),
    ])
    
    # Ridge meta-learner
    meta_model = Ridge(alpha=1.0)
    meta_model.fit(val_preds, y_val)
    
    # Tao wrapper de predict tu test set
    class AdaptiveStack:
        """Wrapper cho AdaptiveStack ensemble."""
        def __init__(self, base_models, meta_model, scaler):
            self.base_models = base_models
            self.meta_model = meta_model
            self.scaler = scaler
        
        def predict(self, X):
            preds = np.column_stack([
                self.base_models["LightGBM"].predict(X),
                self.base_models["ExtraTrees"].predict(X),
                self.base_models["HistGradientBoosting"].predict(X),
                self.base_models["MLP"].predict(self.scaler.transform(X)),
            ])
            return self.meta_model.predict(preds)
    
    adaptive_model = AdaptiveStack(base_models, meta_model, scaler)
    
    return adaptive_model, base_models
