const chalk = require('chalk');
const gradient = require('gradient-string');

// Animation de la roue de la fortune
async function spinWheel(users, selectedUser, chore) {
  const frames = ['🎰', '🎲', '🎯', '🎪', '🎨', '🎭', '🎬', '🎪'];
  const spinDuration = 2000; // 2 secondes
  const frameDelay = 80;
  const iterations = Math.floor(spinDuration / frameDelay);
  
  // Effacer la ligne pour l'animation
  process.stdout.write('\n');
  
  for (let i = 0; i < iterations; i++) {
    const randomUser = users[Math.floor(Math.random() * users.length)];
    const frame = frames[i % frames.length];
    const progress = i / iterations;
    
    // Créer l'effet de ralentissement
    const isSlowingDown = progress > 0.7;
    
    // Texte avec gradient
    let displayText;
    if (progress < 0.3) {
      displayText = gradient.rainbow(`${frame} ${chore.padEnd(15)} → ${randomUser}...`);
    } else if (progress < 0.7) {
      displayText = gradient.cristal(`${frame} ${chore.padEnd(15)} → ${randomUser}...`);
    } else {
      displayText = gradient.pastel(`${frame} ${chore.padEnd(15)} → ${randomUser}...`);
    }
    
    // Afficher
    process.stdout.write('\r' + displayText);
    
    // Attendre
    const delay = isSlowingDown ? frameDelay * (1 + progress * 2) : frameDelay;
    await new Promise(resolve => setTimeout(resolve, delay));
  }
  
  // Animation finale - révélation
  process.stdout.write('\r' + ' '.repeat(80) + '\r');
  
  // Effet de flash
  for (let i = 0; i < 3; i++) {
    if (i % 2 === 0) {
      process.stdout.write('\r' + gradient.rainbow(`✨ ${chore.padEnd(15)} → ${selectedUser} ✨`));
    } else {
      process.stdout.write('\r' + chalk.bold.yellow(`✨ ${chore.padEnd(15)} → ${selectedUser} ✨`));
    }
    await new Promise(resolve => setTimeout(resolve, 150));
  }
  
  // Résultat final avec effet
  process.stdout.write('\r' + ' '.repeat(80) + '\r');
  console.log(chalk.green('✓'), chalk.bold(chore.padEnd(15)), '→', gradient.rainbow.multiline(selectedUser));
  
  // Petite pause pour l'effet
  await new Promise(resolve => setTimeout(resolve, 300));
}

// Animation de titre
function showTitle() {
  console.log('');
  console.log(gradient.rainbow('╔═══════════════════════════════════════════════╗'));
  console.log(gradient.rainbow('║                                               ║'));
  console.log(gradient.rainbow('║        🎰  ROUE DE LA FORTUNE  🎰           ║'));
  console.log(gradient.rainbow('║          Répartition des corvées              ║'));
  console.log(gradient.rainbow('║                                               ║'));
  console.log(gradient.rainbow('╚═══════════════════════════════════════════════╝'));
  console.log('');
}

module.exports = {
  spinWheel,
  showTitle
};
