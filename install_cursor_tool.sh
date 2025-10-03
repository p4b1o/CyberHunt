#!/bin/bash

# CyberHunt Cursor Tool Installer
# Instaluje CyberHunt jako MCP tool w Cursor

set -e

echo "🚀 CyberHunt Cursor Tool Installer"
echo "=================================="

# Sprawdź czy jesteśmy w odpowiednim katalogu
if [ ! -f "cursor_mcp_config.json" ]; then
    echo "❌ Błąd: Uruchom skrypt z katalogu CyberHunt"
    exit 1
fi

# Sprawdź czy virtual environment istnieje
if [ ! -d "venv" ]; then
    echo "📦 Tworzenie virtual environment..."
    python3 -m venv venv
fi

# Aktywuj virtual environment
echo "🔧 Aktywacja virtual environment..."
source venv/bin/activate

# Zainstaluj zależności
echo "📥 Instalacja zależności..."
pip install -r requirements.txt

# Sprawdź czy serwer CyberHunt działa
echo "🔍 Sprawdzanie serwera CyberHunt..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "⚠️  Serwer CyberHunt nie działa. Uruchamianie..."
    docker compose up -d
    echo "⏳ Oczekiwanie na uruchomienie serwera..."
    sleep 10
fi

# Test połączenia
echo "🧪 Testowanie połączenia MCP..."
if python -m src.mcp_wrapper.client cyberhunt '{"tool": "sherlock", "parameters": {"usernames": ["testuser"]}}' > /dev/null 2>&1; then
    echo "✅ Połączenie MCP działa poprawnie"
else
    echo "❌ Błąd połączenia MCP"
    exit 1
fi

echo ""
echo "🎉 Instalacja zakończona pomyślnie!"
echo ""
echo "📋 Następne kroki:"
echo "1. Otwórz Cursor IDE"
echo "2. Przejdź do Settings → Features → Model Context Protocol"
echo "3. Dodaj nowy serwer MCP z konfiguracją z pliku cursor_mcp_config.json"
echo "4. Uruchom ponownie Cursor"
echo ""
echo "📖 Szczegółowe instrukcje: docs/CURSOR_INTEGRATION.md"
echo ""
echo "🔧 Konfiguracja MCP dla Cursor:"
echo "--------------------------------"
cat cursor_mcp_config.json
echo "--------------------------------"
