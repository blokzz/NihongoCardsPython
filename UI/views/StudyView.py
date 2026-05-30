import flet as ft
from UI.components.hoverButton import HoverButton
from core.study_session import StudySession
from UI.theme import *
from UI.views.BaseView import BaseView
from data.repository import save_stats , get_stats
from UI.views.StatsView import StatsView

class StudyView(BaseView):
    def __init__(self, navigate, *, deck_id: int):
        super().__init__(navigate)
        self.session = StudySession(deck_id)
        
        self.status_pill = ft.Text("QUESTION", size=10, weight=ft.FontWeight.BOLD, color=PRIMARY)
        self.status_badge = ft.Container(
            content=self.status_pill,
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, PRIMARY)),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=12, vertical=4),
        )
        
        self.front_text = ft.Text("", size=44, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT, text_align=ft.TextAlign.CENTER)
        self.reading_text = ft.Text("", size=18, color=PRIMARY, italic=True, visible=False, text_align=ft.TextAlign.CENTER)
        self.divider_line = ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, PRIMARY_TEXT), visible=False)
        self.back_text = ft.Text("", size=24, color=PRIMARY_TEXT, weight=ft.FontWeight.W_500, visible=False, text_align=ft.TextAlign.CENTER)
        self.example_text = ft.Text("", size=15, color=ft.Colors.GREY_400, italic=True, visible=False, text_align=ft.TextAlign.CENTER)
        self.onyomi_text = ft.Text("", size=15, color=ft.Colors.GREY_400, italic=True, visible=False, text_align=ft.TextAlign.CENTER)
        self.kunyomi_text = ft.Text("", size=15, color=ft.Colors.GREY_400, italic=True, visible=False, text_align=ft.TextAlign.CENTER)
        self.action_hint_text = ft.Text("Tap card to reveal answer", size=11, color=ft.Colors.GREY_500)
        self.progress_text = ft.Text("", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.GREY_400)
        self.progress_bar = ft.ProgressBar(value=0.0, color=PRIMARY, bgcolor=ft.Colors.GREY_800, height=4, border_radius=2)

        self.card_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self.status_badge,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(expand=True),
                    
                    ft.Column(
                        controls=[
                            self.front_text,
                            self.reading_text,
                            self.onyomi_text,
                            self.kunyomi_text,
                            self.divider_line,
                            self.back_text,
                            self.example_text,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    
                    ft.Container(expand=True),
                    self.action_hint_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.GREY_900,
            border_radius=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.15, PRIMARY_TEXT)),
            padding=30,
            width=480,
            height=320,  
            alignment=ft.Alignment.CENTER,
            on_click=self._reveal,
        )
        self.btn_again = self._create_rating_button("Again", 0, ft.Colors.RED_400)
        self.btn_hard = self._create_rating_button("Hard", 3, ft.Colors.ORANGE_400)
        self.btn_good = self._create_rating_button("Good", 2, PRIMARY)
        self.btn_easy = self._create_rating_button("Easy", 1, ft.Colors.GREEN_400)

        self.buttons_container = ft.Row(
            controls=[
                self.btn_again,
                self.btn_hard,
                self.btn_good,
                self.btn_easy,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
            opacity=0.0,
            animate_opacity=200,
            disabled=True,
        )

        self.expand = True
        self.content = ft.Column(
            expand=True,
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
                            padding=ft.padding.only(left=20, top=10),
                        ),
                        ft.Container(expand=True),
                    ],
                ),
                ft.Container(
                    content=self.progress_bar,
                    padding=ft.padding.symmetric(horizontal=40),
                    width=480,
                ),
                ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        self.progress_text,
                        self.card_container,
                        self.buttons_container,
                    ]
                )
            ],
        )
        self._load_next()

    def _create_rating_button(self, label: str, rating_val: int, active_color: str):
        btn_text = ft.Text(label, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300)
        
        def on_hover_btn(e):
            is_hovered = str(e.data).lower() == "true"
            container.bgcolor = active_color if is_hovered else ft.Colors.TRANSPARENT
            btn_text.color = ft.Colors.BLACK if is_hovered else ft.Colors.GREY_300
            container.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.4, active_color if is_hovered else ft.Colors.BLACK),
                offset=ft.Offset(0, 3)
            ) if is_hovered else None
            container.update()
            
        container = ft.Container(
            content=btn_text,
            width=100,
            height=42,
            border_radius=10,
            border=ft.border.all(1.5, ft.Colors.with_opacity(0.3, active_color)),
            alignment=ft.Alignment.CENTER,
            on_click=lambda e: self._answer(rating_val),
            on_hover=on_hover_btn,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        return container

    def _go_back(self, e):
        from UI.views.SelectDeckView import SelectDeckView
        self._navigation(SelectDeckView)

    def _load_next(self):
        card = self.session.next_card()
        if card:
            done, total, elapsed = self.session.progress
            self.progress_text.value = f"Progress: {done} / {total} cards"
            self.progress_bar.value = done / total if total > 0 else 0.0
            
            self.front_text.value = card.front
            
            if card.reading:
                self.reading_text.value = f"({card.reading})"
            else:
                self.reading_text.value = ""
            self.reading_text.visible = False
            
            if card.onyomi:
                self.onyomi_text.value = f"({card.onyomi})"
            else:
                self.onyomi_text.value = ""
            self.onyomi_text.visible = False

            if card.kunyomi:
                self.kunyomi_text.value = f"({card.kunyomi})"
            else:
                self.kunyomi_text.value = ""
            self.kunyomi_text.visible = False
                
            self.back_text.value = card.back
            self.back_text.visible = False
            
            self.divider_line.visible = False
            
            if card.example:
                example_val = card.example
                if example_val.lower().startswith("example:") or example_val.startswith("Example:"):
                    example_val = example_val.split(":", 1)[1].strip()
                self.example_text.value = example_val
            else:
                self.example_text.value = ""
            self.example_text.visible = False
            
            self.status_pill.value = "QUESTION"
            self.status_pill.color = PRIMARY
            self.status_badge.border = ft.border.all(1, ft.Colors.with_opacity(0.3, PRIMARY))
            self.action_hint_text.value = "Tap card to reveal answer"
            
            self.buttons_container.opacity = 0.0
            self.buttons_container.disabled = True
            self.card_container.shadow = None
            
            try:
                self.update()
            except RuntimeError:
                pass
        else:
            self._show_summary()

    def _reveal(self, e):
        if self.reading_text.value:
            self.reading_text.visible = True
        self.back_text.visible = True
        self.divider_line.visible = True
        if self.onyomi_text.value:
            self.onyomi_text.visible = True
        if self.kunyomi_text.value:
            self.kunyomi_text.visible = True
        if self.example_text.value:
            self.example_text.visible = True
            
        self.status_pill.value = "ANSWER"
        self.status_pill.color = ft.Colors.GREEN_400
        self.status_badge.border = ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.GREEN_400))
        self.action_hint_text.value = "Rate your recall difficulty below"
        
        self.buttons_container.opacity = 1.0
        self.buttons_container.disabled = False
        
        self.card_container.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.2, PRIMARY),
            offset=ft.Offset(0, 5),
        )
        self.update()

    def _answer(self, rating: int):
        self.session.answer(rating)
        self._load_next()

    def _show_summary(self):
        import time
        elapsed_seconds = time.time() - self.session.begin_session
        minutes = int(elapsed_seconds // 60)
        seconds = int(elapsed_seconds % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        self.progress_text.visible = False
        self.progress_bar.visible = False
        self.buttons_container.opacity = 0.0
        self.buttons_container.disabled = True
        
        xp_earned = self.session.correct * 10 + 20
        app = getattr(self._navigation, "__self__", None)
        if app and hasattr(app, "add_xp"):
            app.add_xp(xp_earned)
        cards_reviewed, cards_learned = get_stats()
        save_stats(cards_reviewed + self.session.correct + self.session.incorrect, cards_learned + self.session.correct)
        summary_column = ft.Column(
            controls=[
                ft.Text("Session Finished! 🎉", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY),
                ft.Container(height=10),
                ft.Row(
                    controls=[
                        ft.Text("Cards Reviewed:", size=16, color=PRIMARY_TEXT),
                        ft.Text(f"{self.session.correct + self.session.incorrect}", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY_TEXT),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    controls=[
                        ft.Text("Correct Answers:", size=16, color=ft.Colors.GREEN_400),
                        ft.Text(f"{self.session.correct}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    controls=[
                        ft.Text("XP Earned:", size=16, color=ft.Colors.AMBER_400),
                        ft.Text(f"+{xp_earned} XP", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    controls=[
                        ft.Text("Session Duration:", size=16, color=PRIMARY_TEXT),
                        ft.Text(time_str, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=15),
                ft.Row(
                    controls=[
                        HoverButton("Continue", on_click=self._on_continue_click),
                        HoverButton("Stats", on_click=self._on_stats_click),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        self.card_container.content = summary_column
        self.card_container.on_click = None
        self.card_container.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.3, PRIMARY),
            offset=ft.Offset(0, 5),
        )
        
        self.update()

    def _on_continue_click(self, e):
        from UI.views.SelectDeckView import SelectDeckView
        self._navigation(SelectDeckView)

    def _on_stats_click(self, e):
        from UI.views.StatsView import StatsView
        self._navigation(StatsView)