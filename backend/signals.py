"""Conservative, read-only advisory rules. No orders, no fabricated quotes."""
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
SYMBOLS = ("ULTRACEMCO", "JSWSTEEL")
CAPITAL_INR = 5000
MAX_RISK_INR = 100  # 2% of reference capital; configurable later
MAX_SPREAD_PCT = 2.0
MAX_QUOTE_AGE_SECONDS = 90


def waiting(symbol: str, style: str, reason: str) -> dict:
    return {
        "symbol": symbol, "style": style, "signal": "WAIT",
        "actionable": False, "reason": reason,
        "source": None, "as_of_ist": None, "expiry": None,
        "strike": None, "option_type": None, "spot": None, "futures": None,
        "entry": None, "stop_loss": None, "target_1": None, "target_2": None,
        "lot_size": None, "estimated_lot_cost": None,
        "max_planned_risk": None, "pcr": None, "call_oi": None, "put_oi": None,
        "call_oi_change": None, "put_oi_change": None, "volume": None,
        "bid": None, "ask": None, "support": None, "resistance": None,
        "breakout_level": None, "breakdown_level": None,
    }


def evaluate(symbol: str, style: str, snapshot: dict | None = None, previous: dict | None = None) -> dict:
    if symbol not in SYMBOLS or style not in ("intraday", "swing"):
        raise ValueError("Unsupported symbol or style")
    if not snapshot or not previous:
        return waiting(symbol, style, "No paired, verified Angel One market snapshots available")
    if snapshot.get("provider") != "Angel One SmartAPI" or previous.get("provider") != "Angel One SmartAPI":
        return waiting(symbol, style, "Market-data provenance unverified")
    required = ("timestamp", "spot", "futures", "expiry", "strike", "option_type",
                "premium", "bid", "ask", "lot_size", "call_oi", "put_oi",
                "call_oi_change", "put_oi_change", "volume", "pcr",
                "support", "resistance", "breakout_level", "breakdown_level")
    if any(snapshot.get(k) is None for k in required):
        return waiting(symbol, style, "Incomplete synchronized equity, futures and options snapshot")
    try:
        ts = datetime.fromisoformat(snapshot["timestamp"])
        prev_ts = datetime.fromisoformat(previous["timestamp"])
        if ts.tzinfo is None or prev_ts.tzinfo is None:
            raise ValueError("Timezone required")
        now = datetime.now(IST)
        ts = ts.astimezone(IST)
        prev_ts = prev_ts.astimezone(IST)
        if ts > now + timedelta(seconds=10) or (now - ts).total_seconds() > MAX_QUOTE_AGE_SECONDS:
            return waiting(symbol, style, "Market snapshot stale or clock mismatch")
        if not prev_ts < ts:
            return waiting(symbol, style, "Previous snapshot is not earlier than current snapshot")
        if snapshot.get("synchronized") is not True or previous.get("synchronized") is not True:
            return waiting(symbol, style, "Spot, futures and option timestamps not synchronized")
        if ts.weekday() > 4 or not time(9, 15) <= ts.time() <= time(15, 30):
            return waiting(symbol, style, "Outside regular NSE market hours")
        if snapshot["option_type"] not in ("CE", "PE"):
            raise ValueError("Option type")
        bid, ask = float(snapshot["bid"]), float(snapshot["ask"])
        premium = float(snapshot["premium"])
        lot = int(snapshot["lot_size"])
        if min(bid, ask, premium) <= 0 or ask < bid or lot <= 0:
            raise ValueError("Invalid option quote")
        if (ask - bid) / ((ask + bid) / 2) * 100 > MAX_SPREAD_PCT:
            return waiting(symbol, style, "Option bid-ask spread exceeds 2%")
        if ask * lot > CAPITAL_INR:
            return waiting(symbol, style, "One option lot exceeds reference capital of INR 5,000")
    except (KeyError, ValueError, TypeError, OverflowError):
        return waiting(symbol, style, "Invalid or unverifiable quote fields")
    # Deliberately no BUY/SELL rule until validated, backtested indicator logic,
    # provider instrument metadata, risk sizing and authenticated ingestion exist.
    return waiting(symbol, style, "Verified snapshot received, but actionable strategy validation is not enabled")


def overview() -> dict:
    return {
        "read_only": True, "order_placement_enabled": False,
        "provider": "Angel One SmartAPI", "data_connected": False,
        "reference_capital_inr": CAPITAL_INR, "max_planned_risk_inr": MAX_RISK_INR,
        "signals": [evaluate(symbol, style) for symbol in SYMBOLS for style in ("intraday", "swing")],
        "note": "WAIT means insufficient verified evidence, not a trading recommendation. No alerts are sent for WAIT.",
    }
