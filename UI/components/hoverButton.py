import flet as ft
from UI.theme import *
class HoverButton(ft.Container):
    def __init__(self, label: str, on_click=None):
        super().__init__(
            content=ft.Text(label, color=PRIMARY_TEXT, size=16, weight=ft.FontWeight.W_500),
            width=BTN_WIDTH,
            height=55,
            bgcolor=BG_BUTTON,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
            animate=ft.Animation(duration=200, curve=ft.AnimationCurve.EASE_IN_OUT),
            on_hover=self._on_hover,
            on_click=on_click,
        )

    def _on_hover(self, e):
        self.bgcolor = PRIMARY if e.data else SURFACE
        self.update()