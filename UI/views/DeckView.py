import flet as ft
from UI.components.DeckCard import DeckCard
from UI.theme import *
from data.models import Deck
class DeckView(ft.Container):
    def __init__(self, navigate):
        super().__init__()
        self._navigation = navigate
        self.expand = True
        self.decks = [
            Deck(id=1, name="Test"),
            Deck(id=2, name="Test2"),
            Deck(id=3, name="Test3"),
        ]
        self.content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=self._go_back,
                            icon_color=PRIMARY_TEXT,
                        ),
                        ft.Text("Decks", size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
                    ],
                ),
                ft.Row(
                    controls=[DeckCard(deck) for deck in self.decks],
                    wrap=True,
                    spacing=20,
                    run_spacing=20,
                ),
            ],
        )

    def _go_back(self, e):
        from UI.views.menu import MenuView
        self._navigation(MenuView)