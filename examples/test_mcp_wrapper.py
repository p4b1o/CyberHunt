#!/usr/bin/env python3
"""
Przykład użycia CyberHunt MCP Wrapper
"""

import sys
import os
import json

# Dodaj ścieżkę do src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_wrapper import CyberHuntMCPClient, MCPToolHandler


def test_mcp_client():
    """Testuje MCP Client"""
    print("🔍 Testowanie CyberHunt MCP Client...")
    
    client = CyberHuntMCPClient()
    
    # Test Sherlock
    print("\n1. Test Sherlock:")
    result = client.sherlock_search(["testuser"])
    print(f"   Status: {'✅' if result.get('ok') else '❌'}")
    if result.get('ok'):
        print(f"   Znaleziono {len([line for line in result.get('stdout', '').split('\\n') if '[+]' in line])} platform")
    
    # Test Holehe
    print("\n2. Test Holehe:")
    result = client.holehe_check("test@example.com")
    print(f"   Status: {'✅' if result.get('ok') else '❌'}")
    if result.get('ok'):
        print(f"   Wynik: {result.get('stdout', '')[:100]}...")
    
    # Test Hunter.io
    print("\n3. Test Hunter.io Domain Search:")
    result = client.hunter_domain_search("example.com")
    print(f"   Status: {'✅' if result.get('ok') else '❌'}")
    if result.get('ok'):
        data = result.get('data', {}).get('data', {})
        print(f"   Domena: {data.get('domain', 'N/A')}")
        print(f"   Organizacja: {data.get('organization', 'N/A')}")
    
    # Test Recon-ng
    print("\n4. Test Recon-ng:")
    result = client.reconng_execute(["workspaces list"])
    print(f"   Status: {'✅' if result.get('ok') else '❌'}")
    if result.get('ok'):
        print(f"   Wynik: {result.get('stdout', '')[:100]}...")


def test_mcp_handler():
    """Testuje MCP Tool Handler"""
    print("\n🛠️  Testowanie MCP Tool Handler...")
    
    handler = MCPToolHandler()
    
    # Test różnych narzędzi
    tests = [
        {
            "tool": "sherlock_search",
            "args": {"usernames": ["janedoe"]},
            "description": "Sherlock - wyszukiwanie użytkownika"
        },
        {
            "tool": "holehe_check", 
            "args": {"email": "jane@example.com"},
            "description": "Holehe - sprawdzanie e-maila"
        },
        {
            "tool": "hunter_domain_search",
            "args": {"domain": "github.com"},
            "description": "Hunter.io - wyszukiwanie domeny"
        },
        {
            "tool": "reconng_execute",
            "args": {"commands": ["workspaces list"]},
            "description": "Recon-ng - listowanie workspace"
        }
    ]
    
    for test in tests:
        print(f"\n   {test['description']}:")
        result = handler.handle_tool_call(test["tool"], test["args"])
        status = "✅" if result.get('ok') else "❌"
        print(f"   Status: {status}")
        if not result.get('ok'):
            print(f"   Błąd: {result.get('error', 'Nieznany błąd')}")


if __name__ == "__main__":
    print("🚀 CyberHunt MCP Wrapper - Test")
    print("=" * 50)
    
    try:
        test_mcp_client()
        test_mcp_handler()
        print("\n✅ Wszystkie testy zakończone!")
    except Exception as e:
        print(f"\n❌ Błąd podczas testowania: {e}")
        sys.exit(1)
