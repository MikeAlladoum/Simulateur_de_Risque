"""
Helpers - Fonctions utilitaires
"""

import json
from typing import Any


def to_json(obj: Any) -> str:
    """Convertit un objet en JSON"""
    if hasattr(obj, 'to_dict'):
        return json.dumps(obj.to_dict())
    return json.dumps(obj, default=str)


def format_number(num: float, decimals: int = 2) -> float:
    """Formate un nombre avec un nombre de décimales"""
    return round(num, decimals)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Limite une valeur entre min et max"""
    return max(min_val, min(value, max_val))
