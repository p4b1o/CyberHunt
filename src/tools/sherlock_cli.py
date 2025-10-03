import json
import subprocess
from typing import List


def run_sherlock(usernames: List[str]) -> dict:
    command = [
        "python", "-m", "sherlock",
        *usernames,
        "--print-found",
        "--timeout", "8",
        "--no-color",
        "--csv",
        "--local",
    ]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, check=False)
        return {
            "ok": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


