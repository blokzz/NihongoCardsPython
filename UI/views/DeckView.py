from utils import handle_errors
import flet as ft
from UI.components.DeckCard import DeckCard
from UI.theme import *
from data.models import Deck
from UI.components.hoverButton import HoverButton
from UI.components.CustomField import CustomTextField
from UI.components.BaseDialog import BaseDialog
from data.repository import *
from data.io.importer import *
from core.exceptions import *
from UI.views.BaseView import BaseView
class DeckView(BaseView):
    def __init__(self, navigate):
        super().__init__(navigate)
        self.expand = True
        self.file_picker = ft.FilePicker()
        self.decks = get_all_decks()
        self.grid = ft.GridView(
            controls=[DeckCard(deck, self._navigation) for deck in self.decks],
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
                            "Decks",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=PRIMARY_TEXT,
                            expand=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    HoverButton(label="Add Deck", on_click=self.show_add_deck_dialog),
                                    HoverButton(label="Import Deck", on_click=self.import_deck),
                                ],
                                spacing=10,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),
                            width=200,
                            padding=ft.padding.only(right=40 , top=20),
                            
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
              ft.Container(
                    content=self.grid,
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
    
    def _open_dialog(self, dialog: ft.AlertDialog):
        self.page.overlay.append(dialog)
        self.page.update()

    def _close_dialog(self, dialog: ft.AlertDialog):
        dialog.open = False
        self.page.update()
    def show_add_deck_dialog(self, e):
        field = CustomTextField(label="Nazwa talii", autofocus=True)
        dialog = BaseDialog(
            title="Nowa talia",
            content=field,
            actions=[
                HoverButton("Anuluj", on_click=lambda e: self._close_dialog(dialog)),
                HoverButton("Dodaj", on_click=lambda e: self._save_deck(field.value, dialog)),
            ],
        )
        self._open_dialog(dialog)

    @handle_errors("Deck added successfully")
    def _save_deck(self, name: str, dialog: ft.AlertDialog):
        if not name:
            raise InvalidFormatError("Name cannot be empty")
        save_deck(Deck(id=len(self.decks)+1, name=name))
        self._close_dialog(dialog)
        self._refresh()

    def _refresh(self):
        self.grid.controls = [DeckCard(deck, navigate=self._navigation) for deck in self._load_decks()]
        self.grid.update()

    def _load_decks(self) -> list[Deck]:
        return get_all_decks()

    @handle_errors("Deck imported successfully")
    async def import_deck(self, e):
        files = await self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["json"],
            file_type=ft.FilePickerFileType.CUSTOM,
        )
        if not files:
            raise InvalidJsonError("No file selected")
        else:
            path = files[0].path
            from data.io.importer import import_from_json
            import_from_json(path)
            self._refresh()
