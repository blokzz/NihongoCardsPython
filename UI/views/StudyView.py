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
        self.back_text = ft.Text("", size=30, color=PRIMARY_TEXT, visible=False)
        self.progress_text = ft.Text("", size=16, color=ft.Colors.GREY_400)

        self.expand = True
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.progress_text,
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.front_text,
                            self.back_text,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=BG_BUTTON,
                    border_radius=15,
                    padding=40,
                    width=500,
                    alignment=ft.Alignment.CENTER,
                    on_click=self._reveal,
                ),
                ft.Row(
                    controls=[
                        HoverButton("✗ Źle", on_click=lambda e: self._answer(False)),
                        HoverButton("✓ Dobrze", on_click=lambda e: self._answer(True)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    opacity=0.0,
                    animate_opacity=200,
                    disabled=True,
                ),
            ],
        )
        self._load_next()

    def _load_next(self):
        card = self.session.next_card()
        if card:
            done, total = self.session.progress
            self.progress_text.value = f"{done}/{total}"
            self.front_text.value = card.front
            self.back_text.value = card.back
            self.back_text.visible = False
            self.content.controls[2].opacity = 0.0
            self.content.controls[2].disabled = True
            try:
                self.update()
            except RuntimeError:
                pass
        else:
            self._show_summary()

    def _reveal(self, e):
        self.back_text.visible = True
        self.content.controls[2].opacity = 1.0
        self.content.controls[2].disabled = False
        self.update()

    def _answer(self, correct: bool):
        self.session.answer(correct)
        self._load_next()

    def _show_summary(self):
        self.show_success(f"Koniec sesji! Wynik: {self.session.correct}/{self.session.total}")
        from UI.views.menu import MenuView
        self._navigation(MenuView)