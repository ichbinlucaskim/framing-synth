import pytest


@pytest.fixture
def solid_panel():
    """3000mm x 2438mm exterior load-bearing panel, no openings."""
    return {
        "schema_version": "0.1.0",
        "id": "panel-001",
        "parent_wall": "wall-001",
        "start": {"x": 0, "y": 0},
        "end": {"x": 3000, "y": 0},
        "length": 3000,
        "height": 2438,
        "openings": [],
        "panel_type": "exterior",
        "load_bearing": True,
    }


@pytest.fixture
def window_panel():
    """3000mm panel with a 1200mm window centred at 1500mm."""
    panel = {
        "schema_version": "0.1.0",
        "id": "panel-002",
        "parent_wall": "wall-002",
        "start": {"x": 0, "y": 0},
        "end": {"x": 3000, "y": 0},
        "length": 3000,
        "height": 2438,
        "openings": ["window_0"],
        "panel_type": "exterior",
        "load_bearing": True,
    }
    openings = {
        "window_0": {
            "schema_version": "0.1.0",
            "id": "window_0",
            "type": "window",
            "host_wall": "wall-002",
            "position": 1500,
            "width": 1200,
            "height": 1200,
            "swing_direction": "none",
        }
    }
    return panel, openings
