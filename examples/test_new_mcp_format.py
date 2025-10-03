#!/usr/bin/env python3
"""
Test nowego formatu MCP - jeden główny tool 'cyberhunt' z podnarzędziami
"""

import sys
import os
import json

# Dodaj ścieżkę do src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_wrapper import MCPToolHandler


def test_new_mcp_format():
    """Testuje nowy format MCP z jednym głównym narzędziem"""
    print("🔍 Testowanie nowego formatu MCP...")
    
    handler = MCPToolHandler()
    
    # Testy dla każdego narzędzia OSINT
    tests = [
        {
            "tool": "cyberhunt",
            "arguments": {
                "tool": "sherlock",
                "parameters": {"usernames": ["testuser"]}
            },
            "description": "Sherlock - wyszukiwanie użytkownika"
        },
        {
            "tool": "cyberhunt",
            "arguments": {
                "tool": "holehe",
                "parameters": {"email": "test@example.com"}
            },
            "description": "Holehe - sprawdzanie e-maila"
        },
        {
            "tool": "cyberhunt",
            "arguments": {
                "tool": "hunter_domain",
                "parameters": {"domain": "github.com"}
            },
            "description": "Hunter.io - wyszukiwanie domeny"
        },
        {
            "tool": "cyberhunt",
            "arguments": {
                "tool": "hunter_verifier",
                "parameters": {"email": "test@example.com"}
            },
            "description": "Hunter.io - weryfikacja e-maila"
        },
        {
            "tool": "cyberhunt",
            "arguments": {
                "tool": "hunter_finder",
                "parameters": {
                    "full_name": "John Doe",
                    "domain": "github.com"
                }
            },
            "description": "Hunter.io - znajdowanie e-maila"
        },
        {
            "tool": "cyberhunt",
            "arguments": {
                "tool": "reconng",
                "parameters": {"commands": ["workspaces list"]}
            },
            "description": "Recon-ng - listowanie workspace"
        }
    ]
    
    for test in tests:
        print(f"\n   {test['description']}:")
        result = handler.handle_tool_call(test["tool"], test["arguments"])
        status = "✅" if result.get('ok') else "❌"
        print(f"   Status: {status}")
        if not result.get('ok'):
            print(f"   Błąd: {result.get('error', 'Nieznany błąd')}")
        else:
            # Pokaż fragment wyniku
            if 'stdout' in result:
                output = result['stdout'][:100] + "..." if len(result['stdout']) > 100 else result['stdout']
                print(f"   Wynik: {output}")
            elif 'data' in result:
                print(f"   Dane: {str(result['data'])[:100]}...")


def test_backward_compatibility():
    """Testuje kompatybilność wsteczną ze starym formatem"""
    print("\n🔄 Testowanie kompatybilności wstecznej...")
    
    handler = MCPToolHandler()
    
    # Test starych nazw narzędzi
    old_tests = [
        {
            "tool": "sherlock_search",
            "arguments": {"usernames": ["testuser"]},
            "description": "Stary format - Sherlock"
        },
        {
            "tool": "holehe_check",
            "arguments": {"email": "test@example.com"},
            "description": "Stary format - Holehe"
        }
    ]
    
    for test in old_tests:
        print(f"\n   {test['description']}:")
        result = handler.handle_tool_call(test["tool"], test["arguments"])
        status = "✅" if result.get('ok') else "❌"
        print(f"   Status: {status}")


def test_error_handling():
    """Testuje obsługę błędów"""
    print("\n⚠️  Testowanie obsługi błędów...")
    
    handler = MCPToolHandler()
    
    error_tests = [
        {
            "tool": "cyberhunt",
            "arguments": {
                "tool": "unknown_tool",
                "parameters": {}
            },
            "description": "Nieznane narzędzie OSINT"
        },
        {
            "tool": "cyberhunt",
            "arguments": {
                "tool": "sherlock",
                "parameters": {"usernames": []}  # Pusta lista
            },
            "description": "Pusta lista użytkowników"
        },
        {
            "tool": "unknown_tool",
            "arguments": {},
            "description": "Nieznane główne narzędzie"
        }
    ]
    
    for test in error_tests:
        print(f"\n   {test['description']}:")
        result = handler.handle_tool_call(test["tool"], test["arguments"])
        status = "✅" if not result.get('ok') else "❌"  # Oczekujemy błędu
        print(f"   Status: {status}")
        if result.get('error'):
            print(f"   Błąd: {result['error']}")


if __name__ == "__main__":
    print("🚀 CyberHunt MCP - Test nowego formatu")
    print("=" * 50)
    
    try:
        test_new_mcp_format()
        test_backward_compatibility()
        test_error_handling()
        print("\n✅ Wszystkie testy zakończone!")
    except Exception as e:
        print(f"\n❌ Błąd podczas testowania: {e}")
        sys.exit(1)
