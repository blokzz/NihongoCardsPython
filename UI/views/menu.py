from UI.views.FlashCardView import FlashcardView
from UI.views.DeckView import DeckView
import flet as ft
from UI.components.hoverButton import HoverButton
from UI.theme import *
class MenuView(ft.Column):
    def __init__(self, navigate):
        super().__init__()
        self._navigation = navigate
        self.content = { "Start" : FlashcardView,
                            "Decks" : DeckView,
                            "Settings" : FlashcardView,
                            "Exit" : lambda e: self.page.window.close()
        }
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
                    HoverButton("Start", on_click=self._on_fiszki_click, data="Start"),
                    HoverButton("Decks", on_click=self._on_fiszki_click, data="Decks"),
                    HoverButton("Settings", on_click=self._on_fiszki_click, data="Settings"),
                    HoverButton("Exit", on_click=self._on_fiszki_click, data="Exit"),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            self.info_text,
            ft.Container(expand=True),
            ft.Text("v0.1", size=12, color=SURFACE),
        ]

    def _on_fiszki_click(self, e):
        if e.control.data == "Exit":
            self.page.window.close()
        else:
            self._navigation(self.content[e.control.data])