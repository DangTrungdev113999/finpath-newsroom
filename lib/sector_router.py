"""Sector code → master agent routing.

Source of truth: data/sector_routing.yaml.
Edit YAML to promote sector or add new mapping.
"""
from pathlib import Path
import yaml

ROUTING_FILE = Path(__file__).parent.parent / "data" / "sector_routing.yaml"


class MasterRouteError(ValueError):
    """Raised when sector_code không có trong sector_routing.yaml."""


def get_master_route(sector_code: str) -> str:
    """Map sector_code → master_name. Fail-loud if unmapped.

    Returns master name (lowercase, used in newsroom-master-{name} agent).
    """
    config = _load_routing()
    routing = config.get("routing", {})
    if sector_code not in routing:
        raise MasterRouteError(
            f"sector_code '{sector_code}' chưa map trong {ROUTING_FILE}. "
            f"Add entry to routing dict hoặc check Finpath API có sector mới."
        )
    return routing[sector_code]


def _load_routing() -> dict:
    """Read YAML config. Cached not needed — Python re-reads small file fast."""
    with open(ROUTING_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)
