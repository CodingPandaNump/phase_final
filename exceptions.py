"""Class dexception custom pour gerer les erreurs."""

class ErreurDate(RuntimeError):
    """Exception raised pour les dates invalides."""

    def __init__(self, message="Erreur de date"):
        self.message = message
        super().__init__(self.message)


class ErreurQuantité(RuntimeError):
    """Exception raised pour les erreurs de quantites."""

    def __init__(self, message="Erreur de quantité"):
        self.message = message
        super().__init__(self.message)


class LiquiditéInsuffisante(RuntimeError):
    """Exception raised pour les erreus de liquidites."""

    def __init__(self, message="Liquidité insuffisante"):
        self.message = message
        super().__init__(self.message)
