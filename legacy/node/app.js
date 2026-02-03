#!/usr/bin/env node

const { assignChores } = require('./src/commands/assign');
const { showStatus } = require('./src/commands/status');
const { completeChore } = require('./src/commands/complete');
const { reset } = require('./src/commands/reset');
const { showTotemStatus, addTotemUser, removeTotemUser, clearTotem, addSafeUser, removeSafeUser, clearSafe } = require('./src/commands/totem');
const { showHelp } = require('./src/commands/help');

// Parse des arguments
const args = process.argv.slice(2);
const command = args[0] || 'help';
const autoModeFlag = args.includes('--auto');
const allMode = args.includes('--all');
const forceMode = args.includes('--force') || args.includes('-f');
const personIndex = args.findIndex(arg => arg === '-p' || arg === '--person');
const personValue = (personIndex !== -1 && args[personIndex + 1]) ? args[personIndex + 1] : undefined;

// Récupérer le paramètre --count
let countValue = null;
const countIndex = args.indexOf('--count');
if (countIndex !== -1 && args[countIndex + 1]) {
  countValue = args[countIndex + 1];
}

// Pour la commande assign, récupérer le nom de la corvée si fourni
let specificChore = null;
if (command === 'assign' && args[1] && !args[1].startsWith('-')) {
  specificChore = args[1];
}

// Valeurs par défaut pour assign
const autoMode = (command === 'assign') ? true : autoModeFlag;
if (command === 'assign' && countValue === null) {
  countValue = 3;
}
if (command === 'assign' && specificChore === null) {
  specificChore = 'talomi';
}

// Router les commandes
switch (command) {
  case 'assign':
    assignChores(autoMode, countValue, specificChore, forceMode);
    break;
  case 'status':
    showStatus();
    break;
  case 'complete':
    // Filtrer les arguments pour exclure --all
    let choreArg = (args[1] && !args[1].startsWith('-')) ? args[1] : undefined;
    if (!choreArg) {
      choreArg = 'talomi';
    }
    const userArg = personValue;
    const isDefaultComplete = args.length === 1;
    const effectiveAllMode = allMode || isDefaultComplete;
    completeChore(choreArg, userArg, effectiveAllMode);
    break;
  case 'reset':
    reset();
    break;
  case 'totem': {
    const action = args[1];
    const userArg = args.slice(2).join(' ');
    switch (action) {
      case 'add':
        addTotemUser(userArg);
        break;
      case 'remove':
        removeTotemUser(userArg);
        break;
      case 'safe': {
        const safeAction = args[2];
        const safeUserArg = args.slice(3).join(' ');
        switch (safeAction) {
          case 'add':
            addSafeUser(safeUserArg);
            break;
          case 'remove':
            removeSafeUser(safeUserArg);
            break;
          case 'clear':
            clearSafe();
            break;
          case undefined:
          default:
            showTotemStatus();
            break;
        }
        break;
      }
      case 'clear':
        clearTotem();
        break;
      case 'status':
      case undefined:
      default:
        showTotemStatus();
        break;
    }
    break;
  }
  case 'help':
  default:
    showHelp();
    break;
}
