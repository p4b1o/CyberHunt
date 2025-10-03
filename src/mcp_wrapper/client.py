import json
import sys
import asyncio
import requests
from typing import List, Optional, Dict, Any
import os


class CyberHuntMCPClient:
    """MCP Client dla CyberHunt OSINT Tools"""
    
    def __init__(self, base_url: str = None) -> None:
        self.base_url = (base_url or os.getenv("CYBERHUNT_API_URL", "http://localhost:8000")).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _make_request(self, endpoint: str, data: Dict[str, Any], timeout: int = 60) -> Dict[str, Any]:
        """Wykonuje zapytanie HTTP do API"""
        try:
            response = self.session.post(f"{self.base_url}{endpoint}", json=data, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"ok": False, "error": str(e)}

    def sherlock_search(self, usernames: List[str]) -> Dict[str, Any]:
        """Wyszukuje nazwy użytkowników na platformach społecznościowych"""
        return self._make_request("/tools/sherlock", {"usernames": usernames}, timeout=120)

    def holehe_check(self, email: str) -> Dict[str, Any]:
        """Sprawdza czy e-mail jest zarejestrowany na serwisach"""
        return self._make_request("/tools/holehe", {"emails": [email]}, timeout=60)

    def hunter_domain_search(self, domain: str) -> Dict[str, Any]:
        """Wyszukuje e-maile i informacje o domenie"""
        return self._make_request("/tools/hunter/domain-search", {"domain": domain}, timeout=60)

    def hunter_email_verifier(self, email: str) -> Dict[str, Any]:
        """Weryfikuje poprawność i istnienie adresu e-mail"""
        return self._make_request("/tools/hunter/email-verifier", {"email": email}, timeout=60)

    def hunter_email_finder(self, full_name: str, domain: str) -> Dict[str, Any]:
        """Znajduje prawdopodobne adresy e-mail na podstawie imienia i domeny"""
        return self._make_request("/tools/hunter/email-finder", {
            "full_name": full_name, 
            "domain": domain
        }, timeout=60)

    def reconng_execute(self, commands: List[str]) -> Dict[str, Any]:
        """Wykonuje polecenia Recon-ng framework"""
        return self._make_request("/tools/reconng", {"commands": commands}, timeout=120)


class MCPToolHandler:
    """Handler dla narzędzi MCP"""
    
    def __init__(self):
        self.client = CyberHuntMCPClient()

    def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Obsługuje wywołania narzędzi MCP"""
        try:
            if tool_name == "cyberhunt":
                # Nowy format - jeden główny tool z podnarzędziami
                osint_tool = arguments.get("tool")
                parameters = arguments.get("parameters", {})
                
                if osint_tool == "sherlock":
                    usernames = parameters.get("usernames", [])
                    if not usernames:
                        return {"ok": False, "error": "sherlock wymaga parametru 'usernames' (lista)"}
                    return self.client.sherlock_search(usernames)
                
                elif osint_tool == "holehe":
                    email = parameters.get("email", "")
                    if not email:
                        return {"ok": False, "error": "holehe wymaga parametru 'email'"}
                    return self.client.holehe_check(email)
                
                elif osint_tool == "hunter_domain":
                    domain = parameters.get("domain", "")
                    if not domain:
                        return {"ok": False, "error": "hunter_domain wymaga parametru 'domain'"}
                    return self.client.hunter_domain_search(domain)
                
                elif osint_tool == "hunter_verifier":
                    email = parameters.get("email", "")
                    if not email:
                        return {"ok": False, "error": "hunter_verifier wymaga parametru 'email'"}
                    return self.client.hunter_email_verifier(email)
                
                elif osint_tool == "hunter_finder":
                    full_name = parameters.get("full_name", "")
                    domain = parameters.get("domain", "")
                    if not full_name or not domain:
                        return {"ok": False, "error": "hunter_finder wymaga parametrów 'full_name' i 'domain'"}
                    return self.client.hunter_email_finder(full_name, domain)
                
                elif osint_tool == "reconng":
                    commands = parameters.get("commands", [])
                    if not commands:
                        return {"ok": False, "error": "reconng wymaga parametru 'commands' (lista)"}
                    return self.client.reconng_execute(commands)
                
                else:
                    return {"ok": False, "error": f"Nieznane narzędzie OSINT: {osint_tool}"}
            
            # Zachowanie kompatybilności wstecznej
            elif tool_name == "sherlock_search":
                return self.client.sherlock_search(arguments["usernames"])
            
            elif tool_name == "holehe_check":
                return self.client.holehe_check(arguments["email"])
            
            elif tool_name == "hunter_domain_search":
                return self.client.hunter_domain_search(arguments["domain"])
            
            elif tool_name == "hunter_email_verifier":
                return self.client.hunter_email_verifier(arguments["email"])
            
            elif tool_name == "hunter_email_finder":
                return self.client.hunter_email_finder(
                    arguments["full_name"], 
                    arguments["domain"]
                )
            
            elif tool_name == "reconng_execute":
                return self.client.reconng_execute(arguments["commands"])
            
            else:
                return {"ok": False, "error": f"Nieznane narzędzie: {tool_name}"}
                
        except Exception as e:
            return {"ok": False, "error": str(e)}


def main():
    """Główna funkcja dla MCP server"""
    handler = MCPToolHandler()
    
    # Przykład użycia - można rozszerzyć o pełny protokół MCP
    if len(sys.argv) > 1:
        tool_name = sys.argv[1]
        arguments = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        result = handler.handle_tool_call(tool_name, arguments)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("CyberHunt MCP Client - użyj: python -m src.mcp_wrapper.client <tool_name> <arguments_json>")


if __name__ == "__main__":
    main()
