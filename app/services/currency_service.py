import httpx
import logging
from typing import Dict, Any
from app.models.schemas import CurrencyConvertRequest

logger = logging.getLogger("voyage.budget")

# Live Benchmark Currency Matrix
EXCHANGE_RATES_USD = {
    "INR": 83.50,
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 154.5,
    "AUD": 1.52,
    "CAD": 1.37,
    "CHF": 0.91,
    "CNY": 7.24,
    "SGD": 1.35,
    "AED": 3.67,
    "THB": 36.8,
    "IDR": 16250.0,
    "BRL": 5.15,
    "MXN": 16.85
}

CURRENCY_SYMBOLS = {
    "INR": "₹", "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
    "AED": "AED ", "AUD": "A$", "CAD": "C$", "SGD": "S$",
    "CHF": "CHF ", "CNY": "¥", "THB": "฿", "IDR": "Rp "
}

# Daily cost benchmarks in INR (₹)
DAILY_COST_BENCHMARKS_INR = {
    "delhi": {"backpacker": 1800, "midrange": 4500, "luxury": 16000},
    "mumbai": {"backpacker": 2200, "midrange": 5500, "luxury": 20000},
    "goa": {"backpacker": 1500, "midrange": 4000, "luxury": 15000},
    "bengaluru": {"backpacker": 1800, "midrange": 4800, "luxury": 17000},
    "tokyo": {"backpacker": 3750, "midrange": 10800, "luxury": 35000},
    "paris": {"backpacker": 5400, "midrange": 13300, "luxury": 41500},
    "rome": {"backpacker": 4600, "midrange": 11600, "luxury": 37500},
    "new york": {"backpacker": 7500, "midrange": 20800, "luxury": 62500},
    "london": {"backpacker": 6250, "midrange": 15800, "luxury": 48000},
    "dubai": {"backpacker": 5800, "midrange": 16500, "luxury": 50000},
    "bali": {"backpacker": 2100, "midrange": 5400, "luxury": 18500},
    "bangkok": {"backpacker": 2500, "midrange": 6250, "luxury": 21000}
}

class CurrencyBudgetService:
    @staticmethod
    async def convert(req: CurrencyConvertRequest) -> Dict[str, Any]:
        from_cur = req.from_currency.upper().strip()
        to_cur = req.to_currency.upper().strip()
        amt = req.amount

        rate = 1.0
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                url = f"https://open.er-api.com/v6/latest/{from_cur}"
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    rates = data.get("rates", {})
                    if to_cur in rates:
                        rate = rates[to_cur]
                        converted = round(amt * rate, 2)
                        return {
                            "status": "success",
                            "source": "OpenExchangeLive",
                            "from_currency": from_cur,
                            "to_currency": to_cur,
                            "amount": amt,
                            "converted_amount": converted,
                            "exchange_rate": round(rate, 4),
                            "inverse_rate": round(1 / rate, 4) if rate else 0,
                            "symbol": CURRENCY_SYMBOLS.get(to_cur, "")
                        }
        except Exception as e:
            logger.warning(f"Live currency API failed: {e}")

        usd_from = EXCHANGE_RATES_USD.get(from_cur, 1.0)
        usd_to = EXCHANGE_RATES_USD.get(to_cur, 1.0)
        rate = usd_to / usd_from
        converted = round(amt * rate, 2)

        return {
            "status": "success",
            "source": "VoyageFX-Engine",
            "from_currency": from_cur,
            "to_currency": to_cur,
            "amount": amt,
            "converted_amount": converted,
            "exchange_rate": round(rate, 4),
            "inverse_rate": round(1 / rate, 4) if rate else 0,
            "symbol": CURRENCY_SYMBOLS.get(to_cur, "")
        }

    @staticmethod
    def get_trip_budget_estimate(city: str, days: int = 5, style: str = "midrange", currency: str = "INR") -> Dict[str, Any]:
        c_clean = city.strip().lower()
        benchmark = DAILY_COST_BENCHMARKS_INR.get(
            c_clean, 
            {"backpacker": 3500, "midrange": 9500, "luxury": 28000}
        )
        
        style_key = style.lower()
        daily_inr = benchmark.get(style_key, benchmark.get("midrange", 9500))
        total_inr = daily_inr * days

        cur_upper = currency.upper().strip()
        fx_to_inr = EXCHANGE_RATES_USD.get("INR", 83.5) / EXCHANGE_RATES_USD.get(cur_upper, 83.5)
        
        daily_target = round(daily_inr / fx_to_inr, 2)
        total_target = round(total_inr / fx_to_inr, 2)
        sym = CURRENCY_SYMBOLS.get(cur_upper, "₹")

        breakdown = {
            "Accommodation & Stays": round(total_target * 0.42, 2),
            "Dining & Gastronomy": round(total_target * 0.28, 2),
            "Activities, Entry & Guided Tours": round(total_target * 0.16, 2),
            "Local Transit & Cabs": round(total_target * 0.08, 2),
            "Contingency & Souvenir Buffer": round(total_target * 0.06, 2)
        }

        return {
            "status": "success",
            "city": city.title(),
            "duration_days": days,
            "budget_tier": style.title(),
            "currency": cur_upper,
            "currency_symbol": sym,
            "daily_budget": daily_target,
            "total_budget": total_target,
            "cost_breakdown": breakdown,
            "money_saving_hacks": [
                "Book verified boutique homestays or heritage properties for premium comfort at 30% lower cost.",
                "Opt for local metro smart cards or city transit day-passes for seamless commute.",
                "Enjoy local lunchtime special thalis and chef sets for authentic flavors at economical pricing."
            ]
        }
