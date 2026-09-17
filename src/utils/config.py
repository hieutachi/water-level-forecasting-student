# -*- coding: utf-8 -*-
"""
Load cau hinh tu file YAML.
"""
import yaml
from pathlib import Path


def load_config(config_path=None):
    """
    Load cau hinh tu file config.yaml.
    
    Args:
        config_path: duong dan den file cau hinh. Neu None, dung mac dinh.
        
    Returns:
        dict cau hinh
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "configs" / "config.yaml"
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
