# NSE Options AI Monitor — read-only research dashboard

Tracks **ULTRACEMCO** and **JSWSTEEL** in **intraday** and **swing** views. Advisory states are BUY, SELL, EXIT, WAIT, but **only WAIT is currently enabled**. No Angel One SmartAPI connection has been authenticated, and no live market quotes are available. The app does **not** send alerts or place orders.

## Routes
- `GET /health`: backend health, broker status and safety flags
- `GET /api/signals`: four advisory cards with exact strike, expiry, entry, stop, targets, risk, and IST timestamp fields. These fields are **null/unavailable** until sourced and validated. The endpoint never fabricates data.

## Vercel
`vercel.json` builds the static frontend and Python serverless API in the same project. Set the Vercel root directory to the repository root, and deploy `main`. The frontend uses relative `/api/signals`, so it must be deployed alongside the API or later configured to use a separately hosted API. If using two separate Vercel projects, configure both to deploy this repository, or add a proxy; a frontend-only deployment cannot call the API at a different domain with the current relative path.

## VPS
The existing `docker-compose.yml` binds the backend to `127.0.0.1:8091`. Do not overwrite existing reverse-proxy routes. For cross-origin requests set `FRONTEND_ORIGIN` to your exact frontend origin. Keep secrets out of GitHub and client JavaScript.

## Implementation and safety gates
1. Confirm SmartAPI market-data entitlement, static-IP/allowlisting requirements, allowed instruments and broker rate limits. Use a secure server-side connection only. Do not commit broker API keys, passwords, tokens, TOTP seeds, or credentials.
2. Build a read-only provider adapter for verified spot/futures/option quotes, exchange timestamps, lot size, expiry, strikes, bid/ask, OI and OI change, volume, PCR. Persist paired snapshots to a durable store (not Vercel ephemeral filesystem). Include expiry-calendar and exchange-holiday validation.
3. Validate same-session synchronization, freshness, spreads, liquidity, capital and lot costs. The included `backend/signals.py` contains a **fail-closed validation scaffold**, not a trading strategy. It deliberately emits WAIT even with a validated snapshot until backtesting and strategy approval.
4. Backtest and document intraday vs swing rules, stop/target sizing, gap risk, max loss, trading costs and slippage. A ₹5,000 reference capital and ₹100 reference risk ceiling are defaults, not proof an option lot fits that budget.
5. Only then implement advisory BUY/SELL/EXIT signals, suppression of repeated alerts, and IST timestamps. WAIT is never pushed as a notification. Keep order placement absent.
6. Schedule checks only in permitted NSE sessions; market closure, stale feeds, missing previous comparison, and unchanged conditions produce no alerts.

**No automated trading. No invented quotes. No guaranteed recommendations.**
