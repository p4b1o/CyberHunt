# CyberHunt Integration z Cursor

## Przegląd

CyberHunt można zintegrować z Cursor IDE jako MCP (Model Context Protocol) tool, umożliwiając AI w Cursor korzystanie z narzędzi OSINT.

## Instalacja

### 1. Przygotowanie środowiska

Upewnij się, że masz uruchomiony serwer CyberHunt:

```bash
# W katalogu CyberHunt
source venv/bin/activate
docker compose up -d
```

### 2. Konfiguracja Cursor

#### Opcja A: Użycie pliku konfiguracyjnego

1. Skopiuj zawartość `cursor_mcp_config.json` do konfiguracji MCP w Cursor
2. W Cursor: Settings → Features → Model Context Protocol
3. Dodaj nowy serwer MCP z konfiguracją:

```json
{
  "mcpServers": {
    "cyberhunt": {
      "command": "python",
      "args": ["-m", "src.mcp_wrapper.client"],
      "cwd": "/Users/pawelhordynski/cyberguru/CyberHunt",
      "env": {
        "CYBERHUNT_API_URL": "http://localhost:8000",
        "PYTHONPATH": "/Users/pawelhordynski/cyberguru/CyberHunt/src"
      }
    }
  }
}
```

#### Opcja B: Bezpośrednia konfiguracja

Jeśli Cursor nie obsługuje plików konfiguracyjnych, dodaj konfigurację ręcznie w ustawieniach MCP.

### 3. Weryfikacja instalacji

Po skonfigurowaniu, Cursor powinien rozpoznać narzędzie `cyberhunt` z następującymi podnarzędziami:

- `sherlock` - wyszukiwanie użytkowników na platformach
- `holehe` - sprawdzanie e-maili na serwisach  
- `hunter_domain` - wyszukiwanie informacji o domenach
- `hunter_verifier` - weryfikacja e-maili
- `hunter_finder` - znajdowanie e-maili
- `reconng` - wykonywanie poleceń Recon-ng

## Użycie w Cursor

### Przykłady zapytań

Możesz teraz używać CyberHunt bezpośrednio w Cursor:

```
"Sprawdź czy e-mail john@example.com jest zarejestrowany na różnych serwisach"
"Znajdź profile użytkownika 'janedoe' na platformach społecznościowych"
"Przeszukaj domenę github.com pod kątem e-maili"
"Zweryfikuj poprawność adresu test@example.com"
"Znajdź prawdopodobny e-mail dla 'John Doe' w domenie example.com"
"Wykonaj polecenia Recon-ng: workspaces list"
```

### Format zapytań

AI w Cursor będzie automatycznie używać odpowiedniego narzędzia OSINT:

- **Sherlock**: "Wyszukaj użytkownika X" → użyje `sherlock`
- **Holehe**: "Sprawdź e-mail X" → użyje `holehe`  
- **Hunter.io**: "Przeszukaj domenę X" → użyje `hunter_domain`
- **Recon-ng**: "Wykonaj polecenia Recon-ng" → użyje `reconng`

## Rozwiązywanie problemów

### 1. Błąd połączenia
- Sprawdź czy serwer CyberHunt działa: `curl http://localhost:8000/health`
- Upewnij się, że Docker container jest uruchomiony

### 2. Błąd Python path
- Sprawdź czy `PYTHONPATH` jest ustawiony poprawnie
- Upewnij się, że virtual environment jest aktywny

### 3. Błąd MCP
- Sprawdź logi Cursor w Developer Tools
- Upewnij się, że konfiguracja MCP jest poprawna

### 4. Testowanie połączenia

Możesz przetestować połączenie ręcznie:

```bash
cd /Users/pawelhordynski/cyberguru/CyberHunt
source venv/bin/activate
python -m src.mcp_wrapper.client cyberhunt '{"tool": "sherlock", "parameters": {"usernames": ["testuser"]}}'
```

## Zaawansowane użycie

### Własne skrypty

Możesz tworzyć własne skrypty używające CyberHunt:

```python
from src.mcp_wrapper import CyberHuntMCPClient

client = CyberHuntMCPClient()

# Wyszukaj użytkownika
result = client.sherlock_search(["janedoe"])
print(result)

# Sprawdź e-mail
result = client.holehe_check("jane@example.com")
print(result)
```

### Integracja z innymi narzędziami

CyberHunt może być używany w połączeniu z innymi narzędziami OSINT lub analitycznymi w Cursor.

## Bezpieczeństwo

- Klucze API są przechowywane w `.env` (nie w repo)
- Wszystkie zapytania są logowane
- Używaj narzędzi odpowiedzialnie i zgodnie z prawem

## Wsparcie

W przypadku problemów:
1. Sprawdź logi Cursor
2. Sprawdź status serwera CyberHunt
3. Przetestuj narzędzia ręcznie
4. Sprawdź konfigurację MCP
