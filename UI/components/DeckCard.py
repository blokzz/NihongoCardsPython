import flet as ft
from UI.theme import *
from data.models import Deck
from UI.views.DeckDetailsView import DeckDetailsView
from data.repository import get_card_count, get_due_card_count

class DeckCard(ft.Container):
    def __init__(self, deck: Deck, navigate):
        super().__init__()
        self.deck = deck
        self.navigate = navigate
        
        self.bgcolor = ft.Colors.GREY_900
        self.border_radius = 14
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.1, PRIMARY_TEXT))
        self.padding = 16
        self.height = 135
        self.animate = ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        
        total_cards = get_card_count(deck.id)
        due_cards = get_due_card_count(deck.id)
        
        badge_color = PRIMARY if due_cards > 0 else ft.Colors.GREY_800
        badge_text_color = PRIMARY_TEXT if due_cards > 0 else ft.Colors.GREY_400
        due_badge = ft.Container(
            content=ft.Text(
                f"{due_cards} due",
                size=11,
                weight=ft.FontWeight.BOLD,
                color=badge_text_color,
            ),
            bgcolor=badge_color,
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
        )
        
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.FOLDER_ROUNDED, color=PRIMARY, size=24),
                        due_badge,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(expand=True),
                ft.Text(
                    deck.name,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=PRIMARY_TEXT,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    max_lines=2,
                ),
                ft.Container(expand=True),
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.COPY_ROUNDED, color=ft.Colors.GREY_500, size=14),
                                ft.Text(f"{total_cards} cards", size=12, color=ft.Colors.GREY_400),
                            ],
                            spacing=4,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            spacing=0,
        )
        
        self.on_click = self._on_click
        self.on_hover = self._on_hover

    def _on_hover(self, e):
        is_hovered = str(e.data).lower() == "true"
        self.border = ft.border.all(1.5, PRIMARY if is_hovered else ft.Colors.with_opacity(0.1, PRIMARY_TEXT))
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=ft.Colors.with_opacity(0.2, PRIMARY if is_hovered else ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
        self.update()

    def _on_click(self, e):
        print(f"Wybrano talię: {self.deck.name}")
        self.navigate(DeckDetailsView, deck_id=self.deck.id)