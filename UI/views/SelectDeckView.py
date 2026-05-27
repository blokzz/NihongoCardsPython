import flet as ft
from UI.views.BaseView import BaseView
from UI.theme import *
from data.repository import get_all_decks, get_card_count, get_due_card_count
from UI.views.StudyView import StudyView

class SelectDeckCard(ft.Container):
    def __init__(self, deck, navigate):
        super().__init__()
        self.deck = deck
        self.navigate = navigate
        
        # Premium layout styling
        self.bgcolor = ft.Colors.GREY_900
        self.border_radius = 14
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.1, PRIMARY_TEXT))
        self.padding = 16
        self.height = 135
        self.animate = ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        
        # Fetch counts
        total_cards = get_card_count(deck.id)
        due_cards = get_due_card_count(deck.id)
        self.total_cards = total_cards
        self.due_cards = due_cards
        
        # Due badge styling
        badge_color = PRIMARY if due_cards > 0 else ft.Colors.GREY_800
        badge_text_color = PRIMARY_TEXT if due_cards > 0 else ft.Colors.GREY_400
        due_badge = ft.Container(
            content=ft.Text(
                f"{due_cards} due",
                size=11,
                weight=ft.FontWeight.BOLD,
                color=badge_text_color,
            ),
            bgcolor=badge_color,
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
        )
        
        self.content = ft.Column(
            controls=[
                # Top row with folder icon and due cards badge
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.FOLDER_ROUNDED, color=PRIMARY, size=24),
                        due_badge,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                # Expand to center name vertically
                ft.Container(expand=True),
                # Deck name text in the middle
                ft.Text(
                    deck.name,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=PRIMARY_TEXT,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    max_lines=2,
                ),
                ft.Container(expand=True),
                # Bottom stats row
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.COPY_ROUNDED, color=ft.Colors.GREY_500, size=14),
                                ft.Text(f"{total_cards} cards", size=12, color=ft.Colors.GREY_400),
                            ],
                            spacing=4,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            spacing=0,
        )
        
        self.on_click = self._on_click
        self.on_hover = self._on_hover

    def _on_hover(self, e):
        is_hovered = str(e.data).lower() == "true"
        self.border = ft.border.all(1.5, PRIMARY if is_hovered else ft.Colors.with_opacity(0.1, PRIMARY_TEXT))
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=ft.Colors.with_opacity(0.2, PRIMARY if is_hovered else ft.Colors.BLACK),
            offset=ft.Offset(0, 4)
        )
        self.update()

    def _on_click(self, e):
        if self.total_cards == 0:
            snack = ft.SnackBar(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.WARNING_ROUNDED, color=ft.Colors.AMBER_300),
                        ft.Text(f"Deck '{self.deck.name}' is empty! Add cards first.", color=ft.Colors.WHITE),
                    ]
                ),
                bgcolor=ft.Colors.GREY_900,
                duration=3000,
                open=True,
            )
            self.page.overlay.append(snack)
            self.page.update()
            return

        print(f"Wybrano talię do powtórki: {self.deck.name}")
        self.navigate(StudyView, deck_id=self.deck.id)



class SelectDeckView(BaseView):
    def __init__(self, navigate):
        super().__init__(navigate)
        self.expand = True
        self.decks = get_all_decks()
        
        self.grid = ft.GridView(
            controls=[SelectDeckCard(deck, self._navigation) for deck in self.decks],
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
                            "Choose deck",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=PRIMARY_TEXT,
                            expand=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(width=200)
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(
                    content=self.grid if self.decks else ft.Text("No decks yet, add one first!", size=24, color=ft.Colors.GREY_500),
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
