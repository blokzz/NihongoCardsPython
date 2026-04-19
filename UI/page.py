import flet as ft
from utils import check_level_up
from UI.views.menu import MenuView

class JapaneseApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.xp = 0
        self.level = 0
        self.setup_page()
        self.navigate(MenuView)

    def setup_page(self):
        self.page.title = "日本語暗記"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def navigate(self, view_class, **kwargs):
        self.page.controls.clear()
        self.page.add(view_class(self.navigate, **kwargs))
        self.page.update()

    @check_level_up
    def add_xp(self, amount: int = 40):
        self.xp += amount

    def show_level_up_dialog(self):
        self.page.snack_bar = ft.SnackBar(ft.Text("おめでとう! Level up!"))
        self.page.snack_bar.open = True
        self.page.update()