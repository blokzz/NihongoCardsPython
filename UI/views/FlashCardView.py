import flet as ft
from UI.components.hoverButton import HoverButton
class FlashcardView(ft.Container):
    def __init__(self, navigate):
        super().__init__()
        self._navigate = navigate
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.content = ft.Column(
            controls=[
                ft.Text("Fiszki", size=40, weight=ft.FontWeight.BOLD),
                HoverButton("Wróć", on_click=self._go_back),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _go_back(self, e):
        from UI.views.menu import MenuView
        self._navigate(MenuView)