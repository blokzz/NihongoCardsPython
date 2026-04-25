import flet as ft
from UI.theme import *
from data.models import Deck
from UI.views.DeckDetailsView import DeckDetailsView
class DeckCard(ft.Container):
    def __init__(self, deck: Deck, navigate):
        super().__init__()
        self.deck = deck
        self.navigate = navigate
        self.bgcolor = BG_BUTTON
        self.border_radius = 10
        self.padding = 30
        self.width = BTN_WIDTH
        self.height = 100
        self.content = ft.Column(
            controls=[
                ft.Text(deck.name, size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.on_click = self._on_click
    def _on_click(self, e):
        print(f"Wybrano talię: {self.deck.name}")
        self.navigate(DeckDetailsView, deck_id=self.deck.id)