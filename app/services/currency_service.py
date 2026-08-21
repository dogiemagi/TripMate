import httpx
import logging
from typing import Dict, Any
from app.models.schemas import CurrencyConvertRequest

logger = logging.getLogger("voyage.budget")

EXCHANGE_RATES_USD = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 154.5,
    "AUD": 1.52,
    "CAD": 1.37,
    "CHF": 0.91,
    "CNY": 7.24,
    "INR": 83.45,
    "SGD": 1.35,
    "AED": 3.67,
    "THB": 36.8,
    "IDR": 16250.0,
    "BRL": 5.15,
    "MXN": 16.85
}

CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
    "INR": "₹", "AED": "AED ", "AUD": "A$", "CAD": "C$",
    "SGD": "S$", "CHF": "CHF ", "CNY": "¥", "THB": "฿"
}

DAILY_COST_BENCHMARKS = {
    "tokyo": {"backpacker": 45, "midrange": 130, "luxury": 420, "currency": "JPY", "symbol": "¥"},
    "paris": {"backpacker": 65, "midrange": 160, "luxury": 500, "currency": "EUR", "symbol": "€"},
    "rome": {"backpacker": 55, "midrange": 140, "luxury": 450, "currency": "EUR", "symbol": "€"},
    "new york": {"backpacker": 90, "midrange": 250, "luxury": 750, "currency": "USD", "symbol": "$"},
    "london": {"backpacker": 75, "midrange": 190, "luxury": 580, "currency": "GBP", "symbol": "£"},
    "bali": {"backpacker": 25, "midrange": 65, "luxury": 220, "currency": "IDR", "symbol": "Rp"},
    "bangkok": {"backpacker": 30, "midrange": 75, "luxury": 250, "currency": "THB", "symbol": "฿"},
    "dubai": {"backpacker": 70, "midrange": 200, "luxury": 600, "currency": "AED", "symbol": "AED"}
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
    def get_trip_budget_estimate(city: str, days: int = 5, style: str = "midrange") -> Dict[str, Any]:
        c_clean = city.strip().lower()
        benchmark = DAILY_COST_BENCHMARKS.get(c_clean, {"backpacker": 50, "midrange": 140, "luxury": 450, "currency": "USD", "symbol": "$"})
        
        style_key = style.lower()
        daily_usd = benchmark.get(style_key, benchmark.get("midrange", 140))
        total_usd = daily_usd * days

        breakdown = {
            "Accommodation (Hotel/Hostel/Airbnb)": round(total_usd * 0.42, 2),
            "Dining & Local Gastronomy": round(total_usd * 0.28, 2),
            "Activities, Museums & Guided Tours": round(total_usd * 0.16, 2),
            "Public Transit & Rideshare": round(total_usd * 0.08, 2),
            "Souvenirs & Contingency Buffer": round(total_usd * 0.06, 2)
        }

        return {
            "status": "success",
            "city": city.title(),
            "duration_days": days,
            "budget_tier": style.title(),
            "daily_budget_usd": daily_usd,
            "total_budget_usd": total_usd,
            "cost_breakdown": breakdown,
            "money_saving_hacks": [
                "Purchase multi-day museum and public transit combo passes to save up to 35%.",
                "Withdraw local currency from official bank ATMs rather than airport foreign exchange booths.",
                "Dine on the chef's lunch set menu (Menu del Día / Teishoku) for Michelin-level food at 50% evening prices."
            ]
        }
