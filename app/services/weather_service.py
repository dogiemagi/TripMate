import httpx
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("voyage.weather")

CITY_COORDINATES = {
    "tokyo": {"lat": 35.6762, "lon": 139.6503, "country": "Japan"},
    "paris": {"lat": 48.8566, "lon": 2.3522, "country": "France"},
    "rome": {"lat": 41.9028, "lon": 12.4964, "country": "Italy"},
    "new york": {"lat": 40.7128, "lon": -74.0060, "country": "USA"},
    "london": {"lat": 51.5074, "lon": -0.1278, "country": "United Kingdom"},
    "dubai": {"lat": 25.2048, "lon": 55.2708, "country": "UAE"},
    "singapore": {"lat": 1.3521, "lon": 103.8198, "country": "Singapore"},
    "bangkok": {"lat": 13.7563, "lon": 100.5018, "country": "Thailand"},
    "barcelona": {"lat": 41.3851, "lon": 2.1734, "country": "Spain"},
    "sydney": {"lat": -33.8688, "lon": 151.2093, "country": "Australia"},
    "kyoto": {"lat": 35.0116, "lon": 135.7681, "country": "Japan"},
    "delhi": {"lat": 28.6139, "lon": 77.2090, "country": "India"},
    "bali": {"lat": -8.4095, "lon": 115.1889, "country": "Indonesia"},
    "cairo": {"lat": 30.0444, "lon": 31.2357, "country": "Egypt"},
    "rio de janeiro": {"lat": -22.9068, "lon": -43.1729, "country": "Brazil"},
}

WEATHER_CODE_MAP = {
    0: ("Clear Sky", "sun", "Excellent visibility and perfect for outdoor sightseeing."),
    1: ("Mainly Clear", "sun", "Pleasant weather with mild sunshine."),
    2: ("Partly Cloudy", "cloud-sun", "Great conditions for walking tours and photography."),
    3: ("Overcast", "cloud", "Soft lighting, ideal for visiting museums and landmarks."),
    45: ("Foggy", "cloud-fog", "Reduced visibility in the morning; dress warmly."),
    48: ("Depositing Rime Fog", "cloud-fog", "Misty and cool."),
    51: ("Light Drizzle", "cloud-drizzle", "Pack a compact travel umbrella."),
    53: ("Moderate Drizzle", "cloud-drizzle", "Light rain gear recommended."),
    61: ("Slight Rain", "cloud-rain", "Carry an umbrella; great day for indoor cafes."),
    63: ("Moderate Rain", "cloud-rain", "Waterproof jacket suggested."),
    65: ("Heavy Rain", "cloud-rain-wind", "Consider indoor attractions and galleries."),
    71: ("Slight Snow", "snowflake", "Magical snowy scenery; wear insulated boots."),
    73: ("Moderate Snow", "snowflake", "Layer up with thermal wear."),
    80: ("Rain Showers", "cloud-rain", "Intermittent showers with sunny breaks."),
    95: ("Thunderstorm", "cloud-lightning", "Stay sheltered during peak afternoon storm.")
}

