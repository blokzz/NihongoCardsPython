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

