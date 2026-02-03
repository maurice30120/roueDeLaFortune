from ..utils.console import get_console


def show_help() -> None:
    console = get_console()

    console.print("[bold cyan]\n🏠 Gestionnaire de corvées - Aide\n[/]")

    console.print("[bold]Par défaut :\n[/]")
    console.print("[green]  assign[/]                    talomi x3 (3 personnes, auto)")
    console.print("[green]  complete[/]                  talomi --all (3 personnes du jour)")

    console.print("[bold]\nCommandes disponibles :\n[/]")

    console.print("[yellow]  assign[/]                    Répartir 3 corvées \"talomi\" en mode auto (à 3 personnes)")
    console.print("[yellow]  assign --count N[/]         Attribuer N fois la corvée par défaut")
    console.print("[yellow]  assign <corvée> --count N[/]Attribuer une corvée N fois")
    console.print("[yellow]  assign --auto[/]           Répartir en mode automatique (déjà activé par défaut)")
    console.print("[yellow]  assign --force (-f)[/]       Forcer l'attribution même si déjà fait")
    console.print("[yellow]  assign --no-anim[/]          Désactiver les animations")
    console.print("[yellow]  status[/]                   Afficher le statut et l'historique")
    console.print("[yellow]  complete[/]                 Marquer une corvée comme terminée (talomi --all, 3 personnes)")
    console.print("[yellow]  complete --all[/]          Marquer toutes les occurrences comme terminées")
    console.print("[yellow]  totem[/]                    Afficher l'état du totem")
    console.print("[yellow]  totem add <utilisateur>[/]Ajouter un utilisateur immunisé")
    console.print("[yellow]  totem remove <utilisateur>[/]Retirer un utilisateur immunisé")
    console.print("[yellow]  totem safe[/]               Afficher les utilisateurs à l'abri")
    console.print("[yellow]  totem safe add <utilisateur>[/]Ajouter un utilisateur à l'abri")
    console.print("[yellow]  totem safe remove <utilisateur>[/]Retirer un utilisateur à l'abri")
    console.print("[yellow]  totem safe clear[/]        Réinitialiser la liste à l'abri")
    console.print("[yellow]  totem clear[/]           Réinitialiser le totem")
    console.print("[yellow]  reset[/]                    Réinitialiser l'historique")
    console.print("[yellow]  help[/]                     Afficher cette aide")

    console.print("[bold]\nExemples :\n[/]")

    console.print("[grey70]  python app.py assign   # équivaut à --count 3 --auto talomi[/]")
    console.print("[grey70]  python app.py assign --count 3[/]")
    console.print("[grey70]  python app.py assign Aspirateur --count 3[/]")
    console.print("[grey70]  python app.py assign Vaisselle --count 2[/]")
    console.print("[grey70]  python app.py assign -f[/]")
    console.print("[grey70]  python app.py assign --no-anim[/]")
    console.print("[grey70]  python app.py status[/]")
    console.print("[grey70]  python app.py complete   # équivaut à talomi --all[/]")
    console.print("[grey70]  python app.py complete 1[/]")
    console.print("[grey70]  python app.py complete Vaisselle[/]")
    console.print("[grey70]  python app.py complete Vaisselle -p Alice[/]")
    console.print("[grey70]  python app.py complete Aspirateur --all[/]")
    console.print("[grey70]  python app.py totem[/]")
    console.print("[grey70]  python app.py totem add \"Alice Dupont\"[/]")
    console.print("[grey70]  python app.py totem remove \"Alice Dupont\"[/]")
    console.print("[grey70]  python app.py totem safe[/]")
    console.print("[grey70]  python app.py totem safe add \"Alice Dupont\"[/]")
    console.print("[grey70]  python app.py totem safe remove \"Alice Dupont\"[/]")
    console.print("[grey70]  python app.py totem safe clear[/]")
    console.print("[grey70]  python app.py totem clear[/]")

    console.print("")
