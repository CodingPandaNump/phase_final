"""
 Importation des modules necessaire
    """
from datetime import date
from exceptions import *




class Portefeuille:
    """
    Classe représentant un portefeuille d'actions mobilières.

    Méthodes :
        - __init__(self, bourse: Bourse) -> None
        - deposer(self, montant: float, date: date = None) -> None
        - solde(self, date: date = None) -> float
        - acheter(self, symbole: str, quantite: int, date: date = None) -> None
        - vendre(self, symbole: str, quantite: int, date: date = None) -> None
        - valeur_totale(self, date: date = None) -> float
        - valeur_des_titres(self, symboles: Iterable[str], date: date = None) -> float
        - titres(self, date: date = None) -> Dict[str, int]
        - valeur_projetee(self, date: date, rendement: Union[float, Dict[str, float]]) -> float
        """

    def __init__(self, bourse):
        """
        Constructeur de la classe Portefeuille.

        Args:
            bourse (Bourse): Une instance de la classe Bourse.
        """
        self.bourse = bourse
        self.transactions = []


    def deposer(self, montant, date_transaction=None):
        """
        Effectue le dépôt d'un montant liquide dans le portefeuille à la date spécifiée.

        Args:
            montant (float): Montant en dollars à déposer.
            date (date, optionnel): Date de la transaction. Par défaut, la date du jour.
        """
        if date_transaction is None:
            date_transaction = date.today()

            if date_transaction > date.today():
                raise ErreurDate("La date de la transaction est postérieure à la date actuelle.")

            self.transactions.append({'type': 'depot',
                                       'montant': montant, 'date': date_transaction})


    def solde(self, date_evaluation=None):
        """
        Retourne le solde des liquidités du portefeuille à la date spécifiée.

        Args:
            date (date, optionnel): Date d'évaluation. Par défaut, la date du jour.

        Returns:
            float: Solde des liquidités.
        """
        if date_evaluation is None:
            date_evaluation = date.today()

        if date_evaluation > date.today():
            raise ErreurDate("La date d'évaluation est postérieure à la date actuelle.")

        solde_liquide = 0
        for trans in self.transactions:
            if trans['type'] == 'depot' and trans['date'] <= date_evaluation:
                solde_liquide += trans['montant']

        return solde_liquide


    def acheter(self, symbole, qte, date_transaction=None):
        """
        Effectue l'achat d'une quantité d'actions d'un titre à la date spécifiée.

        Args:
            symbole (str): Symbole du titre.
            quantite (int): Quantité d'actions à acheter.
            date (date, optionnel): Date de la transaction. Par défaut, la date du jour.
        """
        if date_transaction is None:
            date_transaction = date.today()

        if date_transaction > date.today():
            raise ErreurDate("La date de la transaction est postérieure à la date actuelle.")

        prix_action = self.bourse.prix(symbole, date_transaction)
        cout_total = prix_action + qte

        solde_liquide = self.solde(date_transaction)
        if cout_total > solde_liquide:
            raise LiquiditéInsuffisante("Liquidité insuffisante pour effectuer l'achat.")

        self.transactions.append({'type': 'achat', 'symbole': symbole,
                                   'quantite': qte, 'prix_unitaire': prix_action,
                                    'date': date_transaction})


    def vendre(self, symbole, qte, date_transaction=None):
        """
        Effectue la vente d'une quantité d'actions d'un titre à la date spécifiée.

        Args:
            symbole (str): Symbole du titre.
            quantite (int): Quantité d'actions à vendre.
            date (date, optionnel): Date de la transaction. Par défaut, la date du jour.
        """
        if date_transaction is None:
            date_transaction = date.today()

        if date_transaction > date.today():
            raise ErreurDate("La date de la transaction est postérieure à la date actuelle.")

        actions_en_portefeuille = 0
        for trans in self.transactions:
            if trans['type'] == 'achat' and trans['symbole'] == symbole:
                actions_en_portefeuille += trans['quantite']

        if qte > actions_en_portefeuille:
            raise ErreurQuantité("Quantité d'actions insuffisante pour effectuer la vente.")

        prix_action = self.bourse.prix(symbole, date_transaction)
        montant_total = prix_action * qte

        self.transactions.append({'type': 'vente', 'symbole': symbole, 'quantite': qte,
                                  'prix_unitaire': prix_action, 'date': date_transaction})
        self.transactions.append({'type': 'depot', 'montant': montant_total,
                                  'date': date_transaction})


    def valeur_totale(self, date_evaluation=None):
        """
        Retourne la valeur totale des titres spécifiés à la date spécifiée.

        Args:
            symboles (Iterable[str]): Symboles des titres.
            date (date, optionnel): Date d'évaluation. Par défaut, la date du jour.

        Returns:
            float: Valeur totale des titres spécifiés.
        """
        if date_evaluation is None:
            date_evaluation = date.today()

        if date_evaluation > date.today():
            raise ErreurDate("La date d'évaluation est postérieure à la date actuelle.")

        valeur_liquide = self.solde(date_evaluation)


        for trans in self.transactions:
            if trans['type'] == 'achat':
                valeur_liquide += self.bourse.prix(trans['symbole'],
                                                   date_evaluation) * trans['quantite']

        return valeur_liquide

    def valeur_des_titres(self, symboles, date_evaluation=None):
        """
        Calcule la valeur totale des titres spécifiés dans le portefeuille à la date d'évaluation.

        Args:
            symboles (iterable): Un itérable de symboles boursiers.
            date_evaluation (datetime.date, optional): La date d'évaluation.
            Par défaut, utilise la date du jour.

        Returns:
            float: La valeur totale des titres spécifiés.
        
        Raises:
            ErreurDate: Si la date d'évaluation est postérieure à la date actuelle.
    """
        if date_evaluation is None:
            date_evaluation = date.today()

        if date_evaluation > date.today():
            raise ErreurDate("La date d'évaluation est postérieure à la date actuelle.")

        valeur_total = 0.00
        for symb in symboles:
            actions_en_portefeuille = 0
            for trans in self.transactions:
                if trans['type'] == 'achat' and trans['symbole'] == symboles:
                    actions_en_portefeuille += trans['quantite']

        prix_actuel = self.bourse.prix(symboles, date_evaluation)
        valeur_total += actions_en_portefeuille * prix_actuel

        return valeur_total


    def titres(self, date_evaluation=None):
        """
    Retourne un dictionnaire des symboles de
    tous les titres du portefeuille à la date d'évaluation,
    avec les quantités d'actions détenues pour ces titres.

    Args:
        date_evaluation (datetime.date, optional):
        La date d'évaluation. Par défaut, utilise la date du jour.

    Returns:
        dict: Un dictionnaire des symboles des titres avec les quantités d'actions détenues.

    Raises:
        ErreurDate: Si la date d'évaluation est postérieure à la date actuelle.
    """
        if date_evaluation is None:
            date_evaluation = date.today()

        if date_evaluation > date.today():
            raise ErreurDate("La date d'évaluation est postérieure à la date actuelle.")

        titres_en_portefeuille = {}
        for trans in self.transactions:
            if trans['type'] == 'achat' and trans['date'] <= date_evaluation:
                symbole = trans['symbole']
                quantite = trans['quantite']
                if symbole in titres_en_portefeuille:
                    titres_en_portefeuille[symbole] += quantite
                else:
                    titres_en_portefeuille = quantite

        return titres_en_portefeuille

    def valeur_projetee(self, date_future, rendement):
        """
    Retourne la valeur projetée du portefeuille à une
    date future en supposant le ou les rendements spécifiés.

    Args:
        date_future (datetime.date): La date future pour la projection.
        rendement (float ou dict): Le rendement annuel. 
        Peut être un float pour un rendement fixe
        ou un dictionnaire de rendements associés à des symboles spécifiques.

    Returns:
        float: La valeur projetée du portefeuille à la date future.

    Raises:
        ErreurDate: Si la date future est antérieure à la date actuelle.
    """
        if date_future < date.today():
            raise ErreurDate("La date future est antérieure à la date actuelle.")

        valeur_projetee = 0.00

        for trans in self.transactions:
            if trans['date'] > date_future:
                break

            if trans['type'] == 'depot':
                valeur_projetee += trans['montant']
            elif trans['type'] == 'achat':
                symbole = trans['symbole']
                quantite = trans['quantite']
                prix_actuel = self.bourse.prix(symbole, date_future)
            if isinstance(rendement, dict):
                rendement_titre =  rendement.get(symbole, rendement)
            else:
                rendement_titre = rendement
            valeur_projetee += quantite * prix_actuel * (1 + rendement_titre / 100)

        return valeur_projetee
