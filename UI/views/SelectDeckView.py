import flet as ft
from UI.views.BaseView import BaseView
from UI.theme import *
from data.repository import get_all_decks
from UI.views.StudyView import StudyView

class SelectDeckCard(ft.Container):
    def __init__(self, deck, navigate):
        super().__init__()
        self.deck = deck
        self.navigate = navigate
        self.bgcolor = BG_BUTTON
        self.border_radius = 10
        self.padding = 30
        self.width = BTN_WIDTH
        self.height = 100
        self.animate = ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_OUT)
        
        self.content = ft.Column(
            controls=[
                ft.Text(deck.name, size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.on_click = self._on_click
        self.on_hover = self._on_hover

    def _on_hover(self, e):
        self.bgcolor = PRIMARY if str(e.data).lower() == "true" else BG_BUTTON
        self.update()

    def _on_click(self, e):
        print(f"Wybrano talię do powtórki: {self.deck.name}")
        self.navigate(StudyView, deck_id=self.deck.id)
        e.control.update()


class SelectDeckView(BaseView):
    def __init__(self, navigate):
        super().__init__(navigate)
        self.expand = True
        self.decks = get_all_decks()
        
        self.grid = ft.GridView(
            controls=[SelectDeckCard(deck, self._navigation) for deck in self.decks],
            spacing=20,
            max_extent=200,
            run_spacing=20,
            runs_count=3,
        )
        
        self.content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                on_click=self._go_back,
                                icon_color=PRIMARY_TEXT,
                            ),
                            width=200,
                        ),
                        ft.Text(
                            "Wybierz talię",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=PRIMARY_TEXT,
                            expand=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(width=200)
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(
                    content=self.grid if self.decks else ft.Text("Brak talii, dodaj jakąś najpierw!", size=24, color=ft.Colors.GREY_500),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                    padding=20,
                    width=700,
                )
            ],
        )

    def _go_back(self, e):
        from UI.views.menu import MenuView
        self._navigation(MenuView)
