import flet as ft
from UI.views.BaseView import BaseView
import matplotlib.pyplot as plt
from UI.theme import *   
from data.repository import get_stats, save_stats , get_stats_all_time
import july
import pandas as pd
from datetime import datetime
import io
import base64

class StatsView(BaseView):
    def __init__(self, navigate=None):
        super().__init__(navigate)
        self.expand = True
        
        img_base64 = self.generate_stats_base64()
        
        self.content = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=ft.padding.only(top=10, bottom=20, left=20, right=20),
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                                    on_click=self._go_back,
                                    icon_color=PRIMARY_TEXT,
                                    icon_size=20,
                                ),
                                width=100,
                                alignment=ft.Alignment(-1, 0),
                            ),
                            ft.Text(
                                "Statistics",
                                size=32,
                                weight=ft.FontWeight.W_900,
                                color=PRIMARY_TEXT,
                                expand=True,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(width=100)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
                
                ft.Container(
                    bgcolor=BG_BUTTON,
                    padding=25,
                    border_radius=15,
                    width=650,
                    border=ft.border.only(left=ft.BorderSide(4, PRIMARY)),
                    shadow=ft.BoxShadow(
                        blur_radius=10,
                        color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4)
                    ),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                        controls=[
                            ft.Text(
                                "Activity Heatmap (Cards Reviewed)", 
                                size=18, 
                                weight=ft.FontWeight.BOLD, 
                                color=PRIMARY
                            ),
                            ft.Divider(color=ft.Colors.with_opacity(0.1, PRIMARY_TEXT), height=1),
                            
                            ft.Container(
                                content=ft.Image(
                                    src=f"data:image/png;base64,{img_base64}", 
                                    width=600, 
                                    height=240, 
                                    fit="contain"
                                ) if img_base64 else ft.Text("No review history recorded yet.", color=PRIMARY_TEXT),
                                alignment=ft.Alignment.CENTER,
                                padding=ft.padding.symmetric(vertical=10),
                            ),
                        ]
                    )
                )
            ]
        )
        
    def _go_back(self, e):
        from UI.views.menu import MenuView
        self._navigation(MenuView)

    def generate_stats_base64(self) -> str:
        try:
            current_year = datetime.now().year
            dates = pd.date_range(f"{current_year}-01-01", f"{current_year}-12-31")
            
            stats = get_stats_all_time()
            
            df_data = pd.Series(0, index=dates)
            for stat_date, cards_learned, cards_reviewed in stats:
                ts = pd.Timestamp(stat_date)
                if ts in df_data.index:
                    df_data[ts] = cards_reviewed

            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(10, 3.5), facecolor='#1e1e24')
            ax.set_facecolor('#1e1e24')
            
            july.heatmap(
                dates, 
                df_data.values, 
                cmap="github", 
                ax=ax, 
                cmin=1, 
                colorbar=True, 
                value_label=False
            )
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, facecolor='#1e1e24')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)
            return img_base64
        except Exception as e:
            pass
            return None
