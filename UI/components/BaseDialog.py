import flet as ft
from UI.theme import *
class BaseDialog(ft.AlertDialog):
    def __init__(
        self,
        title: str,
        content: ft.Control,
        actions: list[ft.Control],
        width: int = 400,
    ):
        super().__init__(
            modal=True,
            bgcolor=BG_BUTTON,
            shape=ft.RoundedRectangleBorder(radius=15),
            title=ft.Text(title, size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
            title_padding=ft.padding.all(24),
            content=ft.Container(
                content=content,
                width=width,
            ),
            content_padding=ft.padding.symmetric(horizontal=24, vertical=10),
            actions=actions,
            actions_padding=ft.padding.all(16),
            actions_alignment=ft.MainAxisAlignment.END,
            open=True,
        )