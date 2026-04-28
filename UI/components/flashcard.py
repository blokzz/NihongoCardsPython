import flet as ft

class Flashcard:
    def __init__(self, page: ft.Page, kanji: str, reading: str):
        self.page = page
        self.kanji = kanji
        self.reading = reading
        self.is_flipped = False

        self.display_text = ft.Text(self.kanji, size=50, weight=ft.FontWeight.BOLD)
        self.flip_button = ft.ElevatedButton(content=ft.Text("Obróć fiszkę"), on_click=self.flip)

        self.view = ft.Container(
            content=ft.Column(
                controls=[self.display_text, self.flip_button],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=30,
            border_radius=15
        )

    def flip(self, e):
        self.is_flipped = not self.is_flipped
        self.display_text.value = self.reading if self.is_flipped else self.kanji
        self.page.update()