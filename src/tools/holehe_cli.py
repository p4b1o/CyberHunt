import subprocess
from typing import List


def run_holehe(emails: List[str]) -> dict:
    command = ["holehe", *emails, "--only-used"]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, check=False)
        return {
            "ok": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


