const chalk = require('chalk');
const { loadJSON, saveJSON, ASSIGNMENTS_PATH } = require('../utils/fileManager');
const { getTodayDate } = require('../utils/dateHelper');
const { showTodayStatus } = require('./status');

// Commande: Marquer une corvée comme terminée
function completeChore(choreName, userName, allMode = false) {
  const assignments = loadJSON(ASSIGNMENTS_PATH);
  const today = getTodayDate();
  
  // Trouver les assignments d'aujourd'hui
  const todayAssignments = assignments.filter(a => a.date === today);
  
  if (todayAssignments.length === 0) {
    console.log(chalk.yellow('\n⚠️  Aucune corvée attribuée pour aujourd\'hui.'));
    console.log(chalk.gray('Utilisez "node app.js assign" pour attribuer les corvées.\n'));
    return;
  }
  
  // Si aucun argument, afficher les corvées du jour pour sélection
  if (!choreName) {
    console.log(chalk.bold.cyan('\n🏠 Corvées du jour\n'));
    console.log(chalk.gray(`Date : ${today}\n`));
    
    todayAssignments.forEach((assignment, index) => {
      const status = assignment.completed ? chalk.green('✓') : chalk.gray('○');
      console.log(`${index + 1}.`, status, chalk.bold(assignment.chore.padEnd(15)), '→', chalk.yellow(assignment.user));
    });
    
    console.log(chalk.gray('\nUtilisation: node app.js complete <numéro ou nom de la corvée> [-p|--person <nom>] [--all]'));
    console.log(chalk.gray('Par défaut: node app.js complete  ≡  talomi --all (3 personnes)'));
    console.log(chalk.gray('Exemples:'));
    console.log(chalk.gray('  node app.js complete 1'));
    console.log(chalk.gray('  node app.js complete Vaisselle'));
    console.log(chalk.gray('  node app.js complete Vaisselle -p Alice'));
    console.log(chalk.gray('  node app.js complete Aspirateur --all\n'));
    return;
  }
  
  // Rechercher la corvée (par numéro ou par nom)
  let targetAssignment = null;
  let assignmentIndex = -1;
  
  // Essayer de parser comme un numéro
  const choreNum = parseInt(choreName);
  if (!isNaN(choreNum) && choreNum > 0 && choreNum <= todayAssignments.length) {
    targetAssignment = todayAssignments[choreNum - 1];
    assignmentIndex = assignments.findIndex(a => 
      a.date === targetAssignment.date && 
      a.chore === targetAssignment.chore && 
      a.user === targetAssignment.user
    );
  } else {
    // Rechercher par nom de corvée
    const matchingAssignments = todayAssignments.filter(a => 
      a.chore.toLowerCase().includes(choreName.toLowerCase())
    );
    
    if (matchingAssignments.length === 0) {
      console.log(chalk.red(`\n❌ Corvée "${choreName}" non trouvée pour aujourd'hui.\n`));
      return;
    }
    
    // Mode --all : marquer toutes les occurrences
    if (allMode) {
      let completedCount = 0;
      
      matchingAssignments.forEach(matching => {
        if (!matching.completed) {
          const idx = assignments.findIndex(a => 
            a.date === matching.date && 
            a.chore === matching.chore && 
            a.user === matching.user
          );
          if (idx !== -1) {
            assignments[idx].completed = true;
            completedCount++;
          }
        }
      });
      
      saveJSON(ASSIGNMENTS_PATH, assignments);
      
      if (completedCount === 0) {
        console.log(chalk.yellow(`\n⚠️  Toutes les corvées "${choreName}" sont déjà marquées comme terminées.\n`));
      } else {
        console.log(chalk.green(`\n✓ ${completedCount} corvée(s) "${choreName}" marquée(s) comme terminée(s) !\n`));
        matchingAssignments.forEach(a => {
          console.log(chalk.gray('  •'), chalk.bold(a.chore), '→', chalk.yellow(a.user));
        });
        console.log(chalk.gray('\nBon travail ! 🎉\n'));
      }
      
      // Afficher le statut mis à jour
      showTodayStatus();
      return;
    }
    
    // Si plusieurs correspondances et pas de nom d'utilisateur spécifié
    if (matchingAssignments.length > 1 && !userName) {
      console.log(chalk.yellow(`\n⚠️  Plusieurs corvées correspondent à "${choreName}":\n`));
      matchingAssignments.forEach((a, i) => {
        const status = a.completed ? chalk.green('✓') : chalk.gray('○');
        console.log(`${i + 1}.`, status, chalk.bold(a.chore), '→', chalk.yellow(a.user));
      });
      console.log(chalk.gray('\nSpécifiez le nom d\'utilisateur: node app.js complete', choreName, '-p <nom>'));
      console.log(chalk.gray('Ou utilisez --all pour toutes les marquer: node app.js complete', choreName, '--all\n'));
      return;
    }
    
    // Filtrer par utilisateur si spécifié
    if (userName) {
      targetAssignment = matchingAssignments.find(a => 
        a.user.toLowerCase() === userName.toLowerCase()
      );
      if (!targetAssignment) {
        console.log(chalk.red(`\n❌ Corvée "${choreName}" non attribuée à "${userName}" aujourd'hui.\n`));
        return;
      }
    } else {
      targetAssignment = matchingAssignments[0];
    }
    
    assignmentIndex = assignments.findIndex(a => 
      a.date === targetAssignment.date && 
      a.chore === targetAssignment.chore && 
      a.user === targetAssignment.user
    );
  }
  
  // Marquer comme complétée
  if (targetAssignment.completed) {
    console.log(chalk.yellow(`\n⚠️  La corvée "${targetAssignment.chore}" (${targetAssignment.user}) est déjà marquée comme terminée.\n`));
    return;
  }
  
  assignments[assignmentIndex].completed = true;
  saveJSON(ASSIGNMENTS_PATH, assignments);
  
  console.log(chalk.green('\n✓ Corvée terminée !'));
  console.log(chalk.bold(targetAssignment.chore), '→', chalk.yellow(targetAssignment.user));
  console.log(chalk.gray('Bon travail ! 🎉\n'));
  
  // Afficher le statut mis à jour des corvées du jour
  showTodayStatus();
}

module.exports = {
  completeChore
};
