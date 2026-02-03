const fs = require('fs');
const path = require('path');
const chalk = require('chalk');

// Chemins des fichiers
const CONFIG_PATH = path.join(__dirname, '../../config.json');
const HISTORY_PATH = path.join(__dirname, '../../data/history.json');
const ASSIGNMENTS_PATH = path.join(__dirname, '../../data/assignments.json');
const TOTEM_PATH = path.join(__dirname, '../../data/totem.json');

// Charger les données JSON
function loadJSON(filePath) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(chalk.red(`❌ Erreur lors de la lecture de ${filePath}:`), error.message);
    process.exit(1);
  }
}

// Sauvegarder les données JSON
function saveJSON(filePath, data) {
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
  } catch (error) {
    console.error(chalk.red(`❌ Erreur lors de l'écriture de ${filePath}:`), error.message);
    process.exit(1);
  }
}

module.exports = {
  CONFIG_PATH,
  HISTORY_PATH,
  ASSIGNMENTS_PATH,
  TOTEM_PATH,
  loadJSON,
  saveJSON
};
