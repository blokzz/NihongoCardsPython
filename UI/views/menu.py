import flet as ft
from UI.components.hoverButton import HoverButton
from UI.theme import *
class MenuView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.info_text = ft.Text("", size=16, color=PRIMARY_TEXT)
        self.controls = [
            ft.Container(
                content=ft.Text("日本語暗記", size=70, weight=ft.FontWeight.BOLD),
                padding=ft.padding.only(top=70),
            ),
            ft.Container(expand=True),
            ft.Column(
                controls=[
                    HoverButton("Start", on_click=self._on_fiszki_click),
                    HoverButton("Decks"),
                    HoverButton("Settings"),
                    HoverButton("Exit", on_click=lambda e: page.window.close()),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            self.info_text,
            ft.Container(expand=True),
            ft.Text("v0.1", size=12, color=SURFACE),
        ]

    def _on_fiszki_click(self, e):
        deck_count = 5
        self.info_text.value = f"Masz {deck_count} decków"
        self.info_text.update()