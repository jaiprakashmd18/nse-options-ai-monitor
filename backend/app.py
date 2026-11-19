"""Read-only market data backend skeleton. No trading endpoints."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NSE Options AI Monitor", docs_url=None, redoc_url=None)
origin = os.getenv("FRONTEND_ORIGIN", "")
if origin:
    app.add_middleware(CORSMiddleware, allow_origins=[origin], allow_methods=["GET"], allow_headers=[])

@app.get("/health")
def health():
    return {"ok": True, "read_only": True, "data_connected": False}
