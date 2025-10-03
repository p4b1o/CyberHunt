import requests
from typing import List, Optional


class CyberHuntClient:
    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self.base_url = base_url.rstrip("/")

    def sherlock(self, usernames: List[str]) -> dict:
        return requests.post(f"{self.base_url}/tools/sherlock", json={"usernames": usernames}, timeout=60).json()

    def holehe(self, emails: List[str]) -> dict:
        return requests.post(f"{self.base_url}/tools/holehe", json={"emails": emails}, timeout=60).json()

    def hunter_domain(self, domain: str, api_key: Optional[str] = None) -> dict:
        return requests.post(f"{self.base_url}/tools/hunter/domain-search", json={"domain": domain, "api_key": api_key}, timeout=60).json()

    def hunter_finder(self, full_name: str, domain: str, api_key: Optional[str] = None) -> dict:
        payload = {"full_name": full_name, "domain": domain, "api_key": api_key}
        return requests.post(f"{self.base_url}/tools/hunter/email-finder", json=payload, timeout=60).json()

    def hunter_verify(self, email: str, api_key: Optional[str] = None) -> dict:
        payload = {"email": email, "api_key": api_key}
        return requests.post(f"{self.base_url}/tools/hunter/email-verifier", json=payload, timeout=60).json()

    def reconng(self, commands: List[str]) -> dict:
        return requests.post(f"{self.base_url}/tools/reconng", json={"commands": commands}, timeout=120).json()