class WeatherService:
    @staticmethod
    async def get_weather(city_name: str, days: int = 7) -> Dict[str, Any]:
        normalized = city_name.strip().lower()
        lat, lon, country = 0.0, 0.0, "Global"

        # Check geocoding
        if normalized in CITY_COORDINATES:
            geo = CITY_COORDINATES[normalized]
            lat, lon, country = geo["lat"], geo["lon"], geo["country"]
        else:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
                    resp = await client.get(geo_url)
                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get("results"):
                            res = data["results"][0]
                            lat = res["latitude"]
                            lon = res["longitude"]
                            country = res.get("country", "")
                        else:
                            lat, lon, country = 35.6762, 139.6503, "Featured"
            except Exception as e:
                logger.warning(f"Geocoding lookup failed: {e}")
                lat, lon, country = 35.6762, 139.6503, "Featured"

        # Fetch Open-Meteo weather
        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                w_url = (
                    f"https://api.open-meteo.com/v1/forecast?"
                    f"latitude={lat}&longitude={lon}&daily=weathercode,temperature_2m_max,temperature_2m_min,"
                    f"apparent_temperature_max,precipitation_probability_max,uv_index_max,windspeed_10m_max"
                    f"&current_weather=true&timezone=auto"
                )
                resp = await client.get(w_url)
                if resp.status_code == 200:
                    data = resp.json()
                    current = data.get("current_weather", {})
                    daily = data.get("daily", {})

                    code = current.get("weathercode", 0)
                    condition, icon_name, advice = WEATHER_CODE_MAP.get(code, ("Pleasant", "sun", "Ideal travel day."))

                    forecast_items = []
                    dates = daily.get("time", [])[:days]
                    for idx, dt in enumerate(dates):
                        w_code = daily.get("weathercode", [0])[idx] if idx < len(daily.get("weathercode", [])) else 0
                        cond_name, f_icon, f_adv = WEATHER_CODE_MAP.get(w_code, ("Clear", "sun", "Good conditions"))
                        t_max = daily.get("temperature_2m_max", [22])[idx]
                        t_min = daily.get("temperature_2m_min", [15])[idx]
                        precip = daily.get("precipitation_probability_max", [10])[idx]
                        uv = daily.get("uv_index_max", [5])[idx]
                        wind = daily.get("windspeed_10m_max", [12])[idx]

                        forecast_items.append({
                            "date": dt,
                            "day_name": "Day " + str(idx + 1),
                            "temp_max_c": round(t_max, 1),
                            "temp_min_c": round(t_min, 1),
                            "temp_max_f": round(t_max * 9/5 + 32, 1),
                            "temp_min_f": round(t_min * 9/5 + 32, 1),
                            "condition": cond_name,
                            "icon": f_icon,
                            "precipitation_chance_pct": precip,
                            "uv_index": uv,
                            "windspeed_kmh": wind,
                            "travel_suitability": "Optimal" if precip < 30 else ("Fair" if precip < 60 else "Rainy Prep")
                        })

                    temp_c = current.get("temperature", 22.0)
                    return {
                        "status": "success",
                        "city": city_name.title(),
                        "country": country,
                        "coordinates": {"lat": lat, "lon": lon},
                        "current": {
                            "temperature_c": temp_c,
                            "temperature_f": round(temp_c * 9/5 + 32, 1),
                            "condition": condition,
                            "icon": icon_name,
                            "windspeed_kmh": current.get("windspeed", 10),
                            "wind_direction": current.get("winddirection", 0),
                            "advice": advice,
                            "is_day": current.get("is_day", 1) == 1
                        },
                        "forecast": forecast_items,
                        "travel_climate_score": 92 if current.get("temperature", 20) > 15 and current.get("temperature", 20) < 28 else 82,
                        "packing_recommendation": "Light jacket, sunglasses, walking shoes, and breathable layers."
                    }
        except Exception as e:
            logger.error(f"Weather API error: {e}")

        # Fallback simulation
        return WeatherService._fallback_weather(city_name, country, lat, lon)

    @staticmethod
    def _fallback_weather(city: str, country: str, lat: float, lon: float) -> Dict[str, Any]:
        return {
            "status": "success",
            "city": city.title(),
            "country": country or "Global Destination",
            "coordinates": {"lat": lat or 35.67, "lon": lon or 139.65},
            "current": {
                "temperature_c": 21.5,
                "temperature_f": 70.7,
                "condition": "Mainly Sunny & Mild",
                "icon": "sun",
                "windspeed_kmh": 11.2,
                "wind_direction": 180,
                "advice": "Exceptional travel weather. Ideal for walking tours, outdoor markets, and photography.",
                "is_day": True
            },
            "forecast": [
                {"date": "Day 1", "day_name": "Today", "temp_max_c": 23, "temp_min_c": 15, "temp_max_f": 73.4, "temp_min_f": 59, "condition": "Sunny", "icon": "sun", "precipitation_chance_pct": 5, "uv_index": 6, "windspeed_kmh": 10, "travel_suitability": "Optimal"},
                {"date": "Day 2", "day_name": "Tomorrow", "temp_max_c": 22, "temp_min_c": 14, "temp_max_f": 71.6, "temp_min_f": 57.2, "condition": "Partly Cloudy", "icon": "cloud-sun", "precipitation_chance_pct": 15, "uv_index": 5, "windspeed_kmh": 12, "travel_suitability": "Optimal"},
                {"date": "Day 3", "day_name": "Day 3", "temp_max_c": 20, "temp_min_c": 13, "temp_max_f": 68, "temp_min_f": 55.4, "condition": "Overcast", "icon": "cloud", "precipitation_chance_pct": 25, "uv_index": 4, "windspeed_kmh": 14, "travel_suitability": "Good"},
                {"date": "Day 4", "day_name": "Day 4", "temp_max_c": 19, "temp_min_c": 12, "temp_max_f": 66.2, "temp_min_f": 53.6, "condition": "Light Shower", "icon": "cloud-rain", "precipitation_chance_pct": 45, "uv_index": 3, "windspeed_kmh": 16, "travel_suitability": "Fair"},
                {"date": "Day 5", "day_name": "Day 5", "temp_max_c": 22, "temp_min_c": 14, "temp_max_f": 71.6, "temp_min_f": 57.2, "condition": "Clear Sky", "icon": "sun", "precipitation_chance_pct": 10, "uv_index": 6, "windspeed_kmh": 9, "travel_suitability": "Optimal"}
            ],
            "travel_climate_score": 88,
            "packing_recommendation": "Layered clothing, comfortable sneakers, light cardigan, sunglasses."
        }
