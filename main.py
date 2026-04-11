import flet as ft

def check_level_up(func):
    def wrapper(self, *args, **kwargs):
        old_level = self.level
        result = func(self, *args, **kwargs)
        
        self.level = self.xp // 100
        if self.level > old_level:
            print(f"Awans! Poziom {self.level}")
            self.show_level_up_dialog()
        return result
    return wrapper

class JapaneseApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.xp = 0
        self.level = 0
        self.setup_ui()

    def setup_ui(self):
        self.page.title = "日本語暗記"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        self.stats_text = ft.Text(f"Poziom: {self.level} | XP: {self.xp}", size=20)
        self.btn = ft.ElevatedButton("Zaliczone słówko (+40 XP)", on_click=self.add_xp)
        
        self.page.add(
            ft.Text("こんにちは (Konnichiwa)", size=40, weight="bold"),
            self.stats_text,
            self.btn
        )

    @check_level_up
    def add_xp(self, e):
        self.xp += 40
        self.stats_text.value = f"Poziom: {self.level} | XP: {self.xp}"
        self.page.update()

    def show_level_up_dialog(self):
        self.page.snack_bar = ft.SnackBar(ft.Text("おめでとう!"))
        self.page.snack_bar.open = True
        self.page.update()

if __name__ == "__main__":
    ft.app(target=JapaneseApp)