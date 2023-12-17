import argparse
from datetime import datetime, date
from bourse import Bourse
from portefeuille import Portefeuille
from exceptions import *


bourse = Bourse()
portefeuille = Portefeuille(bourse)

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError("La date doit être au format AAAA-MM-JJ")

# surement pas le meilleur moyen mais ca marche
def handle_deposer(args):
    montant = args.quantité
    date_depot = args.date

    try:
        portefeuille.deposer(montant, date_depot)
        print(f"Montant de {montant:.2f} déposé le {date_depot}. Nouveau solde: {portefeuille.solde(date_depot):.2f}")
    except Exception as e:
        print(f"Erreur lors du dépôt: {e}")


def handle_acheter(args):
    montant_total = 0
    for titre in args.titres:
        prix = bourse.prix(titre, args.date)
        cout = prix * args.quantité
        montant_total += cout
        portefeuille.acheter(titre, args.quantité, args.date)
        print(f"Achat de {args.quantité} actions de {titre} à {prix:.2f} chacune pour un total de {cout:.2f}")
    print(f"Coût total des achats: {montant_total:.2f}")


def handle_vendre(args):
    montant_total = 0
    for titre in args.titres:
        prix = bourse.prix(titre, args.date)
        revenu = prix * args.quantité
        montant_total += revenu
        portefeuille.vendre(titre, args.quantité, args.date)
        print(f"Vente de {args.quantité} actions de {titre} à {prix:.2f} chacune pour un total de {revenu:.2f}")
    print(f"Revenu total des ventes: {montant_total:.2f}")


def handle_lister(args):
    actions = portefeuille.lister(args.date)
    for symbole, quantité in actions.items():
        print(f"{symbole}: {quantité} actions")


def handle_projeter(args):
    valeur_projete = portefeuille.valeur_projetee(args.date, args.rendement, args.volatilité)
    print(f"Valeur projetée du portefeuille à la date {args.date}: {valeur_projete:.2f}")


def analyser_commande():
    parser = argparse.ArgumentParser(description="Gestionnaire de portefeuille d'actions")
    subparsers = parser.add_subparsers(dest='action', required=True)

    # Sous-commande 'déposer'
    parser_deposer = subparsers.add_parser('déposer', help="Déposer des liquidités dans le portefeuille")
    parser_deposer.add_argument("--date", default=date.today(), type=parse_date, help="Date de dépôt (format: AAAA-MM-JJ)")
    parser_deposer.add_argument("--quantité", type=float, required=True, help="Montant à déposer")
    parser_deposer.set_defaults(func=handle_deposer)

    # Sous-commande 'acheter'
    parser_acheter = subparsers.add_parser('acheter', help="Acheter des actions")
    parser_acheter.add_argument("--date", default=date.today(), type=parse_date, help="Date d'achat (format: AAAA-MM-JJ)")
    parser_acheter.add_argument("--titres", nargs='+', required=True, help="Symbole(s) des titres à acheter")
    parser_acheter.add_argument("--quantité", type=int, required=True, help="Quantité à acheter")
    parser_acheter.set_defaults(func=handle_acheter)

    # Sous-commande 'vendre'
    parser_vendre = subparsers.add_parser('vendre', help="Vendre des actions")
    parser_vendre.add_argument("--date", default=date.today(), type=parse_date, help="Date de vente (format: AAAA-MM-JJ)")
    parser_vendre.add_argument("--titres", nargs='+', required=True, help="Symbole(s) des titres à vendre")
    parser_vendre.add_argument("--quantité", type=int, required=True, help="Quantité à vendre")
    parser_vendre.set_defaults(func=handle_vendre)

    # Sous-commande 'lister'
    parser_lister = subparsers.add_parser('lister', help="Lister les actions du portefeuille")
    parser_lister.add_argument("--date", default=date.today(), type=parse_date, help="Date pour la liste (format: AAAA-MM-JJ)")
    parser_lister.set_defaults(func=handle_lister)

    # Sous-commande 'projeter'
    parser_projeter = subparsers.add_parser('projeter', help="Projeter la valeur future du portefeuille")
    parser_projeter.add_argument("--date", required=True, type=parse_date, help="Date future de projection (format: AAAA-MM-JJ)")
    parser_projeter.add_argument("--rendement", type=float, required=True, help="Rendement annuel attendu (en %)")
    parser_projeter.add_argument("--volatilité", type=float, default=0.00, help="Indice de volatilité sur le rendement annuel (par défaut, 0)")
    parser_projeter.set_defaults(func=handle_projeter)

    return parser.parse_args()


def main():
    args = analyser_commande()
    #bourse = Bourse()
    #portefeuille = Portefeuille(bourse)

    if hasattr(args, 'func'):
        args.func(args)
    else:
        print("Aucune sous-commande fournie. Affichez l'aide.")


if __name__ == "__main__":
    main()

