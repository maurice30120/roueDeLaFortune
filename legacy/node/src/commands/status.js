const chalk = require('chalk');
const { loadJSON, CONFIG_PATH, HISTORY_PATH, ASSIGNMENTS_PATH, TOTEM_PATH } = require('../utils/fileManager');
const { getTodayDate } = require('../utils/dateHelper');
const { normalizeTotem } = require('../utils/totemManager');

// Commande: Afficher le statut
function showStatus() {
  const config = loadJSON(CONFIG_PATH);
  const history = loadJSON(HISTORY_PATH);
  const assignments = loadJSON(ASSIGNMENTS_PATH);
  
  console.log(chalk.bold.cyan('\n📊 Statut des corvées\n'));
  
  // Afficher l'historique total
  console.log(chalk.bold('Historique total :'));
  Object.entries(history)
    .sort((a, b) => a[1] - b[1])
    .forEach(([user, count]) => {
      const bar = '█'.repeat(count);
      console.log(chalk.yellow(user.padEnd(30)), chalk.cyan(bar), chalk.gray(`(${count})`));
    });
  
  console.log('');
  
  // Afficher les dernières attributions
  const today = getTodayDate();
  const todayAssignments = assignments.filter(a => a.date === today);
  
  if (todayAssignments.length > 0) {
    console.log(chalk.bold(`Attributions du jour (${today}) :`));
    todayAssignments.forEach(assignment => {
      const status = assignment.completed ? chalk.green('✓') : chalk.gray('○');
      console.log(status, chalk.bold(assignment.chore.padEnd(15)), '→', chalk.yellow(assignment.user));
    });
  } else {
    console.log(chalk.gray('Aucune attribution pour aujourd\'hui.'));
  }

  const totemRaw = loadJSON(TOTEM_PATH);
  const totem = normalizeTotem(totemRaw, config.users);
  console.log(chalk.bold('\nTotem d\'immunité :'));
  if (totem.immune.length === 0) {
    console.log(chalk.gray('  Immunisés : aucun'));
  } else {
    console.log(chalk.gray('  Immunisés :'), chalk.yellow(totem.immune.join(', ')));
  }
  if (totem.safe.length === 0) {
    console.log(chalk.gray('  À l\'abri : aucun'));
  } else {
    console.log(chalk.gray('  À l\'abri :'), chalk.cyan(totem.safe.join(', ')));
  }
  if (totem.forcedQueue.length === 0) {
    console.log(chalk.gray('  File forcée : aucune'));
  } else {
    console.log(chalk.gray('  File forcée :'), chalk.cyan(totem.forcedQueue.join(', ')));
  }
  
  // Afficher les 5 dernières attributions (hors aujourd'hui)
  const recentAssignments = assignments
    .filter(a => a.date !== today)
    .slice(-5)
    .reverse();
  
  if (recentAssignments.length > 0) {
    console.log(chalk.bold('\nDernières attributions :'));
    recentAssignments.forEach(assignment => {
      console.log(
        chalk.gray(assignment.date),
        '│',
        assignment.chore.padEnd(15),
        '→',
        chalk.yellow(assignment.user)
      );
    });
  }
  
  console.log('');
}

// Fonction pour afficher uniquement les corvées du jour
function showTodayStatus() {
  const assignments = loadJSON(ASSIGNMENTS_PATH);
  const today = getTodayDate();
  const todayAssignments = assignments.filter(a => a.date === today);
  
  if (todayAssignments.length === 0) {
    return;
  }
  
  console.log(chalk.bold.cyan('📋 Statut du jour:\n'));
  
  const completed = todayAssignments.filter(a => a.completed).length;
  const total = todayAssignments.length;
  const percentage = Math.round((completed / total) * 100);
  
  todayAssignments.forEach(assignment => {
    const status = assignment.completed ? chalk.green('✓') : chalk.gray('○');
    console.log(status, chalk.bold(assignment.chore.padEnd(15)), '→', chalk.yellow(assignment.user));
  });
  
  console.log('');
  console.log(chalk.cyan(`Progression: ${completed}/${total} (${percentage}%)`));
  
  if (completed === total) {
    console.log(chalk.green.bold('🎊 Toutes les corvées sont terminées ! Bravo ! 🎊'));
  }
  
  console.log('');
}

module.exports = {
  showStatus,
  showTodayStatus
};
