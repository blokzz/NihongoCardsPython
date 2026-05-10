import flet as ft
class BaseView(ft.Container):
    def __init__(self, navigate):
        super().__init__()
        self._navigation = navigate

    def go_back(self, e):
        pass
    def show_error(self, message: str):
        print("Error")
        snack = ft.SnackBar(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.WHITE),
                    ft.Text(message, color=ft.Colors.WHITE),
                ]
            ),
            bgcolor=ft.Colors.RED_700,
            duration=3000,
            open=True,
        )
        self.page.overlay.append(snack)
        self.page.update()

    def show_success(self, message: str):
        snack = ft.SnackBar(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE),
                    ft.Text(message, color=ft.Colors.WHITE),
                ]
            ),
            bgcolor=ft.Colors.GREEN_700,
            duration=2000,
            open=True,
        )
        self.page.overlay.append(snack)
        self.page.update()