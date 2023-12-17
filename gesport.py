import argparse
from datetime import datetime, date
from bourse import Bourse
from portefeuille import Portefeuille
from exceptions import *


def analyser_commande():
    parser = argparse.ArgumentParser(description="Gestionnaire de portefeuille d'actions.")
    
    parser.add_argument("action", help="Nom de l'action à gérer")
    parser.add_argument("-d", "--date", default=date.today(), type=lambda d: date.fromisoformat(d),
                        help="Date effective (par défaut, date du jour)")
    parser.add_argument("-q", "--quantité", default=1, type=int,
                        help="Quantité désirée (par défaut: 1)")
    parser.add_argument("-t", "--titres", nargs='*', default=None,
                        help="Le ou les titres à considérer (par défaut, tous les titres du portefeuille)")
    parser.add_argument("-r", "--rendement", default=0.0, type=float,
                        help="Rendement annuel global (par défaut, 0)")
    parser.add_argument("-v", "--volatilité", default=0.0, type=float,
                        help="Indice de volatilité global sur le rendement annuel (par défaut, 0)")
    parser.add_argument("-g", "--graphique", action='store_true',
                        help="Affichage graphique (par défaut, pas d'affichage graphique)")
    parser.add_argument("-p", "--portefeuille", default="folio", type=str,
                        help="Nom de portefeuille (par défaut, utiliser 'folio')")

    args = parser.parse_args()

    # Correction des valeurs par défaut si nécessaire
    if args.début is None and args.fin:
        args.début = args.fin

    if args.fin is None and args.début:
        args.fin = args.début

    if args.début == args.fin:
        args.fin = args.début
    
    return args

def main():
    args = analyser_commande()

    # Initialisation des objets Bourse et Portefeuille
    bourse = Bourse()
    portefeuille = Portefeuille(bourse, args.portefeuille)

    # Traitement des différentes actions basées sur les arguments de la ligne de commande
    if args.action == "acheter":
        # Vérification et achat des titres spécifiés
        for titre in args.titres:
            portefeuille.acheter(titre, args.quantité, args.date)
    elif args.action == "vendre":
        # Vérification et vente des titres spécifiés
        for titre in args.titres:
            portefeuille.vendre(titre, args.quantité, args.date)
    

    # Gérer l'affichage graphique si demandé
    if args.graphique:
        # Code pour générer et afficher le graphique
        pass

    # Traiter les options de rendement et de volatilité
    if args.rendement or args.volatilité:
        # Code pour gérer le rendement et la volatilité
        pass

    # Traiter les autres options/arguments selon les besoins

if __name__ == "__main__":
    main()


