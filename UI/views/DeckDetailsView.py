import flet as ft
from UI.theme import *
from data.repository import *
class DeckDetailsView(ft.Container):
    def __init__(self, navigate, * , deck_id):
        super().__init__()
        self._navigate = navigate
        self.deck_id = deck_id
        self.cards = get_cards(deck_id)
        self.cardState = None
        if self.cards == []:
            self.cardState = ft.Text("Pusta talia", size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT)
        else:
            self.cardState = ft.Container(
                content=ft.ListView(
                    controls=[
                        ft.Text(f"{card.front} - {card.back}", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT) for card in self.cards
                    ]
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
                padding=20,
                width=700,
            )
        self.expand = True
        self.content = ft.Column(
            controls=[
                ft.Text(f"Szczegóły talii o ID: {deck_id}", size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=self._go_back),
                self.cardState,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _go_back(self, e):
        from UI.views.DeckView import DeckView
        self._navigate(DeckView)