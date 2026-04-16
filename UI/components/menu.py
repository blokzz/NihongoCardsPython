import flet as ft

def menu(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def make_btn(label: str):
        btn = ft.Container(
            content=ft.Text(label, color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.W_500),
            width=250,
            height=55,
            bgcolor=ft.Colors.GREY_800,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
            animate=ft.Animation(duration=200, curve=ft.AnimationCurve.EASE_IN_OUT),
        )

        def on_hover(e):
            btn.bgcolor = ft.Colors.RED_500 if e.data else ft.Colors.GREY_800
            btn.update()

        btn.on_hover = on_hover
        return btn

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
                    make_btn("Fiszki"),
                    make_btn("Ustawienia"),
                    make_btn("Wyjście"),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(expand=True),
            ft.Text("v1.0", size=12, color=ft.Colors.GREY_500),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(layout)