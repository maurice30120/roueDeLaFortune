from typing import Dict, List


def _dedupe(users: List[str]) -> List[str]:
    seen = set()
    result = []
    for user in users:
        if user in seen:
            continue
        result.append(user)
        seen.add(user)
    return result


def normalize_totem(totem: Dict, users: List[str]) -> Dict[str, List[str]]:
    safe_totem = {
        "immune": list(totem.get("immune", [])) if isinstance(totem, dict) else [],
        "forcedQueue": list(totem.get("forcedQueue", [])) if isinstance(totem, dict) else [],
        "safe": list(totem.get("safe", [])) if isinstance(totem, dict) else [],
    }

    user_set = set(users)

    immune = _dedupe([user for user in safe_totem["immune"] if user in user_set])
    forced_queue = _dedupe([user for user in safe_totem["forcedQueue"] if user in user_set])
    safe = _dedupe([user for user in safe_totem["safe"] if user in user_set])

    forced_set = set(forced_queue)
    immune_filtered = [user for user in immune if user not in forced_set]
    safe_set = set(safe)
    immune_final = [user for user in immune_filtered if user not in safe_set]

    return {
        "immune": immune_final,
        "forcedQueue": forced_queue,
        "safe": safe,
    }
