import flet as ft
from UI.theme import *
from data.repository import *
from UI.components.hoverButton import HoverButton
from UI.components.BaseDialog import BaseDialog
from UI.components.CustomField import CustomTextField

class DeckDetailsView(ft.Container):
    def __init__(self, navigate, * , deck_id):
        super().__init__()
        self._navigate = navigate
        self.deck_id = deck_id
        self.cards = get_cards(deck_id)
        self.cardState = None
        if self.cards == []:
            self.cardState = ft.Text("Pusta talia", size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT)
        else:
            self.cardState = ft.Container(
                
                content=ft.ListView(
                    controls=[
                        ft.Text(f"{card.front} - {card.back}", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT, text_align=ft.TextAlign.CENTER) for card in self.cards
                    ]
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
                padding=20,
                width=700,
            )
        self.expand = True
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
                            f"Szczegóły talii o ID: {deck_id}",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=PRIMARY_TEXT,
                            expand=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    # HoverButton(label="Add Card", on_click=self.show_add_deck_dialog),
                                    HoverButton(label="Delete Deck", on_click=self.show_delete_deck_dialog),
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
                self.cardState,
            ],
        )

    def _go_back(self, e):
        from UI.views.DeckView import DeckView
        self._navigate(DeckView)

    def _open_dialog(self, dialog: ft.AlertDialog):
        self.page.overlay.append(dialog)
        self.page.update()

    def _close_dialog(self, dialog: ft.AlertDialog):
        dialog.open = False
        self.page.update()
        print("Zamknięto dialog")
    def show_delete_deck_dialog(self, e):
        field = ft.Text("Are you sure you want to delete this deck?", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT, text_align=ft.TextAlign.CENTER)

        dialog = BaseDialog(
            title="Delete Deck",
            content=field,
            actions=[
                HoverButton("Delete", on_click=lambda e: self._delete_deck(dialog)),
                HoverButton("Cancel", on_click=lambda e: self._close_dialog(dialog)),
            ],
        )
        self._open_dialog(dialog)
        
    def _delete_deck(self, dialog: ft.AlertDialog):
        delete_deck(self.deck_id)
        self._close_dialog(dialog)
        self._go_back(None)