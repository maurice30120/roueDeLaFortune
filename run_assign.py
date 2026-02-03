#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def _ensure_repo_on_syspath() -> None:
    # Allow running from notebooks/ (or elsewhere) without installing the package.
    repo_root = Path.cwd().resolve()
    if not (repo_root / "chore_manager").exists():
        repo_root = repo_root.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def main(argv: list[str] | None = None) -> int:
    _ensure_repo_on_syspath()

    parser = argparse.ArgumentParser(description="Run assign with animation (notebook-friendly).")
    parser.add_argument("chore", nargs="?", default="talomi", help="Chore name (default: talomi)")
    parser.add_argument("--count", type=int, default=3, help="How many times to assign (default: 3)")
    parser.add_argument("--force", "-f", action="store_true", help="Force even if already assigned today")
    parser.add_argument("--no-anim", action="store_true", help="Disable animation")
    parser.add_argument("--anim", action="store_true", help="Force animation (even without TTY)")

    ns = parser.parse_args(argv)

    if ns.anim and not ns.no_anim:
        os.environ["RDLF_FORCE_ANIM"] = "1"

    from chore_manager import assign_chores  # noqa: E402

    assign_chores(
        auto_mode=True,
        count=ns.count,
        specific_chore=ns.chore,
        force_mode=ns.force,
        animate=None,  # let should_animate decide; RDLF_FORCE_ANIM can force it
        no_anim=ns.no_anim,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

