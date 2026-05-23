import flet as ft
import json
from pathlib import Path

THEMES = {
    "czerwony": ft.Colors.RED_500,
    "zielony": ft.Colors.GREEN_400,
    "różowy": ft.Colors.PINK_400,
    "niebieski": ft.Colors.BLUE_400
}

def load_saved_theme():
    settings_file = Path("data/settings.json")
    if settings_file.exists():
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                theme_name = data.get("theme_color", "czerwony")
                if theme_name in THEMES:
                    return THEMES[theme_name]
        except Exception:
            pass
    return ft.Colors.RED_500

PRIMARY = load_saved_theme()
PRIMARY_TEXT = ft.Colors.WHITE
SECONDARY_TEXT = ft.Colors.BLACK
BG_BUTTON = ft.Colors.GREY_800
SURFACE = ft.Colors.GREY_800
BTN_WIDTH = 250
BG_APP = ft.Colors.BLACK

def set_primary_theme(theme_name):
    import sys
    if theme_name not in THEMES:
        print(f"Theme {theme_name} not found in THEMES")
        return
    
    color_val = THEMES[theme_name]
    global PRIMARY
    PRIMARY = color_val
    print(f"Setting primary theme global to: {theme_name}")
    
    for name, module in list(sys.modules.items()):
        if name.startswith("UI.") or name == "UI":
            if hasattr(module, "PRIMARY"):
                try:
                    setattr(module, "PRIMARY", color_val)
                    print(f"Updated PRIMARY in module: {name} to {theme_name}")
                except Exception as e:
                    print(f"Error setting PRIMARY in {name}: {e}")