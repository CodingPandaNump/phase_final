import argparse
from datetime import datetime, date
from bourse import Bourse
from portefeuille import Portefeuille
from exceptions import *


def analyser_commande():
    parser = argparse.ArgumentParser(description="Gestionnaire de portefeuille d'actions")
    
    subparsers = parser.add_subparsers(dest='action', required=True)

    # Sous-commande 'déposer'
    parser_deposer = subparsers.add_parser('déposer', help="Déposer des liquidités dans le portefeuille")
    parser_deposer.add_argument("--date", default=date.today(), type=lambda d: date.fromisoformat(d), help="Date de dépôt (format: AAAA-MM-JJ)")
    parser_deposer.add_argument("--quantité", type=float, required=True, help="Montant à déposer")

    # Sous-commande 'acheter'
    parser_acheter = subparsers.add_parser('acheter', help="Acheter des actions")
    parser_acheter.add_argument("--date", default=date.today(), type=lambda d: date.fromisoformat(d), help="Date d'achat (format: AAAA-MM-JJ)")
    parser_acheter.add_argument("--titres", nargs='+', required=True, help="Symbole(s) des titres à acheter")
    parser_acheter.add_argument("--quantité", type=int, required=True, help="Quantité à acheter")

    # Sous-commande 'vendre'
    parser_vendre = subparsers.add_parser('vendre', help="Vendre des actions")
    parser_vendre.add_argument("--date", default=date.today(), type=lambda d: date.fromisoformat(d), help="Date de vente (format: AAAA-MM-JJ)")
    parser_vendre.add_argument("--titres", nargs='+', required=True, help="Symbole(s) des titres à vendre")
    parser_vendre.add_argument("--quantité", type=int, required=True, help="Quantité à vendre")

    # Sous-commande 'lister'
    parser_lister = subparsers.add_parser('lister', help="Lister les actions du portefeuille")
    parser_lister.add_argument("--date", default=date.today(), type=lambda d: date.fromisoformat(d), help="Date pour la liste (format: AAAA-MM-JJ)")

    # Sous-commande 'projeter'
    parser_projeter = subparsers.add_parser('projeter', help="Projeter la valeur future du portefeuille")
    parser_projeter.add_argument("--date", required=True, type=lambda d: date.fromisoformat(d), help="Date future de projection (format: AAAA-MM-JJ)")
    parser_projeter.add_argument("--rendement", type=float, required=True, help="Rendement annuel attendu (en %)")
    parser_projeter.add_argument("--volatilité", type=float, default=0.0, help="Indice de volatilité sur le rendement annuel (par défaut, 0)")



def main():
    args = analyser_commande()
    bourse = Bourse()
    portefeuille = Portefeuille(bourse)

    if args.action == "déposer":
        # Logique pour déposer
        montant = portefeuille.deposer(args.quantité, args.date)
        print(f"solde = {montant:.2f}")

    elif args.action == "acheter":
        # Logique pour acheter
        for titre in args.titres:
            portefeuille.acheter(titre, args.quantité, args.date)
        solde = portefeuille.solde(args.date)
        print(f"solde = {solde:.2f}")

    elif args.action == "vendre":
        # Logique pour vendre
        for titre in args.titres:
            portefeuille.vendre(titre, args.quantité, args.date)
        solde = portefeuille.solde(args.date)
        print(f"solde = {solde:.2f}")
    elif args.action == "lister":
        # Logique pour lister
        actions = portefeuille.lister(args.date)
        for symbole, (quantité, prix, montant) in actions.items():
            print(f"{symbole} = {quantité} x {prix:.2f} = {montant:.2f}")

    elif args.action == "projeter":
        # Logique pour projeter
        valeur_projete = portefeuille.projeter(args.date, args.rendement, args.volatilité)
        print(f"valeur projetée = {valeur_projete:.2f}")

if __name__ == "__main__":
    main()