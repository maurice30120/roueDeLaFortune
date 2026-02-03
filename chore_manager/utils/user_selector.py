import random
from typing import Dict, List, Optional


def select_user_for_chore(history: Dict[str, int], exclude: Optional[List[str]] = None) -> Optional[str]:
    exclude_set = set(exclude or [])
    users = [user for user in history.keys() if user not in exclude_set]

    if not users:
        return None

    min_tasks = min(history[user] for user in users)
    candidates = [user for user in users if history[user] == min_tasks]

    if not candidates:
        return None

    return random.choice(candidates)
