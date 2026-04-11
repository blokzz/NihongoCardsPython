import flet as ft

from utils import check_level_up

class JapaneseApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.xp = 0
        self.level = 0
        self.setup_ui()

    def setup_ui(self):
        self.page.title = "日本語暗記"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        self.stats_text = ft.Text(f"Poziom: {self.level} | XP: {self.xp}", size=20)
        self.btn = ft.ElevatedButton("Zaliczone słówko", on_click=self.add_xp)
        
        self.page.add(
            ft.Text("こんにちは", size=40, weight="bold"),
            self.stats_text,
            self.btn
        )

    @check_level_up
    def add_xp(self, e):
        self.xp += 40
        self.stats_text.value = f"Poziom: {self.level} | XP: {self.xp}"
        self.page.update()

    def show_level_up_dialog(self):
        self.page.snack_bar = ft.SnackBar(ft.Text("おめでとう!"))
        self.page.snack_bar.open = True
        self.page.update()