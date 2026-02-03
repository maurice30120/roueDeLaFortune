const chalk = require('chalk');

// Commande: Aide
function showHelp() {
  console.log(chalk.bold.cyan('\n🏠 Gestionnaire de corvées - Aide\n'));
  
  console.log(chalk.bold('Par défaut :\n'));
  console.log(chalk.green('  assign'), '                    talomi x3 (3 personnes, auto)');
  console.log(chalk.green('  complete'), '                  talomi --all (3 personnes du jour)');
  
  console.log(chalk.bold('\nCommandes disponibles :\n'));
  
  console.log(chalk.yellow('  assign'), '                    Répartir 3 corvées "talomi" en mode auto (à 3 personnes)');
  console.log(chalk.yellow('  assign --count N'), '         Attribuer N fois la corvée par défaut');
  console.log(chalk.yellow('  assign <corvée> --count N'), 'Attribuer une corvée N fois');
  console.log(chalk.yellow('  assign --auto'), '           Répartir en mode automatique (déjà activé par défaut)');
  console.log(chalk.yellow('  assign --force (-f)'), '       Forcer l\'attribution même si déjà fait');
  console.log(chalk.yellow('  status'), '                   Afficher le statut et l\'historique');
  console.log(chalk.yellow('  complete'), '                 Marquer une corvée comme terminée (talomi --all, 3 personnes)');
  console.log(chalk.yellow('  complete --all'), '          Marquer toutes les occurrences comme terminées');
  console.log(chalk.yellow('  totem'), '                    Afficher l\'état du totem');
  console.log(chalk.yellow('  totem add <utilisateur>'), 'Ajouter un utilisateur immunisé');
  console.log(chalk.yellow('  totem remove <utilisateur>'), 'Retirer un utilisateur immunisé');
  console.log(chalk.yellow('  totem safe'), '               Afficher les utilisateurs à l\'abri');
  console.log(chalk.yellow('  totem safe add <utilisateur>'), 'Ajouter un utilisateur à l\'abri');
  console.log(chalk.yellow('  totem safe remove <utilisateur>'), 'Retirer un utilisateur à l\'abri');
  console.log(chalk.yellow('  totem safe clear'), '        Réinitialiser la liste à l\'abri');
  console.log(chalk.yellow('  totem clear'), '           Réinitialiser le totem');
  console.log(chalk.yellow('  reset'), '                    Réinitialiser l\'historique');
  console.log(chalk.yellow('  help'), '                     Afficher cette aide');
  
  console.log(chalk.bold('\nScripts npm :\n'));
  
  console.log(chalk.yellow('  npm run assign'), ' Répartir les corvées');
  console.log(chalk.yellow('  npm run status'), ' Voir le statut');
  console.log(chalk.yellow('  npm run reset'), '  Réinitialiser');
  
  console.log(chalk.bold('\nExemples :\n'));
  
  console.log(chalk.gray('  node app.js assign   # équivaut à --count 3 --auto talomi'));
  console.log(chalk.gray('  node app.js assign --count 3'));
  console.log(chalk.gray('  node app.js assign Aspirateur --count 3'));
  console.log(chalk.gray('  node app.js assign Vaisselle --count 2'));
  console.log(chalk.gray('  node app.js assign -f'));
  console.log(chalk.gray('  node app.js status'));
  console.log(chalk.gray('  node app.js complete   # équivaut à talomi --all'));
  console.log(chalk.gray('  node app.js complete 1'));
  console.log(chalk.gray('  node app.js complete Vaisselle'));
  console.log(chalk.gray('  node app.js complete Vaisselle -p Alice'));
  console.log(chalk.gray('  node app.js complete Aspirateur --all'));
  console.log(chalk.gray('  node app.js totem'));
  console.log(chalk.gray('  node app.js totem add "Alice Dupont"'));
  console.log(chalk.gray('  node app.js totem remove "Alice Dupont"'));
  console.log(chalk.gray('  node app.js totem safe'));
  console.log(chalk.gray('  node app.js totem safe add "Alice Dupont"'));
  console.log(chalk.gray('  node app.js totem safe remove "Alice Dupont"'));
  console.log(chalk.gray('  node app.js totem safe clear'));
  console.log(chalk.gray('  node app.js totem clear'));
  
  console.log('');
}

module.exports = {
  showHelp
};
