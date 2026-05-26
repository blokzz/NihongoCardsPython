from utils import handle_errors
import flet as ft
from UI.theme import *
from data.repository import *
from UI.components.hoverButton import HoverButton
from data.io.exporter import export_to_json
from UI.components.BaseDialog import BaseDialog
from UI.components.CardDetails import CardDetails
from UI.components.CustomField import CustomTextField
from UI.views.BaseView import BaseView
class DeckDetailsView(BaseView):
    def __init__(self, navigate, * , deck_id):
        super().__init__(navigate)
        self.deck_id = deck_id
        self.card_type = None
        self.cards = get_cards(deck_id)
        self.deck = get_deck(deck_id)
        self.deck.cards = self.cards
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
                                    HoverButton(label="Export", on_click=self.show_export_dialog),
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

    def show_export_dialog(self, e):
        dialog = BaseDialog(
            title="Export Deck",
            content=ft.Text("Are you sure you want to export this deck?", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT, text_align=ft.TextAlign.CENTER),
            actions=[
                HoverButton("Export", on_click=lambda e: self._export_deck(dialog)),
                HoverButton("Cancel", on_click=lambda e: self._close_dialog(dialog)),
            ],
        )
        self._open_dialog(dialog)
    
    @handle_errors("Deck exported successfully")
    def _export_deck(self, dialog: ft.AlertDialog):
        export_to_json("decks/" + self.deck.name + ".json", self.deck.id)
        self._close_dialog(dialog)

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


    def handle_dropdown_select(self, e):
        self.card_type = e.control.value
        is_kanji = self.card_type == "Kanji"
        if is_kanji:
            if self.reading in self.dialog_content.controls:
                self.dialog_content.controls.remove(self.reading)
            if self.onyomi not in self.dialog_content.controls:
                self.dialog_content.controls.insert(3, self.onyomi)
                self.dialog_content.controls.insert(4, self.kunyomi)
        else:
            if self.reading not in self.dialog_content.controls:
                self.dialog_content.controls.insert(3, self.reading)
            if self.onyomi in self.dialog_content.controls:
                self.dialog_content.controls.remove(self.onyomi)
            if self.kunyomi in self.dialog_content.controls:
                self.dialog_content.controls.remove(self.kunyomi)
        self.dialog_content.update()
        e.control.update()

    def show_add_card_dialog(self, e):
        front = CustomTextField(label="Front", autofocus=True)
        back = CustomTextField(label="Back")
        self.onyomi = CustomTextField(label="Onyomi")
        self.kunyomi = CustomTextField(label="Kunyomi")
        example = CustomTextField(label="Example")
        self.reading = CustomTextField(label="Reading")
        
        card_type = ft.Dropdown(
            options=[
                ft.dropdown.Option("Kanji"),
                ft.dropdown.Option("Kana"),
                ft.dropdown.Option("Word"),
                ft.dropdown.Option("Sentence"),
            ],
            label="Card Type",
            on_select=self.handle_dropdown_select,
        )
        
        self.dialog_content = ft.Column([
            front,
            back,
            example,
            self.reading,
            card_type,
        ], tight=True, height=500)
        
        dialog = BaseDialog(
            title="Add Card",
            content=self.dialog_content,
            actions=[
                HoverButton("Add", on_click=lambda e: self._add_card(front.value, back.value, example.value, self.reading.value, card_type.value, self.onyomi.value if self.onyomi in self.dialog_content.controls else None, self.kunyomi.value if self.kunyomi in self.dialog_content.controls else None, dialog)),
                HoverButton("Cancel", on_click=lambda e: self._close_dialog(dialog)),
            ],
        )
        self._open_dialog(dialog)

    @handle_errors("Card added successfully")
    def _add_card(self, front: str, back: str, example: str, reading: str, card_type: str, onyomi: str, kunyomi: str, dialog: ft.AlertDialog):
        if card_type != "Kanji":
            onyomi = None
            kunyomi = None
        save_card(Card(id=get_next_card_id(), deck_id=self.deck_id, front=front, back=back, example=example, reading=reading, card_type=card_type, onyomi=onyomi, kunyomi=kunyomi))
        self._refresh()
        self._close_dialog(dialog)

    def show_edit_card_dialog(self, card: Card):
        front = CustomTextField(label="Front", value=card.front, autofocus=True)
        back = CustomTextField(label="Back", value=card.back)
        self.onyomi = CustomTextField(label="Onyomi", value=getattr(card, "onyomi", "") or "")
        self.kunyomi = CustomTextField(label="Kunyomi", value=getattr(card, "kunyomi", "") or "")
        example = CustomTextField(label="Example", value=card.example)
        self.reading = CustomTextField(label="Reading", value=card.reading)
        
        card_type = ft.Dropdown(
            options=[
                ft.dropdown.Option("Kanji"),
                ft.dropdown.Option("Kana"),
                ft.dropdown.Option("Word"),
                ft.dropdown.Option("Sentence"),
            ],
            label="Card Type",
            value=card.card_type,
            on_select=self.handle_dropdown_select,
        )
        
        is_kanji_initially = card.card_type == "Kanji"
        if is_kanji_initially:
            self.dialog_content = ft.Column([
                front,
                back,
                example,
                self.onyomi,
                self.kunyomi,
                card_type,
            ], tight=True, height=500)
        else:
            self.dialog_content = ft.Column([
                front,
                back,
                example,
                self.reading,
                card_type,
            ], tight=True, height=500)
            
        dialog = BaseDialog(
            title="Edit Card",
            content=self.dialog_content,
            actions=[
                HoverButton("Save", on_click=lambda e: self._edit_card(card.id, front.value, back.value, example.value, self.reading.value, card_type.value, self.onyomi.value if self.onyomi in self.dialog_content.controls else None, self.kunyomi.value if self.kunyomi in self.dialog_content.controls else None, dialog)),
                HoverButton("Cancel", on_click=lambda e: self._close_dialog(dialog)),
            ],
        )
        self._open_dialog(dialog)

    def _edit_card(self, card_id: int, front: str, back: str, example: str, reading: str, card_type: str, onyomi: str, kunyomi: str, dialog: ft.AlertDialog):
        if card_type != "Kanji":
            onyomi = None
            kunyomi = None
        update_card_details(card_id, front, back, card_type, example, reading, onyomi, kunyomi)
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
    