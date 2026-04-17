import flet as ft
from UI.components.hoverButton import HoverButton
from UI.theme import *

def menu(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    layout = ft.Column(
        expand=True,
        controls=[
            ft.Container(
                content=ft.Text("日本語暗記", size=70, weight=ft.FontWeight.BOLD),
                padding=ft.padding.only(top=70),
            ),
            ft.Container(expand=True),
            ft.Column(
                controls=[
                    HoverButton("Fiszki"),
                    HoverButton("Ustawienia"),
                    HoverButton("Wyjście"),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(expand=True),
            ft.Text("v1.0", size=12, color=SURFACE),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(layout)