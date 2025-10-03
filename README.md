## CyberHunt (OSINT + MCP)

CyberHunt to modułowe narzędzie OSINT, zaprojektowane do namierzania i korelacji informacji o osobach w internecie. Repozytorium zawiera:
- kontenerowy obraz uruchamiający narzędzia CLI: Sherlock, Holehe, Recon-ng oraz integracje z Hunter.io,
- serwer MCP (Model Context Protocol) do wpinania CyberHunt jako narzędzia AI,
- prosty wrapper MCP po stronie klienta,
- standaryzowane przekazywanie kluczy API przez zmienne środowiskowe.

### Struktura katalogów
```
.
├── src/
│   ├── config/
│   │   └── settings.py
│   ├── mcp/
│   │   └── server.py
│   ├── mcp_wrapper/
│   │   └── client.py
│   └── tools/
│       ├── sherlock_cli.py
│       ├── holehe_cli.py
│       ├── hunter_cli.py
│       └── reconng_cli.py
├── .env.example
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

### Klucze API i konfiguracja
Skopiuj `.env.example` do `.env` i uzupełnij wartości.

Wspierane klucze:
- `HUNTER_API_KEY` — Hunter.io (email finding/verification),
- `RECONNG_API_KEYS` — opcjonalne klucze do modułów Recon-ng (JSON, patrz `.env.example`).

### Uruchomienie (Docker Compose)
```bash
cp .env.example .env
docker compose up --build
```

Serwer MCP: `http://localhost:8000` (FastAPI). Narzędzia CLI dostępne jako polecenia w kontenerze (uruchamiane przez skrypty w `src/tools`).

### Przekazywanie kluczy API
- W pliku `.env` ustaw: `HUNTER_API_KEY` oraz ewentualne `RECONNG_API_KEYS` w formacie JSON.
- Docker Compose automatycznie wczyta `.env` i przekaże do kontenera.
- Serwer MCP odczytuje klucze przy starcie i wystawia spójne endpointy.

Przykład `RECONNG_API_KEYS`:
```json
{"shodan_api":"<SHODAN_KEY>", "binaryedge_api":"<BINARYEDGE_KEY>"}
```

### Główne funkcje narzędzi
- Sherlock: wyszukiwanie nazw użytkowników na wielu serwisach, wynik z linkami/probką dowodów.
- Holehe: sprawdzanie czy email jest powiązany z kontami na popularnych serwisach.
- Hunter.io: wyszukiwanie i weryfikacja adresów email domeny/osoby (API).
- Recon-ng: framework recon z modułami do enumeracji (domeny, osoby, kontakty, social, breaches).

### MCP
Serwer MCP eksponuje proste endpointy do uruchamiania powyższych narzędzi, zwracając ujednolicone JSON-y. Wrapper MCP ułatwia integrację z agentami AI.


