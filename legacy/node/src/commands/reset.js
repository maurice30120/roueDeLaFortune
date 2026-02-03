const chalk = require('chalk');
const { loadJSON, saveJSON, CONFIG_PATH, HISTORY_PATH, ASSIGNMENTS_PATH, TOTEM_PATH } = require('../utils/fileManager');

// Commande: Réinitialiser
function reset() {
  const config = loadJSON(CONFIG_PATH);
  
  // Demander confirmation
  console.log(chalk.yellow('\n⚠️  Attention : Cette action va réinitialiser tout l\'historique !'));
  console.log(chalk.gray('Appuyez sur Ctrl+C pour annuler, ou Entrée pour continuer...'));
  
  process.stdin.once('data', () => {
    // Réinitialiser l'historique
    const freshHistory = {};
    config.users.forEach(user => {
      freshHistory[user] = 0;
    });
    
    // Réinitialiser les attributions
    const freshAssignments = [];
    const freshTotem = { immune: [], forcedQueue: [], safe: [] };
    
    // Sauvegarder
    saveJSON(HISTORY_PATH, freshHistory);
    saveJSON(ASSIGNMENTS_PATH, freshAssignments);
    saveJSON(TOTEM_PATH, freshTotem);
    
    console.log(chalk.green('\n✓ Historique réinitialisé avec succès !\n'));
    process.exit(0);
  });
}

module.exports = {
  reset
};
