from datetime import datetime
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


def log_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            with open("errors.log", "a") as f:
                f.write(f"{datetime.now()} | {func.__name__} | {e}\n")
            raise
    return wrapper