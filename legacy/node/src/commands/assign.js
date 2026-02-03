const chalk = require('chalk');
const gradient = require('gradient-string');
const { loadJSON, saveJSON, CONFIG_PATH, HISTORY_PATH, ASSIGNMENTS_PATH, TOTEM_PATH } = require('../utils/fileManager');
const { getTodayDate } = require('../utils/dateHelper');
const { selectUserForChore } = require('../utils/userSelector');
const { normalizeTotem } = require('../utils/totemManager');
const { spinWheel, showTitle } = require('../animations/spinner');

// Vérifier si une attribution existe déjà aujourd'hui
function hasAssignmentToday(assignments) {
  const today = getTodayDate();
  return assignments.some(assignment => assignment.date === today);
}

// Commande: Répartir les corvées
async function assignChores(autoMode = false, count = null, specificChore = null, forceMode = false) {
  const config = loadJSON(CONFIG_PATH);
  const history = loadJSON(HISTORY_PATH);
  const assignments = loadJSON(ASSIGNMENTS_PATH);
  
  const today = getTodayDate();
  
  // Vérifier si des attributions existent déjà aujourd'hui
  if (autoMode && hasAssignmentToday(assignments) && !forceMode) {
    console.log(chalk.yellow('⚠️  Les corvées ont déjà été attribuées aujourd\'hui (mode auto).'));
    return;
  }
  
  // Afficher le titre animé
  showTitle();

  // Charger et normaliser le totem
  const totemRaw = loadJSON(TOTEM_PATH);
  let { immune, forcedQueue, safe } = normalizeTotem(totemRaw, Object.keys(history));
  const safeSet = new Set(safe);
  
  // Déterminer les corvées à attribuer
  let choresToAssign = [];
  
  // Cas 1: Corvée spécifique avec count
  if (specificChore && count !== null) {
    // Vérifier que la corvée existe
    const matchingChores = config.chores.filter(c => 
      c.toLowerCase().includes(specificChore.toLowerCase())
    );
    
    if (matchingChores.length === 0) {
      console.log(chalk.red(`\n❌ Corvée "${specificChore}" non trouvée dans la configuration.\n`));
      console.log(chalk.gray('Corvées disponibles:'));
      config.chores.forEach(c => console.log(chalk.gray(`  • ${c}`)));
      console.log('');
      return;
    }
    
    const choreToAssign = matchingChores[0];
    const numCount = parseInt(count);
    
    if (isNaN(numCount) || numCount < 1) {
      console.log(chalk.red('\n❌ Le nombre doit être un nombre positif.\n'));
      return;
    }
    
    // Créer un tableau avec la corvée répétée N fois
    choresToAssign = Array(numCount).fill(choreToAssign);
    
    console.log(chalk.gray(`📅 Date : ${today}`));
    console.log(chalk.gray(`🎯 Corvée : ${choreToAssign} x${numCount}`));
    console.log('');
    
  }
  // Cas 2: Count sans corvée spécifique (sélection aléatoire)
  else if (count !== null && !specificChore) {
    const numCount = parseInt(count);
    if (isNaN(numCount) || numCount < 1) {
      console.log(chalk.red('\n❌ Le nombre de corvées doit être un nombre positif.\n'));
      return;
    }
    if (numCount > config.chores.length) {
      console.log(chalk.yellow(`\n⚠️  Vous avez demandé ${numCount} corvées mais il n'y en a que ${config.chores.length} disponibles.`));
      console.log(chalk.gray(`Toutes les ${config.chores.length} corvées seront attribuées.\n`));
    } else {
      // Sélectionner aléatoirement les corvées
      const shuffled = [...config.chores].sort(() => Math.random() - 0.5);
      choresToAssign = shuffled.slice(0, numCount);
    }
    
    if (choresToAssign.length === 0) {
      choresToAssign = config.chores;
    }
    
    console.log(chalk.gray(`📅 Date : ${today}`));
    console.log(chalk.gray(`🎯 Nombre de corvées : ${choresToAssign.length}/${config.chores.length}`));
    console.log('');
  }
  // Cas 3: Toutes les corvées (défaut)
  else {
    choresToAssign = config.chores;
    console.log(chalk.gray(`📅 Date : ${today}`));
    console.log(chalk.gray(`🎯 Toutes les corvées (${choresToAssign.length})`));
    console.log('');
  }
  
  const todayAssignments = [];
  const users = Object.keys(history);
  const nonSafeUsers = users.filter(user => !safeSet.has(user));
  if (nonSafeUsers.length > 0) {
    const total = nonSafeUsers.reduce((sum, user) => sum + history[user], 0);
    const avg = Math.round(total / nonSafeUsers.length);
    safe.forEach(user => {
      history[user] = avg;
    });
  }
  const eligibleUsers = users.filter(user => !safeSet.has(user));

  if (eligibleUsers.length === 0) {
    console.log(chalk.red('\n❌ Aucun utilisateur disponible : tout le monde est "à l\'abri".\n'));
    return;
  }
  
  function showSafeArt(user) {
    console.log(chalk.cyan('   .-""""-.\n  /  _  _  \\\n |  (o)(o)  |\n |   .__.   |\n  \\  ----  /\n   `-.__.-`'));
    console.log(chalk.cyan(`🛡️ ${user} est à l'abri. Tour annulé, on relance.`));
  }

  function selectUserForRun(runHistory, runImmune, runForcedQueue, ignoreSafe) {
    if (runForcedQueue.length > 0) {
      const forcedIndex = runForcedQueue.findIndex(user => !safeSet.has(user));
      if (forcedIndex !== -1) {
        const [forcedUser] = runForcedQueue.splice(forcedIndex, 1);
        return { selectedUser: forcedUser, restartAll: false };
      }
      if (!ignoreSafe && runForcedQueue.length > 0 && safeSet.has(runForcedQueue[0])) {
        return { selectedUser: runForcedQueue[0], restartAll: true, safeHit: true };
      }
    }

    const excludeSafe = ignoreSafe ? safe : [];
    const candidateAll = selectUserForChore(runHistory, { exclude: excludeSafe });
    if (!candidateAll) {
      return { selectedUser: null, restartAll: false };
    }

    if (!ignoreSafe && safeSet.has(candidateAll)) {
      return { selectedUser: candidateAll, restartAll: true, safeHit: true };
    }

    if (runImmune.includes(candidateAll)) {
      const excludeList = [...new Set([...runImmune, ...safe])];
      const alternative = selectUserForChore(runHistory, { exclude: excludeList });
      if (alternative) {
        const immuneIndex = runImmune.indexOf(candidateAll);
        if (immuneIndex !== -1) {
          runImmune.splice(immuneIndex, 1);
        }
        if (!runForcedQueue.includes(candidateAll)) {
          runForcedQueue.push(candidateAll);
        }
        console.log(chalk.gray(`🛡️ Totem actif : ${candidateAll} reporté au prochain tour.`));
        return { selectedUser: alternative, restartAll: false };
      }
    }

    return { selectedUser: candidateAll, restartAll: false };
  }

  let ignoreSafe = false;
  let attempts = 0;
  const maxAttempts = 5;

  while (attempts < maxAttempts) {
    attempts += 1;
    const runHistory = { ...history };
    const runAssignments = [];
    const runImmune = [...immune];
    const runForcedQueue = [...forcedQueue];
    let restartAll = false;

    for (const chore of choresToAssign) {
      const result = selectUserForRun(runHistory, runImmune, runForcedQueue, ignoreSafe);
      if (result.restartAll) {
        if (result.safeHit && result.selectedUser) {
          await spinWheel(users, result.selectedUser, chore);
          showSafeArt(result.selectedUser);
        }
        restartAll = true;
        ignoreSafe = true;
        break;
      }

      const selectedUser = result.selectedUser;
      if (!selectedUser) {
        console.log(chalk.red('\n❌ Impossible de sélectionner un utilisateur non protégé.\n'));
        return;
      }

      runHistory[selectedUser]++;
      runAssignments.push({
        date: today,
        chore: chore,
        user: selectedUser,
        completed: false
      });
    }

    if (restartAll) {
      continue;
    }

    for (const assignment of runAssignments) {
      await spinWheel(users, assignment.user, assignment.chore);
      todayAssignments.push(assignment);
      assignments.push(assignment);
    }

    Object.assign(history, runHistory);
    immune = runImmune;
    forcedQueue = runForcedQueue;
    break;
  }

  if (attempts >= maxAttempts) {
    console.log(chalk.red('\n❌ Trop de relances dues aux utilisateurs "à l\'abri".\n'));
    return;
  }
  
  // Sauvegarder les données
  saveJSON(HISTORY_PATH, history);
  saveJSON(ASSIGNMENTS_PATH, assignments);
  saveJSON(TOTEM_PATH, { immune, forcedQueue, safe });
  
  // Message final spectaculaire
  console.log('');
  console.log(gradient.rainbow('═'.repeat(50)));
  console.log(gradient.pastel.multiline('✨ Répartition terminée avec succès ! ✨'));
  console.log(gradient.rainbow('═'.repeat(50)));
  console.log('');
}

module.exports = {
  assignChores
};
