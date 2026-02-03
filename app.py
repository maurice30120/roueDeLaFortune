#!/usr/bin/env python3

import sys

from chore_manager import (
    add_safe_user,
    add_totem_user,
    assign_chores,
    clear_safe,
    clear_totem,
    complete_chore,
    remove_safe_user,
    remove_totem_user,
    reset,
    show_help,
    show_status,
    show_totem_status,
)


def _get_option_value(args, *flags):
    positions = [(args.index(flag), flag) for flag in flags if flag in args]
    if not positions:
        return None
    idx, _ = min(positions, key=lambda item: item[0])
    if idx + 1 < len(args):
        return args[idx + 1]
    return None


def main() -> None:
    args = sys.argv[1:]
    command = args[0] if args else "help"

    auto_mode_flag = "--auto" in args
    all_mode = "--all" in args
    force_mode = "--force" in args or "-f" in args
    no_anim = "--no-anim" in args

    person_value = _get_option_value(args, "-p", "--person")
    count_value = _get_option_value(args, "--count")

    specific_chore = None
    if command == "assign" and len(args) > 1 and not args[1].startswith("-"):
        specific_chore = args[1]

    auto_mode = True if command == "assign" else auto_mode_flag
    if command == "assign" and count_value is None:
        count_value = 3
    if command == "assign" and specific_chore is None:
        specific_chore = "talomi"

    if command == "assign":
        assign_chores(auto_mode, count_value, specific_chore, force_mode, no_anim=no_anim)
    elif command == "status":
        show_status()
    elif command == "complete":
        chore_arg = args[1] if len(args) > 1 and not args[1].startswith("-") else None
        if not chore_arg:
            chore_arg = "talomi"
        is_default_complete = len(args) == 1
        effective_all = all_mode or is_default_complete
        complete_chore(chore_arg, person_value, effective_all)
    elif command == "reset":
        reset()
    elif command == "totem":
        action = args[1] if len(args) > 1 else None
        user_arg = " ".join(args[2:]).strip()
        if action == "add":
            add_totem_user(user_arg)
        elif action == "remove":
            remove_totem_user(user_arg)
        elif action == "safe":
            safe_action = args[2] if len(args) > 2 else None
            safe_user_arg = " ".join(args[3:]).strip()
            if safe_action == "add":
                add_safe_user(safe_user_arg)
            elif safe_action == "remove":
                remove_safe_user(safe_user_arg)
            elif safe_action == "clear":
                clear_safe()
            else:
                show_totem_status()
        elif action == "clear":
            clear_totem()
        else:
            show_totem_status()
    elif command == "help":
        show_help()
    else:
        show_help()


if __name__ == "__main__":
    main()
