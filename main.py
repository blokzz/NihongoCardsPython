import flet as ft
from UI.page import JapaneseApp
from data.database import init_db

if __name__ == "__main__":
    init_db()
    ft.run(JapaneseApp)