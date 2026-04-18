import flet as ft

from UI.components.flashcard import Flashcard
from utils import check_level_up
from UI.views.menu import MenuView

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
        self.page.add(MenuView(self.page))
        # self.page.add(
        #     Flashcard(self.page, "私", "わたし").view
        # )
        self.page.update()

    @check_level_up
    def add_xp(self, e):
        self.xp += 40
        self.stats_text.value = f"Poziom: {self.level} | XP: {self.xp}"
        self.page.update()

    def show_level_up_dialog(self):
        self.page.snack_bar = ft.SnackBar(ft.Text("おめでとう!"))
        self.page.snack_bar.open = True
        self.page.update()