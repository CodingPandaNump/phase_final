# Importation
from datetime import datetime
import requests
from exceptions import ErreurDate



class Bourse:
    """
    Represents a financial market for retrieving historical stock prices.

    Methods:
        - __init__(self) -> None:
            Initializes the Bourse object.

        - prix(self, symbole: str, date_interet: date) -> float:
            Retrieves the closing price of a stock symbol on a specific date.

            Args:
                symbole (str): The stock symbol.
                date_interet (date): The date for which the closing price is requested.

            Returns:
                float: The closing price of the stock on the specified date.

            Raises:
                ErreurDate: If the requested date is later than the current date.
                requests.exceptions.HTTPError: If the API request fails.
    """
    def __init__(self):
        """
        ajouter d'autres configurations ici si nécessaire
            """

        pass

    def prix(self, symbole, date_interet):
        """
        Retrieves the closing price of a stock symbol on a specific date.

        Args:
            symbole (str): The stock symbol.
            date_interet (date): The date for which the closing price is requested.

        Returns:
            float: The closing price of the stock on the specified date.

        Raises:
            ErreurDate: If the requested date is later than the current date.
            requests.exceptions.HTTPError: If the API request fails.
        """
        url = f'https://pax.ulaval.ca/action/{symbole}/historique/'

        params = {
            'début': date_interet,
            'fin': date_interet,
        }

        # API request
        response = requests.get(url=url, params=params)
        response.raise_for_status()  # Raise exception if request fails

        print(response.json())

        # Utilisation de historique au lieu d'une compréhension inutile
        historique = response.json()['historique']



        date_actuelle = datetime.now().date()
        if date_interet > date_actuelle:
            raise ErreurDate("La date demandée est postérieure à la date actuelle.")

        # Récupère la valeur de fermeture la plus récente avant la date spécifiée
        for date_historique, valeurs in sorted(historique.items(), reverse=True):
            date_historique = datetime.strptime(date_historique, '%Y-%m-%d').date()
            if date_historique <= date_interet:
                return valeurs['fermeture']

        raise ErreurDate("Aucune valeur de fermeture disponible avant la date spécifiée.")
