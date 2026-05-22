import flet as ft
from UI.components.hoverButton import HoverButton
from core.study_session import StudySession
from UI.theme import *
from UI.views.BaseView import BaseView
class StudyView(BaseView):
    def __init__(self, navigate, *, deck_id: int):
        super().__init__(navigate)
        self.session = StudySession(deck_id)
        
        self.front_text = ft.Text("", size=50, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT)
        self.reading_text = ft.Text("", size=22, color=ft.Colors.RED_300, italic=True, visible=False)
        self.back_text = ft.Text("", size=30, color=PRIMARY_TEXT, visible=False)
        self.example_text = ft.Text("", size=18, color=ft.Colors.GREY_300, italic=True, visible=False, text_align=ft.TextAlign.CENTER)
        self.progress_text = ft.Text("", size=16, color=ft.Colors.GREY_400)

        self.card_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.front_text,
                    self.reading_text,
                    ft.Container(height=10),
                    self.back_text,
                    ft.Container(height=10),
                    self.example_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=BG_BUTTON,
            border_radius=15,
            padding=40,
            width=500,
            alignment=ft.Alignment.CENTER,
            on_click=self._reveal,
        )

        self.buttons_container = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        HoverButton("Nothing", on_click=lambda e: self._answer(0)),
                        HoverButton("Easy", on_click=lambda e: self._answer(1)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Row(
                    controls=[
                        HoverButton("Good", on_click=lambda e: self._answer(2)),
                        HoverButton("Hard", on_click=lambda e: self._answer(3)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
            opacity=0.0,
            animate_opacity=200,
            disabled=True,
        )

        self.expand = True
        self.content = ft.Column(
            expand=True,
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
                            padding=ft.padding.only(left=20, top=10),
                        ),
                        ft.Container(expand=True),
                    ],
                ),
                ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        # self.progress_text,
                        self.card_container,
                        self.buttons_container,
                    ]
                )
            ],
        )
        self._load_next()

    def _go_back(self, e):
        from UI.views.SelectDeckView import SelectDeckView
        self._navigation(SelectDeckView)

    def _load_next(self):
        card = self.session.next_card()
        if card:
            done, total, elapsed = self.session.progress
            self.progress_text.value = f"{done}/{total}"
            self.front_text.value = card.front
            
            if card.reading:
                self.reading_text.value = f"({card.reading})"
            else:
                self.reading_text.value = ""
            self.reading_text.visible = False
            
            self.back_text.value = card.back
            self.back_text.visible = False
            
            if card.example:
                self.example_text.value = f"Przykład:\n{card.example}"
            else:
                self.example_text.value = ""
            self.example_text.visible = False
            
            self.buttons_container.opacity = 0.0
            self.buttons_container.disabled = True
            try:
                self.update()
            except RuntimeError:
                pass
        else:
            self._show_summary()

    def _reveal(self, e):
        if self.reading_text.value:
            self.reading_text.visible = True
        self.back_text.visible = True
        if self.example_text.value:
            self.example_text.visible = True
            
        self.buttons_container.opacity = 1.0
        self.buttons_container.disabled = False
        self.update()

    def _answer(self, rating: int):
        self.session.answer(rating)
        self._load_next()

    def _show_summary(self):
        import time
        elapsed_seconds = time.time() - self.session.begin_session
        minutes = int(elapsed_seconds // 60)
        seconds = int(elapsed_seconds % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.progress_text.visible = False
        self.buttons_container.opacity = 0.0
        self.buttons_container.disabled = True
        summary_column = ft.Column(
            controls=[
                ft.Text("Sesja Zakończona! 🎉", size=28, weight=ft.FontWeight.BOLD, color=PRIMARY),
                ft.Container(height=10),
                ft.Row(
                    controls=[
                        ft.Text("Przejrzane karty:", size=18, color=PRIMARY_TEXT),
                        ft.Text(f"{self.session.correct + self.session.incorrect}", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    controls=[
                        ft.Text("Czas trwania:", size=18, color=PRIMARY_TEXT),
                        ft.Text(time_str, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=20),
                HoverButton(
                    "Kontynuuj", 
                    on_click=self._on_continue_click
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        self.card_container.content = summary_column
        self.card_container.on_click = None
        
        self.update()

    def _on_continue_click(self, e):
        from UI.views.SelectDeckView import SelectDeckView
        self._navigation(SelectDeckView)