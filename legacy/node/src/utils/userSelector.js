// Algorithme de sélection équitable d'utilisateur
function selectUserForChore(history, options = {}) {
  const exclude = Array.isArray(options.exclude) ? options.exclude : [];
  const excludeSet = new Set(exclude);
  const users = Object.keys(history).filter(user => !excludeSet.has(user));

  if (users.length === 0) {
    return null;
  }
  
  // Trouver le minimum de tâches effectuées
  const minTasks = Math.min(...users.map(user => history[user]));
  
  // Filtrer les utilisateurs ayant le minimum de tâches
  const candidates = users.filter(user => history[user] === minTasks);

  // Sélection aléatoire parmi les candidats
  if (candidates.length === 0) {
    return null;
  }
  const selectedUser = candidates[Math.floor(Math.random() * candidates.length)];
  
  return selectedUser;
}

module.exports = {
  selectUserForChore
};
