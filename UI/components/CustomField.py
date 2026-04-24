import flet as ft
from UI.theme import *
class CustomTextField(ft.TextField):
    def __init__(self, label: str, **kwargs):
        super().__init__(
            label=label,
            color=PRIMARY_TEXT,
            bgcolor=BG_BUTTON,
            cursor_color=ft.Colors.RED_500,
            selection_color=ft.Colors.RED_200,
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
            focused_color=PRIMARY_TEXT,
            border=ft.InputBorder.OUTLINE,
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.RED_500,
            border_radius=10,
            border_width=1,
            focused_border_width=2,
            text_size=16,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
            **kwargs
        )