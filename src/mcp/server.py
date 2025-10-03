from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

from src.tools.sherlock_cli import run_sherlock
from src.tools.holehe_cli import run_holehe
from src.tools.hunter_cli import (
    hunter_domain_search,
    hunter_email_finder,
    hunter_email_verifier,
)
from src.tools.reconng_cli import run_reconng, seed_reconng_api_keys
from src.config.settings import settings


app = FastAPI(title="CyberHunt MCP", version="0.1.0")


class SherlockRequest(BaseModel):
    usernames: List[str]


class HoleheRequest(BaseModel):
    emails: List[str]


class HunterDomainRequest(BaseModel):
    domain: str
    api_key: Optional[str] = None


class HunterFinderRequest(BaseModel):
    full_name: str
    domain: str
    api_key: Optional[str] = None


class HunterVerifyRequest(BaseModel):
    email: str
    api_key: Optional[str] = None


class ReconNgRequest(BaseModel):
    commands: List[str]


@app.on_event("startup")
def on_startup():
    seed_reconng_api_keys()


@app.post("/tools/sherlock")
def mcp_sherlock(req: SherlockRequest):
    return run_sherlock(req.usernames)


@app.post("/tools/holehe")
def mcp_holehe(req: HoleheRequest):
    return run_holehe(req.emails)


@app.post("/tools/hunter/domain-search")
def mcp_hunter_domain(req: HunterDomainRequest):
    return hunter_domain_search(req.domain, req.api_key)


@app.post("/tools/hunter/email-finder")
def mcp_hunter_finder(req: HunterFinderRequest):
    return hunter_email_finder(req.full_name, req.domain, req.api_key)


@app.post("/tools/hunter/email-verifier")
def mcp_hunter_verifier(req: HunterVerifyRequest):
    return hunter_email_verifier(req.email, req.api_key)


@app.post("/tools/reconng")
def mcp_reconng(req: ReconNgRequest):
    return run_reconng(req.commands)


@app.get("/health")
def health():
    return {"status": "ok", "log_level": settings.log_level}


