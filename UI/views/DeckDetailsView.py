from utils import handle_errors
import flet as ft
from UI.theme import *
from data.repository import *
from UI.components.hoverButton import HoverButton
from UI.components.BaseDialog import BaseDialog
from UI.components.CardDetails import CardDetails
from UI.components.CustomField import CustomTextField
from UI.views.BaseView import BaseView
class DeckDetailsView(BaseView):
    def __init__(self, navigate, * , deck_id):
        super().__init__(navigate)
        self.deck_id = deck_id
        self.cards = get_cards(deck_id)
        self.cardState = None
        if self.cards == []:
            self.cardState = ft.Container(
                content=ft.Text("Pusta talia", size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
                alignment=ft.Alignment.CENTER,
                expand=True,
                padding=20,
                width=700,
            )
        else:
            self.cardState = ft.Container(
                
                content=ft.ListView(
                    controls=[
                        CardDetails(
                            card,
                            on_edit=lambda e, c=card: self.show_edit_card_dialog(c),
                            on_delete=lambda e, c=card: self.show_delete_card_dialog(c)
                        ) for card in self.cards
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
                            f"Deck: {get_deck(self.deck_id).name} Details",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=PRIMARY_TEXT,
                            expand=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    HoverButton(label="Add Card", on_click=self.show_add_card_dialog),
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
        self._navigation(DeckView)

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
    @handle_errors("Deck deleted successfully")
    def _delete_deck(self, dialog: ft.AlertDialog):
        delete_deck(self.deck_id)
        self._close_dialog(dialog)
        self._go_back(None)


    def show_add_card_dialog(self, e):
        front = CustomTextField(label="Front", autofocus=True)
        back = CustomTextField(label="Back")
        card_type = ft.Dropdown(
            options=[
                ft.dropdown.Option("Kanji"),
                ft.dropdown.Option("Kana"),
                ft.dropdown.Option("Word"),
                ft.dropdown.Option("Sentence"),
            ],
            label="Card Type"
        )
        example = CustomTextField(label="Example")
        reading = CustomTextField(label="Reading")
        dialog = BaseDialog(
            title="Add Card",
            content=ft.Column([
                front,
                back,
                example,
                reading,
                card_type,
            ], tight=True),
            actions=[
                HoverButton("Add", on_click=lambda e: self._add_card(front.value, back.value, example.value, reading.value, card_type.value, dialog)),
                HoverButton("Cancel", on_click=lambda e: self._close_dialog(dialog)),
            ],
            
        )
        self._open_dialog(dialog)

    @handle_errors("Card added successfully")
    def _add_card(self, front: str, back: str, example: str, reading: str, card_type: str, dialog: ft.AlertDialog):
        save_card(Card(id=get_next_card_id(), deck_id=self.deck_id, front=front, back=back, example=example, reading=reading, card_type=card_type))
        self._refresh()
        self._close_dialog(dialog)

    def show_edit_card_dialog(self, card: Card):
        front = CustomTextField(label="Front", value=card.front, autofocus=True)
        back = CustomTextField(label="Back", value=card.back)
        card_type = ft.Dropdown(
            options=[
                ft.dropdown.Option("Kanji"),
                ft.dropdown.Option("Kana"),
                ft.dropdown.Option("Word"),
                ft.dropdown.Option("Sentence"),
            ],
            label="Card Type",
            value=card.card_type
        )
        example = CustomTextField(label="Example", value=card.example)
        reading = CustomTextField(label="Reading", value=card.reading)
        dialog = BaseDialog(
            title="Edit Card",
            content=ft.Column([
                front,
                back,
                example,
                reading,
                card_type,
            ], tight=True),
            actions=[
                HoverButton("Save", on_click=lambda e: self._edit_card(card.id, front.value, back.value, example.value, reading.value, card_type.value, dialog)),
                HoverButton("Cancel", on_click=lambda e: self._close_dialog(dialog)),
            ],
        )
        self._open_dialog(dialog)

    def _edit_card(self, card_id: int, front: str, back: str, example: str, reading: str, card_type: str, dialog: ft.AlertDialog):
        update_card_details(card_id, front, back, card_type, example, reading)
        self._refresh()
        self._close_dialog(dialog)

    def show_delete_card_dialog(self, card: Card):
        field = ft.Text("Are you sure you want to delete this card?", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT, text_align=ft.TextAlign.CENTER)
        dialog = BaseDialog(
            title="Delete Card",
            content=field,
            actions=[
                HoverButton("Delete", on_click=lambda e: self._delete_card(card.id, dialog)),
                HoverButton("Cancel", on_click=lambda e: self._close_dialog(dialog)),
            ],
        )
        self._open_dialog(dialog)
    
    @handle_errors("Card deleted successfully")
    def _delete_card(self, card_id: int, dialog: ft.AlertDialog):
        delete_card(card_id)
        self._refresh()
        self._close_dialog(dialog)

    def _refresh(self):
        self.cards = get_cards(self.deck_id)
        if self.cards:
            self.cardState.content = ft.ListView(
                controls=[
                    CardDetails(
                        card, 
                        on_edit=lambda e, c=card: self.show_edit_card_dialog(c),
                        on_delete=lambda e, c=card: self.show_delete_card_dialog(c)
                    ) for card in self.cards
                ]
            )
            self.cardState.update()
        else:
            self.cardState.content = ft.Text("Pusta talia", size=40, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT)
            self.cardState.update()
    