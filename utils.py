import asyncio
from datetime import datetime
from core.exceptions import * 

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

def handle_errors(success_msg: str = None):
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            async def wrapper(self, *args, **kwargs):
                try:
                    result = await func(self, *args, **kwargs)
                    if success_msg:
                        self.show_success(success_msg)
                    return result
                except InvalidCardError as ex:
                    self.show_error(str(ex))
                except EmptyDeckError as ex:
                    self.show_error(str(ex))
                except Exception as ex:
                    self.show_error(str(ex))
            return wrapper
        else:
            def wrapper(self, *args, **kwargs):
                try:
                    result = func(self, *args, **kwargs)
                    if success_msg:
                        self.show_success(success_msg)
                    return result
                except InvalidCardError as ex:
                    self.show_error(str(ex))
                except EmptyDeckError as ex:
                    self.show_error(str(ex))
                except Exception as ex:
                    self.show_error(str(ex))
            return wrapper
    return decorator