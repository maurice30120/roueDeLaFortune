// Obtenir la date du jour au format YYYY-MM-DD
function getTodayDate() {
  const today = new Date();
  return today.toISOString().split('T')[0];
}

module.exports = {
  getTodayDate
};
