import flet as ft
from UI.theme import *
class DeckDetailsView(ft.Container):
    def __init__(self, navigate, * , deck_id):
        super().__init__()
        self._navigate = navigate
        self.deck_id = deck_id
        self.expand = True
        self.content = ft.Column(
            controls=[
                ft.Text(f"Szczegóły talii o ID: {deck_id}", size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=self._go_back),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _go_back(self, e):
        from UI.views.DeckView import DeckView
        self._navigate(DeckView)