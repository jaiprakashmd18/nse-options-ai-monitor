# NSE Options AI Monitor (read-only starter)

Mobile-friendly Vercel frontend and Oracle VPS FastAPI skeleton for ULTRACEMCO and JSWSTEEL. No trading or order placement.

## Vercel
Deploy the repository with vercel.json; it serves frontend/index.html. No secrets in the frontend.

## Oracle VPS
Verify public IP and existing Caddy routes before changing the server. Run docker compose up -d --build from the repository root. Backend binds 127.0.0.1:8091 only. Put it behind authenticated HTTPS reverse proxy. Configure FRONTEND_ORIGIN to the Vercel origin.

## Next
Verify Angel One SmartAPI terms, read-only market-data access, static-IP requirements and session flow. Keep secrets server-side. Add authenticated market-data endpoints, timestamps, stale-data handling, and 15-minute scheduled checks during NSE trading hours. Never implement order placement.
