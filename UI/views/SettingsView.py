import flet as ft

from UI.views.BaseView import BaseView
from UI.theme import * 

class SettingsView(BaseView):
    def __init__(self, navigate):
        super().__init__(navigate)
        print(f"SettingsView __init__ - PRIMARY: {PRIMARY}")
        self.expand = True
        
        settings = self._load_settings_file()
        self.current_goal = str(settings.get("daily_goal", "10"))
        self.current_order = settings.get("study_order", "Random")
        self.current_theme = settings.get("theme_color", "czerwony")
        
        self.dropdown_goal = ft.Dropdown(
            width=120,
            height=40,
            options=[
                ft.dropdown.Option("5"),
                ft.dropdown.Option("10"),
                ft.dropdown.Option("15"),
                ft.dropdown.Option("20"),
                ft.dropdown.Option("30"),
                ft.dropdown.Option("50"),
            ],
            text_size=14,
            border_radius=8,
            border_color=ft.Colors.GREY_700,
            focused_border_color=PRIMARY,
            bgcolor=BG_BUTTON,
            color=PRIMARY_TEXT,
            value=self.current_goal,
        )
        self.dropdown_goal.on_change = self._on_dropdown_change

        self.dropdown_order = ft.Dropdown(
            width=150,
            height=40,
            options=[
                ft.dropdown.Option("Random", "Losowa"),
                ft.dropdown.Option("Chronological", "Chronologiczna"),
            ],
            text_size=14,
            border_radius=8,
            border_color=ft.Colors.GREY_700,
            focused_border_color=PRIMARY,
            bgcolor=BG_BUTTON,
            color=PRIMARY_TEXT,
            value=self.current_order,
        )
        self.dropdown_order.on_change = self._on_dropdown_change

        theme_options = []
        for name, color in THEMES.items():
            is_active = (self.current_theme == name)
            theme_options.append(
                ft.Container(
                    width=32,
                    height=32,
                    border_radius=16,
                    bgcolor=color,
                    content=ft.Icon(ft.Icons.CHECK, color=ft.Colors.WHITE, size=16) if is_active else None,
                    alignment=ft.Alignment.CENTER,
                    on_click=lambda e, name=name: self._change_theme(name),
                    border=ft.border.all(2, ft.Colors.WHITE) if is_active else None,
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
                )
            )
        self.theme_row = ft.Row(controls=theme_options, spacing=10)

        self.switch_reading = ft.Switch(
            value=settings.get("show_reading", True),
            active_color=PRIMARY,
        )
        self.switch_reading.on_change = self._save_settings_switches

        self.switch_sound = ft.Switch(
            value=settings.get("sound_effects", True),
            active_color=PRIMARY,
        )
        self.switch_sound.on_change = self._save_settings_switches
        
        self.btn_reset = ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.REFRESH_ROUNDED, color=ft.Colors.RED_400, size=18),
                    ft.Text("Reset", color=ft.Colors.RED_400, weight=ft.FontWeight.BOLD, size=14),
                ],
                spacing=5,
            ),
            on_click=self._on_reset_click,
        )

        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=ft.padding.only(top=10, bottom=20, left=20, right=20),
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                                    on_click=self._go_back,
                                    icon_color=PRIMARY_TEXT,
                                    icon_size=20,
                                ),
                                width=100,
                                alignment=ft.Alignment(-1, 0),
                            ),
                            ft.Text(
                                "Settings",
                                size=32,
                                weight=ft.FontWeight.W_900,
                                color=PRIMARY_TEXT,
                                expand=True,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(width=100)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
                
                ft.Container(
                    expand=True,
                    padding=ft.padding.symmetric(horizontal=20),
                    alignment=ft.Alignment(0, -1),
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        width=650,
                        spacing=20,
                        controls=[
                            self.create_setting_card(
                                "Study & Cards",
                                [
                                    self.create_setting_row(
                                        ft.Icons.TRACK_CHANGES_ROUNDED,
                                        "Daily goal",
                                        "Sets the number of new words you want to learn each day.",
                                        self.dropdown_goal
                                    ),
                                    self.create_setting_row(
                                        ft.Icons.SORT_ROUNDED,
                                        "Study Order",
                                        "Decide whether you want to review words randomly or by their creation date.",
                                        self.dropdown_order
                                    ),
                                    self.create_setting_row(
                                        ft.Icons.TRANSLATE_ROUNDED,
                                        "Phonetic transcription (Kana/Romaji)",
                                        "Shows auxiliary reading above Kanji characters.",
                                        self.switch_reading
                                    ),
                                ]
                            ),
                            
                            self.create_setting_card(
                                "Appearance & Sounds",
                                [
                                    self.create_setting_row(
                                        ft.Icons.PALETTE_ROUNDED,
                                        "Primary color",
                                        "Choose the main accent color of the application.",
                                        self.theme_row
                                    ),
                                    self.create_setting_row(
                                        ft.Icons.VOLUME_UP_ROUNDED,
                                        "Sound effects",
                                        "Plays sound confirmations of answers during the learning session.",
                                        self.switch_sound
                                    ),
                                ]
                            ),
                            
                            self.create_setting_card(
                                "Safety & Data",
                                [
                                    self.create_setting_row(
                                        ft.Icons.DELETE_FOREVER_ROUNDED,
                                        "Reset progress",
                                        "Resets all statistics, levels and next review dates.",
                                        self.btn_reset
                                    ),
                                ]
                            ),
                            
                            ft.Container(
                                content=ft.Text(
                                    "Saved settings will be automatically applied.",
                                    size=12,
                                    italic=True,
                                    color=ft.Colors.GREY_500,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                padding=ft.padding.symmetric(vertical=15),
                                alignment=ft.Alignment.CENTER,
                            ),
                        ]
                    )
                )
            ]
        )

    def _load_settings_file(self):
        import json
        from pathlib import Path
        settings_file = Path("data/settings.json")
        default_settings = {
            "daily_goal": "10",
            "study_order": "Random",
            "show_reading": True,
            "sound_effects": True,
            "theme_color": "czerwony"
        }
        if not settings_file.exists():
            return default_settings
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                return {**default_settings, **json.load(f)}
        except Exception:
            return default_settings

    def _save_settings_file(self, settings):
        import json
        from pathlib import Path
        settings_file = Path("data/settings.json")
        try:
            settings_file.parent.mkdir(exist_ok=True)
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving settings file: {e}")

    def did_mount(self):
        pass

    def _save_settings(self):
        settings = {
            "daily_goal": self.current_goal,
            "study_order": self.current_order,
            "show_reading": self.switch_reading.value,
            "sound_effects": self.switch_sound.value,
            "theme_color": self.current_theme
        }
        self._save_settings_file(settings)

    def _save_settings_switches(self, e):
        self._save_settings()
        self.show_success("Settings saved successfully!")

    def _change_theme(self, theme_name):
        self.current_theme = theme_name
        self._save_settings()
        
        from UI.theme import set_primary_theme
        set_primary_theme(theme_name)
        
        self.show_success("Primary color has been changed!")
        self._navigation(SettingsView)

    def _on_dropdown_change(self, e):
        self.current_goal = self.dropdown_goal.value
        self.current_order = self.dropdown_order.value
        self._save_settings()
        self.show_success("Settings saved successfully!")

    def create_setting_card(self, title: str, controls_list: list):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=PRIMARY),
                    ft.Divider(color=ft.Colors.with_opacity(0.1, PRIMARY_TEXT), height=1),
                    *controls_list
                ],
                spacing=15,
            ),
            bgcolor=BG_BUTTON,
            border_radius=15,
            padding=20,
            border=ft.border.only(left=ft.BorderSide(4, PRIMARY)),
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 4)
            )
        )

    def create_setting_row(self, icon: str, name: str, description: str, control: ft.Control):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(icon, color=PRIMARY_TEXT, size=24),
                            bgcolor=ft.Colors.with_opacity(0.05, PRIMARY_TEXT),
                            padding=10,
                            border_radius=10,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(name, size=15, weight=ft.FontWeight.W_600, color=PRIMARY_TEXT),
                                ft.Text(description, size=12, color=ft.Colors.GREY_400, max_lines=2, width=320),
                            ],
                            spacing=2,
                        )
                    ],
                    spacing=15,
                ),
                control
            ]
        )

    def _on_reset_click(self, e):
        from UI.components.BaseDialog import BaseDialog
        
        def close_dialog(e):
            dialog.open = False
            self.page.update()

        def confirm_reset(e):
            from data.database import get_connection
            try:
                with get_connection() as conn:
                    conn.execute("UPDATE user_progress SET xp = 0, level = 0")
                    conn.execute("UPDATE cards SET correct = 0, incorrect = 0, interval = 1, next_review = CURRENT_DATE")
                    conn.commit()
                dialog.open = False
                self.show_success("Wszystkie postępy zostały pomyślnie zresetowane!")
            except Exception as ex:
                dialog.open = False
                self.show_error(f"Błąd podczas resetowania: {ex}")
            self.page.update()

        dialog = BaseDialog(
            title="Potwierdzenie resetu",
            content=ft.Text("Czy na pewno chcesz zresetować wszystkie statystyki nauki? Tej operacji nie można cofnąć.", color=PRIMARY_TEXT),
            actions=[
                ft.TextButton("Anuluj", on_click=close_dialog, style=ft.ButtonStyle(color=ft.Colors.GREY_400)),
                ft.ElevatedButton("Zresetuj", on_click=confirm_reset, bgcolor=ft.Colors.RED_700, color=PRIMARY_TEXT),
            ],
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _go_back(self, e):
        from UI.views.menu import MenuView
        self._navigation(MenuView)