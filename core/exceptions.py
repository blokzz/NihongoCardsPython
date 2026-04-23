class EmptyDeckError(Exception):
    """Rzucany gdy próbujemy rozpocząć sesję z pustą talią"""
    pass

class InvalidCardError(Exception):
    """Rzucany gdy karta nie zawiera japońskich znaków"""
    pass