# CyberHunt MCP Integration

## Przegląd

CyberHunt oferuje integrację z protokołem MCP (Model Context Protocol), umożliwiając AI korzystanie z narzędzi OSINT przez standardowy interfejs. Wszystkie narzędzia OSINT są dostępne przez jeden główny tool `cyberhunt`.

## Konfiguracja

### 1. Virtual Environment

CyberHunt wymaga Python virtual environment:

```bash
# Utwórz virtual environment
python3 -m venv venv

# Aktywuj virtual environment
source venv/bin/activate  # Linux/macOS
# lub
venv\Scripts\activate     # Windows

# Zainstaluj zależności
pip install -r requirements.txt
```

### 2. Plik konfiguracyjny MCP

Utwórz plik `mcp_config.json` w katalogu głównym:

```json
{
  "mcpServers": {
    "cyberhunt": {
      "command": "python",
      "args": ["-m", "src.mcp_wrapper.client"],
      "env": {
        "CYBERHUNT_API_URL": "http://localhost:8000"
      }
    }
  },
  "tools": {
    "cyberhunt": {
      "name": "cyberhunt",
      "description": "CyberHunt OSINT Toolkit - kompleksowe narzędzie do wyszukiwania informacji o ludziach w internecie",
      "inputSchema": {
        "type": "object",
        "properties": {
          "tool": {
            "type": "string",
            "enum": ["sherlock", "holehe", "hunter_domain", "hunter_verifier", "hunter_finder", "reconng"],
            "description": "Narzędzie OSINT do użycia"
          },
          "parameters": {
            "type": "object",
            "description": "Parametry specyficzne dla wybranego narzędzia"
          }
        },
        "required": ["tool", "parameters"]
      }
    }
  }
}
```

### 3. Zmienne środowiskowe

Upewnij się, że serwer CyberHunt działa na `http://localhost:8000` lub ustaw odpowiednią zmienną:

```bash
export CYBERHUNT_API_URL="http://localhost:8000"
```

## Główne narzędzie MCP: cyberhunt

CyberHunt eksponuje jedno główne narzędzie `cyberhunt` z następującymi podnarzędziami:

### Dostępne narzędzia OSINT

#### 1. sherlock
**Opis:** Wyszukuje nazwy użytkowników na platformach społecznościowych i zawodowych

**Parametry:**
- `usernames` (array): Lista nazw użytkowników do wyszukania

**Przykład:**
```json
{
  "tool": "cyberhunt",
  "arguments": {
    "tool": "sherlock",
    "parameters": {
      "usernames": ["janedoe", "johndoe"]
    }
  }
}
```

#### 2. holehe
**Opis:** Sprawdza czy e-mail jest zarejestrowany na różnych serwisach

**Parametry:**
- `email` (string): Adres e-mail do sprawdzenia

**Przykład:**
```json
{
  "tool": "cyberhunt",
  "arguments": {
    "tool": "holehe",
    "parameters": {
      "email": "jane@example.com"
    }
  }
}
```

#### 3. hunter_domain
**Opis:** Wyszukuje e-maile i informacje o domenie

**Parametry:**
- `domain` (string): Domena do przeszukania

**Przykład:**
```json
{
  "tool": "cyberhunt",
  "arguments": {
    "tool": "hunter_domain",
    "parameters": {
      "domain": "example.com"
    }
  }
}
```

#### 4. hunter_verifier
**Opis:** Weryfikuje poprawność i istnienie adresu e-mail

**Parametry:**
- `email` (string): Adres e-mail do weryfikacji

**Przykład:**
```json
{
  "tool": "cyberhunt",
  "arguments": {
    "tool": "hunter_verifier",
    "parameters": {
      "email": "jane@example.com"
    }
  }
}
```

#### 5. hunter_finder
**Opis:** Znajduje prawdopodobne adresy e-mail na podstawie imienia i domeny

**Parametry:**
- `full_name` (string): Pełne imię i nazwisko
- `domain` (string): Domena firmy

**Przykład:**
```json
{
  "tool": "cyberhunt",
  "arguments": {
    "tool": "hunter_finder",
    "parameters": {
      "full_name": "Jane Doe",
      "domain": "example.com"
    }
  }
}
```

#### 6. reconng
**Opis:** Wykonuje polecenia Recon-ng framework

**Parametry:**
- `commands` (array): Lista poleceń Recon-ng do wykonania

**Przykład:**
```json
{
  "tool": "cyberhunt",
  "arguments": {
    "tool": "reconng",
    "parameters": {
      "commands": ["workspaces list", "modules search email"]
    }
  }
}
```

## Użycie programistyczne

### Python Client

```python
from src.mcp_wrapper import CyberHuntMCPClient

# Inicjalizacja klienta
client = CyberHuntMCPClient("http://localhost:8000")

# Wyszukiwanie użytkownika
result = client.sherlock_search(["janedoe"])
print(result)

# Sprawdzanie e-maila
result = client.holehe_check("jane@example.com")
print(result)
```

### MCP Tool Handler

```python
from src.mcp_wrapper import MCPToolHandler

# Inicjalizacja handlera
handler = MCPToolHandler()

# Wywołanie narzędzia
result = handler.handle_tool_call("sherlock_search", {
    "usernames": ["janedoe"]
})
print(result)
```

## Testowanie

Uruchom testy MCP wrapper:

```bash
python examples/test_mcp_wrapper.py
```

## Rozwiązywanie problemów

### 1. Błąd połączenia
- Sprawdź czy serwer CyberHunt działa na `http://localhost:8000`
- Upewnij się, że Docker container jest uruchomiony

### 2. Błąd autoryzacji
- Sprawdź czy klucze API są poprawnie skonfigurowane w `.env`
- Upewnij się, że zmienne środowiskowe są przekazywane do kontenera

### 3. Timeout
- Zwiększ timeout w konfiguracji MCP
- Sprawdź czy narzędzia OSINT odpowiadają w rozumnym czasie

## Rozszerzanie

Aby dodać nowe narzędzie MCP:

1. Dodaj endpoint w `src/mcp/server.py`
2. Dodaj metodę w `CyberHuntMCPClient`
3. Dodaj obsługę w `MCPToolHandler`
4. Zaktualizuj `mcp_config.json`
5. Dodaj testy w `examples/test_mcp_wrapper.py`
