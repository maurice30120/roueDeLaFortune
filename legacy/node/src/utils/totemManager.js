function normalizeTotem(totem, users) {
  const safeTotem = {
    immune: Array.isArray(totem?.immune) ? totem.immune : [],
    forcedQueue: Array.isArray(totem?.forcedQueue) ? totem.forcedQueue : [],
    safe: Array.isArray(totem?.safe) ? totem.safe : []
  };

  const userSet = new Set(users);
  const immune = [];
  const seenImmune = new Set();
  for (const user of safeTotem.immune) {
    if (!userSet.has(user) || seenImmune.has(user)) {
      continue;
    }
    immune.push(user);
    seenImmune.add(user);
  }

  const forcedQueue = [];
  const seenForced = new Set();
  for (const user of safeTotem.forcedQueue) {
    if (!userSet.has(user) || seenForced.has(user)) {
      continue;
    }
    forcedQueue.push(user);
    seenForced.add(user);
  }

  const safe = [];
  const seenSafe = new Set();
  for (const user of safeTotem.safe) {
    if (!userSet.has(user) || seenSafe.has(user)) {
      continue;
    }
    safe.push(user);
    seenSafe.add(user);
  }

  const forcedSet = new Set(forcedQueue);
  const immuneFiltered = immune.filter(user => !forcedSet.has(user));
  const safeSet = new Set(safe);
  const immuneFinal = immuneFiltered.filter(user => !safeSet.has(user));

  return {
    immune: immuneFinal,
    forcedQueue,
    safe
  };
}

module.exports = {
  normalizeTotem
};
