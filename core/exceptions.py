class EmptyDeckError(Exception):
    """Rzucany gdy próbujemy rozpocząć sesję z pustą talią"""
    def __init__(self, deck_name: str):
        self.deck_name = deck_name
        super().__init__(f"Deck '{deck_name}' is empty")

class InvalidCardError(Exception):
    """Rzucany gdy karta nie zawiera japońskich znaków"""
    def __init__(self, field: str):
        self.field = field
        super().__init__(f"Field '{field}' does not contain Japanese characters")

class InvalidJsonError(Exception):
    """Rzucany gdy plik JSON jest nieprawidłowy"""
    def __init__(self, field: str):
        self.field = field
        super().__init__(f"JSON file is missing field '{field}'")

class InvalidFormatError(Exception):
    """Rzucany gdy nazwa talii jest nieprawidłowa"""
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(f"Invalid format: {msg}")
