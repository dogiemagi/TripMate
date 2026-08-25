import httpx
import logging
from typing import Dict, Any

logger = logging.getLogger("voyage.geo")

POPULAR_DESTINATIONS = {
    "chennai": (13.0827, 80.2707, "Chennai", "India", "Chennai, Tamil Nadu, India"),
    "chennai, india": (13.0827, 80.2707, "Chennai", "India", "Chennai, Tamil Nadu, India"),
    "delhi": (28.6139, 77.2090, "Delhi", "India", "Delhi, India"),
    "delhi, india": (28.6139, 77.2090, "Delhi", "India", "Delhi, India"),
    "new delhi": (28.6139, 77.2090, "New Delhi", "India", "New Delhi, India"),
    "mumbai": (19.0760, 72.8777, "Mumbai", "India", "Mumbai, Maharashtra, India"),
    "mumbai, india": (19.0760, 72.8777, "Mumbai", "India", "Mumbai, Maharashtra, India"),
    "bengaluru": (12.9716, 77.5946, "Bengaluru", "India", "Bengaluru, Karnataka, India"),
    "bangalore": (12.9716, 77.5946, "Bengaluru", "India", "Bengaluru, Karnataka, India"),
    "kolkata": (22.5726, 88.3639, "Kolkata", "India", "Kolkata, West Bengal, India"),
    "jaipur": (26.9124, 75.7873, "Jaipur", "India", "Jaipur, Rajasthan, India"),
    "hyderabad": (17.3850, 78.4867, "Hyderabad", "India", "Hyderabad, Telangana, India"),
    "hydrabad": (17.3850, 78.4867, "Hyderabad", "India", "Hyderabad, Telangana, India"),
    "hyderabad, india": (17.3850, 78.4867, "Hyderabad", "India", "Hyderabad, Telangana, India"),
    "goa": (15.2993, 74.1240, "Goa", "India", "Goa, India"),
    "goa, india": (15.2993, 74.1240, "Goa", "India", "Goa, India"),
    "kashmir": (34.0837, 74.7973, "Srinagar (Kashmir)", "India", "Srinagar, Kashmir, India"),
    "ladakh": (34.1526, 77.5771, "Leh (Ladakh)", "India", "Leh Ladakh, India"),
    "kerala": (9.9312, 76.2673, "Kochi (Kerala)", "India", "Kochi, Kerala, India"),
    "bali": (-8.3405, 115.0920, "Bali", "Indonesia", "Bali, Indonesia"),
    "phuket": (7.8804, 98.3923, "Phuket", "Thailand", "Phuket, Thailand"),
    "maldives": (4.1755, 73.5093, "Malé", "Maldives", "Malé, Maldives"),
    "dubai": (25.2048, 55.2708, "Dubai", "United Arab Emirates", "Dubai, UAE"),
    "dubai, uae": (25.2048, 55.2708, "Dubai", "United Arab Emirates", "Dubai, UAE"),
    "singapore": (1.3521, 103.8198, "Singapore", "Singapore", "Singapore"),
    "paris": (48.8566, 2.3522, "Paris", "France", "Paris, France"),
    "paris, france": (48.8566, 2.3522, "Paris", "France", "Paris, France"),
    "tokyo": (35.6762, 139.6503, "Tokyo", "Japan", "Tokyo, Japan"),
    "tokyo, japan": (35.6762, 139.6503, "Tokyo", "Japan", "Tokyo, Japan"),
    "london": (51.5074, -0.1278, "London", "United Kingdom", "London, UK"),
    "london, uk": (51.5074, -0.1278, "London", "United Kingdom", "London, UK"),
    "new york": (40.7128, -74.0060, "New York", "United States", "New York, USA"),
    "rome": (41.9028, 12.4964, "Rome", "Italy", "Rome, Italy"),
}

class GeoService:
    @staticmethod
    async def resolve_location(query: str, default_lat: float = 28.6139, default_lon: float = 77.2090) -> Dict[str, Any]:
        """
        Robustly resolves any location query (city, city+country, landmark, region)
        using Open-Meteo search with multi-candidate fallbacks and OpenStreetMap Nominatim.
        """
        clean = query.strip()
        if not clean:
            return {
                "latitude": default_lat,
                "longitude": default_lon,
                "city": "Delhi",
                "country": "India",
                "display_name": "Delhi, India"
            }

        lower_clean = clean.lower()
        if lower_clean in POPULAR_DESTINATIONS:
            lat, lon, c_name, country, disp = POPULAR_DESTINATIONS[lower_clean]
            return {
                "latitude": lat,
                "longitude": lon,
                "city": c_name,
                "country": country,
                "display_name": disp,
                "source": "curated"
            }

        candidates = [clean]
        if "," in clean:
            # e.g., "Paris, France" -> try "Paris, France", then "Paris"
            parts = [p.strip() for p in clean.split(",") if p.strip()]
            if parts and parts[0] != clean:
                candidates.append(parts[0])
            if len(parts) >= 2:
                # Also try first and last part if multiple commas
                candidates.append(f"{parts[0]} {parts[-1]}")


        # 1. Try Open-Meteo Geocoding
        async with httpx.AsyncClient(timeout=6.0) as client:
            for candidate in candidates:
                try:
                    resp = await client.get(
                        "https://geocoding-api.open-meteo.com/v1/search",
                        params={"name": candidate, "count": 1, "language": "en", "format": "json"}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        results = data.get("results")
                        if results and len(results) > 0:
                            top = results[0]
                            city_name = top.get("name", clean)
                            country_name = top.get("country", "")
                            display_str = f"{city_name}, {country_name}" if country_name else city_name
                            return {
                                "latitude": float(top["latitude"]),
                                "longitude": float(top["longitude"]),
                                "city": city_name,
                                "country": country_name,
                                "display_name": display_str,
                                "source": "open-meteo"
                            }
                except Exception as e:
                    logger.debug(f"Open-Meteo lookup error for '{candidate}': {e}")

            # 2. Try Nominatim Fallback
            for candidate in candidates:
                try:
                    resp = await client.get(
                        "https://nominatim.openstreetmap.org/search",
                        params={"q": candidate, "format": "json", "limit": 1, "addressdetails": 1},
                        headers={"User-Agent": "VoyageAI-Platform/1.0 (travel-intelligence)"}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        if data and len(data) > 0:
                            top = data[0]
                            address = top.get("address", {})
                            city_name = (
                                address.get("city")
                                or address.get("town")
                                or address.get("village")
                                or address.get("municipality")
                                or top.get("display_name", clean).split(",")[0].strip()
                            )
                            country_name = address.get("country", "")
                            display_str = f"{city_name}, {country_name}" if country_name else city_name
                            return {
                                "latitude": float(top["lat"]),
                                "longitude": float(top["lon"]),
                                "city": city_name,
                                "country": country_name,
                                "display_name": display_str,
                                "source": "nominatim"
                            }
                except Exception as e:
                    logger.debug(f"Nominatim lookup error for '{candidate}': {e}")

        # Fallback
        return {
            "latitude": default_lat,
            "longitude": default_lon,
            "city": clean.title(),
            "country": "Global",
            "display_name": clean.title(),
            "source": "fallback"
        }
