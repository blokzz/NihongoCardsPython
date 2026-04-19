import flet as ft
from UI.components.hoverButton import HoverButton
class FlashcardView(ft.Column):
    def __init__(self, navigate):
        super().__init__()
        self._navigate = navigate
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [
            ft.Text("Fiszki", size=40, weight=ft.FontWeight.BOLD),
            HoverButton("Wróć", on_click=self._go_back),
        ]

    def _go_back(self, e):
        from UI.views.menu import MenuView
        self._navigate(MenuView)