import os
import requests
from typing import Optional


HUNTER_BASE = "https://api.hunter.io/v2"


def hunter_domain_search(domain: str, api_key: Optional[str] = None) -> dict:
    key = api_key or os.getenv("HUNTER_API_KEY")
    if not key:
        return {"ok": False, "error": "Missing HUNTER_API_KEY"}
    url = f"{HUNTER_BASE}/domain-search"
    params = {"domain": domain, "api_key": key}
    try:
        resp = requests.get(url, params=params, timeout=20)
        return {"ok": resp.ok, "status": resp.status_code, "data": resp.json()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def hunter_email_finder(full_name: str, domain: str, api_key: Optional[str] = None) -> dict:
    key = api_key or os.getenv("HUNTER_API_KEY")
    if not key:
        return {"ok": False, "error": "Missing HUNTER_API_KEY"}
    url = f"{HUNTER_BASE}/email-finder"
    params = {"full_name": full_name, "domain": domain, "api_key": key}
    try:
        resp = requests.get(url, params=params, timeout=20)
        return {"ok": resp.ok, "status": resp.status_code, "data": resp.json()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def hunter_email_verifier(email: str, api_key: Optional[str] = None) -> dict:
    key = api_key or os.getenv("HUNTER_API_KEY")
    if not key:
        return {"ok": False, "error": "Missing HUNTER_API_KEY"}
    url = f"{HUNTER_BASE}/email-verifier"
    params = {"email": email, "api_key": key}
    try:
        resp = requests.get(url, params=params, timeout=20)
        return {"ok": resp.ok, "status": resp.status_code, "data": resp.json()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


