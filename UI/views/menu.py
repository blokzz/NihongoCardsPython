from UI.views.BaseView import BaseView
from UI.views.FlashCardView import FlashcardView
from UI.views.DeckView import DeckView
import flet as ft
from UI.components.hoverButton import HoverButton
from UI.theme import *

class MenuView(BaseView):
    def __init__(self, navigate):
        super().__init__(navigate)
        self.expand = True
        self.views_map = { 
            "Start": FlashcardView,
            "Decks": DeckView,
            "Settings": FlashcardView,
            "Exit": None
        }
        self.info_text = ft.Text("", size=16, color=PRIMARY_TEXT)
        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Text(
                        "日本語暗記", 
                        size=80, 
                        weight=ft.FontWeight.W_900, 
                        color=PRIMARY_TEXT
                    ),
                    padding=ft.padding.only(top=100, bottom=10),
                    alignment=ft.Alignment.CENTER
                ),
                ft.Container(
                    content=ft.Text(
                        "Japanese Flashcards", 
                        size=20, 
                        weight=ft.FontWeight.W_400, 
                        color=PRIMARY,
                        italic=True
                    ),
                    padding=ft.padding.only(bottom=50),
                    alignment=ft.Alignment.CENTER
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            HoverButton("Start", on_click=self._on_fiszki_click, data="Start"),
                            HoverButton("Decks", on_click=self._on_fiszki_click, data="Decks"),
                            HoverButton("Settings", on_click=self._on_fiszki_click, data="Settings"),
                            HoverButton("Exit", on_click=self._on_fiszki_click, data="Exit"),
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.Alignment.CENTER
                ),
                ft.Container(expand=True),
                self.info_text,
                ft.Container(
                    content=ft.Text("v0.1", size=14, color=ft.Colors.GREY_600),
                    padding=ft.padding.only(bottom=20),
                    alignment=ft.Alignment.CENTER
                ),
            ]
        )

    async def _on_fiszki_click(self, e):
        if e.control.data == "Exit":
            await self.page.window.close()
        else:
            self._navigation(self.views_map[e.control.data])