import flet as ft
from UI.theme import *
from data.models import Card
class CardDetails(ft.Container):
    def __init__(self, card: Card):
        super().__init__()
        self.card = card
        self.expand = True
        self.content = ft.Column(
            controls=[
                ft.Text(card.front, size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
                ft.Text(card.back, size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.update()