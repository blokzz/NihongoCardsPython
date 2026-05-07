import flet as ft
from UI.theme import *
from data.models import Card

class CardDetails(ft.Container):
    def __init__(self, card: Card, on_edit=None, on_delete=None):
        super().__init__()
        self.card = card
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self.bgcolor = BG_BUTTON
        self.border_radius = 10
        self.padding = ft.padding.all(20)
        self.margin = ft.margin.only(bottom=15)
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.1, PRIMARY_TEXT))
        
        details_column = []
        if card.reading:
            details_column.append(ft.Text(f"Reading: {card.reading}", size=16, color=PRIMARY_TEXT, italic=True))
        if card.example:
            details_column.append(ft.Text(f"Example: {card.example}", size=16, color=PRIMARY_TEXT))
            
        details_container = ft.Column(
            controls=details_column,
            spacing=5,
        ) if details_column else ft.Container()

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Row([
                                    ft.Text(card.front, size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
                                    ft.Icon(ft.Icons.ARROW_FORWARD, size=20, color=PRIMARY_TEXT),
                                    ft.Text(card.back, size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
                                ], spacing=15, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                                ft.Container(
                                    content=ft.Text(card.card_type, size=12, color=SECONDARY_TEXT),
                                    bgcolor=PRIMARY,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                    border_radius=10,
                                ),
                            ],
                            spacing=5,
                            expand=True,
                        ),
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_ROUNDED,
                                    icon_color=PRIMARY_TEXT,
                                    tooltip="Edit Card",
                                    on_click=self.on_edit
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_ROUNDED,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip="Delete Card",
                                    on_click=self.on_delete
                                ),
                            ],
                            spacing=0,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                details_container,
            ],
            spacing=15,
        )