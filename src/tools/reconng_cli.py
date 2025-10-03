import json
import os
import subprocess


def seed_reconng_api_keys(keys_json: str | None = None) -> None:
    raw = keys_json or os.getenv("RECONNG_API_KEYS", "{}")
    try:
        data = json.loads(raw) if raw else {}
    except Exception:
        data = {}
    # Recon-ng posiada własny magazyn kluczy (keys add <name> <value>)
    for name, value in data.items():
        try:
            subprocess.run(["recon-ng", "--no-check", "-r", "-"], input=f"keys add {name} {value}\nexit\n", text=True, capture_output=True)
        except Exception:
            pass


def run_reconng(script_commands: list[str]) -> dict:
    # Pozwala uruchamiać zestaw poleceń recon-ng batchowo (workspace, modules, options, run)
    script = "\n".join(script_commands + ["exit"]) + "\n"
    try:
        proc = subprocess.run(["recon-ng", "--no-check", "-r", "-"], input=script, text=True, capture_output=True)
        return {
            "ok": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


