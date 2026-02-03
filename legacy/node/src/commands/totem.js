const chalk = require('chalk');
const { loadJSON, saveJSON, CONFIG_PATH, TOTEM_PATH } = require('../utils/fileManager');
const { normalizeTotem } = require('../utils/totemManager');

function loadNormalizedTotem() {
  const config = loadJSON(CONFIG_PATH);
  const totemRaw = loadJSON(TOTEM_PATH);
  const normalized = normalizeTotem(totemRaw, config.users);
  return { config, totem: normalized };
}

function showTotemStatus() {
  const { totem } = loadNormalizedTotem();

  console.log(chalk.bold.cyan('\n🛡️ Totem d\'immunité\n'));

  if (totem.immune.length === 0) {
    console.log(chalk.gray('Aucun utilisateur immunisé.'));
  } else {
    console.log(chalk.bold('Immunisés:'));
    totem.immune.forEach(user => console.log(chalk.yellow(`  • ${user}`)));
  }

  if (totem.safe.length === 0) {
    console.log(chalk.gray('\nAucun utilisateur à l\'abri.'));
  } else {
    console.log(chalk.bold('\nÀ l\'abri:'));
    totem.safe.forEach(user => console.log(chalk.cyan(`  • ${user}`)));
  }

  if (totem.forcedQueue.length === 0) {
    console.log(chalk.gray('\nAucune sélection forcée en attente.'));
  } else {
    console.log(chalk.bold('\nFile forcée (prochains tours):'));
    totem.forcedQueue.forEach(user => console.log(chalk.cyan(`  • ${user}`)));
  }

  console.log('');
}

function addTotemUser(userName) {
  if (!userName) {
    console.log(chalk.red('\n❌ Spécifiez un utilisateur.\n'));
    return;
  }

  const { config, totem } = loadNormalizedTotem();
  if (!config.users.includes(userName)) {
    console.log(chalk.red(`\n❌ Utilisateur "${userName}" introuvable.\n`));
    return;
  }

  if (totem.immune.includes(userName)) {
    console.log(chalk.yellow(`\n⚠️  "${userName}" est déjà immunisé.\n`));
    return;
  }

  totem.immune.push(userName);
  saveJSON(TOTEM_PATH, totem);
  console.log(chalk.green(`\n✓ Totem attribué à "${userName}".\n`));
}

function addSafeUser(userName) {
  if (!userName) {
    console.log(chalk.red('\n❌ Spécifiez un utilisateur.\n'));
    return;
  }

  const { config, totem } = loadNormalizedTotem();
  if (!config.users.includes(userName)) {
    console.log(chalk.red(`\n❌ Utilisateur "${userName}" introuvable.\n`));
    return;
  }

  if (totem.safe.includes(userName)) {
    console.log(chalk.yellow(`\n⚠️  "${userName}" est déjà à l'abri.\n`));
    return;
  }

  totem.safe.push(userName);
  saveJSON(TOTEM_PATH, totem);
  console.log(chalk.green(`\n✓ "${userName}" est désormais à l'abri.\n`));
}

function removeTotemUser(userName) {
  if (!userName) {
    console.log(chalk.red('\n❌ Spécifiez un utilisateur.\n'));
    return;
  }

  const { totem } = loadNormalizedTotem();
  const beforeImmune = totem.immune.length;
  const beforeForced = totem.forcedQueue.length;
  const beforeSafe = totem.safe.length;

  totem.immune = totem.immune.filter(user => user !== userName);
  totem.forcedQueue = totem.forcedQueue.filter(user => user !== userName);
  totem.safe = totem.safe.filter(user => user !== userName);

  if (totem.immune.length === beforeImmune && totem.forcedQueue.length === beforeForced && totem.safe.length === beforeSafe) {
    console.log(chalk.yellow(`\n⚠️  "${userName}" n'était pas dans le totem.\n`));
    return;
  }

  saveJSON(TOTEM_PATH, totem);
  console.log(chalk.green(`\n✓ Totem retiré pour "${userName}".\n`));
}

function clearTotem() {
  saveJSON(TOTEM_PATH, { immune: [], forcedQueue: [], safe: [] });
  console.log(chalk.green('\n✓ Totem réinitialisé.\n'));
}

function removeSafeUser(userName) {
  if (!userName) {
    console.log(chalk.red('\n❌ Spécifiez un utilisateur.\n'));
    return;
  }

  const { totem } = loadNormalizedTotem();
  const beforeSafe = totem.safe.length;

  totem.safe = totem.safe.filter(user => user !== userName);

  if (totem.safe.length === beforeSafe) {
    console.log(chalk.yellow(`\n⚠️  "${userName}" n'était pas à l'abri.\n`));
    return;
  }

  saveJSON(TOTEM_PATH, totem);
  console.log(chalk.green(`\n✓ "${userName}" n'est plus à l'abri.\n`));
}

function clearSafe() {
  const { totem } = loadNormalizedTotem();
  if (totem.safe.length === 0) {
    console.log(chalk.yellow('\n⚠️  Aucun utilisateur à l\'abri.\n'));
    return;
  }
  totem.safe = [];
  saveJSON(TOTEM_PATH, totem);
  console.log(chalk.green('\n✓ Liste "à l\'abri" réinitialisée.\n'));
}

module.exports = {
  showTotemStatus,
  addTotemUser,
  removeTotemUser,
  clearTotem,
  addSafeUser,
  removeSafeUser,
  clearSafe
};
