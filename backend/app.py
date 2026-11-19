"""Read-only API. No trade placement, broker secrets, or mock market quotes."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.signals import overview

app = FastAPI(title="NSE Options AI Monitor", docs_url=None, redoc_url=None)
origins = [x.strip() for x in os.getenv("FRONTEND_ORIGIN", "").split(",") if x.strip()]
if origins:
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET"], allow_headers=[])


@app.get("/health")
def health():
    return {"ok": True, "read_only": True, "data_connected": False,
            "order_placement_enabled": False, "signals_enabled": False}


@app.get("/api/signals")
def signals():
    return overview()
