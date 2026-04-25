"""
Converters - Conversion de formats
"""

import json
from typing import Dict, Any


def json_to_dict(json_str: str) -> Dict[str, Any]:
    """Convertit JSON en dictionnaire"""
    return json.loads(json_str)


def dict_to_json(data: Dict[str, Any]) -> str:
    """Convertit dictionnaire en JSON"""
    return json.dumps(data)
