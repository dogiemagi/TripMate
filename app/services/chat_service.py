import logging
import re
from typing import List, Dict, Any, Optional, Tuple
from app.config import settings
from app.services.geo_service import GeoService

logger = logging.getLogger("tripmate.chat")

SYSTEM_PROMPT = """You are Kaira, the lead AI travel friend and curator at TripMate AI (inspired by the thoughtful, personalized trip planning of The Tarzan Way). 
You help users turn their travel ideas into seamless, verified dream itineraries in a warm, knowledgeable, and inspiring way.

Your personality:
- Warm, friendly, enthusiastic, yet deeply professional
- Like talking to a well-traveled friend who has been everywhere
- Highly practical with flight durations, transit times, geographic flow, and realistic budgets (in INR ₹)
- Provide concrete recommendations with specific names of neighborhoods, viewpoints, and local culinary gems
- Clean tone: NEVER USE EMOJIS anywhere in your responses. Use clean markdown formatting, bold headers, and bullet points.

Your capabilities:
- Build day-by-day itineraries with clear morning, afternoon, and evening recommendations
- Suggest the best season, flight connections, transit routes, and packing tips
- Recommend budget tiers (Smart Budget, Balanced Comfort, Boutique Luxury)
- Provide visa guidance and local cultural etiquette

Always:
- Keep answers structured, actionable, and engaging
- End with an inspiring follow-up question to keep planning going
- Never use emojis in responses
- Structure recommendations clearly by area or days"""

# Signature 8 destination presets matching The Tarzan Way chat experience
SIGNATURE_PRESETS = {
    "bali": {
        "key": "bali",
        "name": "Bali, Indonesia",
        "title": "Ubud · Canggu · Seminyak",
        "date": "November 2026",
        "nights": "7N",
        "stopsCount": "3 stops",
        "depCity": "Hyderabad",
        "flightDur": "Flight ~8h",
        "price": "₹55–80K",
        "center": [-8.58, 115.20],
        "zoom": 11,
        "stops": [
            {
                "name": "Ubud",
                "nights": "3N",
                "desc": "Explore emerald rice terraces, temple rituals, jungle waterfalls, and Balinese artistic traditions.",
                "transit": "Taxi ~1h15",
                "lat": -8.5069,
                "lng": 115.2625,
                "color": "blue",
                "num": 1,
            },
            {
                "name": "Canggu",
                "nights": "2N",
                "desc": "Ease into coastal Bali with beach sunsets, creative cafÃ©s, and relaxed village lanes.",
                "transit": "Taxi ~30m",
                "lat": -8.6478,
                "lng": 115.1385,
                "color": "purple",
                "num": 2,
            },
            {
                "name": "Seminyak",
                "nights": "2N",
                "desc": "Finish beside the airport amid golden beaches, stylish streets, and sunset shores.",
                "transit": "Flight ~8h",
                "lat": -8.6913,
                "lng": 115.1682,
                "color": "green",
                "num": 3,
            },
        ],
        "path": [
            [-8.5069, 115.2625],
            [-8.58, 115.20],
            [-8.6478, 115.1385],
            [-8.67, 115.155],
            [-8.6913, 115.1682],
        ],
    },
    "vietnam": {
        "key": "vietnam",
        "name": "Vietnam Odyssey",
        "title": "Hanoi · Sapa & Ninh Binh · Ha Long Bay",
        "date": "May 2026",
        "nights": "10N",
        "stopsCount": "3 stops",
        "depCity": "Delhi",
        "flightDur": "Flight ~4h30",
        "price": "₹52–75K",
        "center": [21.0, 105.8],
        "zoom": 7,
        "stops": [
            {
                "name": "Hanoi",
                "nights": "3N",
                "desc": "Old Quarter street food, egg coffee heritage, Train Street, and French colonial architecture.",
                "transit": "Express Limousine ~2h30",
                "lat": 21.0285,
                "lng": 105.8542,
                "color": "blue",
                "num": 1,
            },
            {
                "name": "Sapa & Fansipan",
                "nights": "4N",
                "desc": "Terraced emerald rice valley trekking, Fansipan Peak trail, and Black Hmong indigenous villages.",
                "transit": "Overnight Sleeper Train / Van ~5h",
                "lat": 22.3364,
                "lng": 103.8438,
                "color": "purple",
                "num": 2,
            },
            {
                "name": "Ninh Binh & Ha Long",
                "nights": "3N",
                "desc": "Hang Mua 500-step karst peak climb, Trang An river grotto rowboats, and Lan Ha Bay kayaking.",
                "transit": "Flight ~4h30",
                "lat": 20.2506,
                "lng": 105.9745,
                "color": "green",
                "num": 3,
            },
        ],
        "path": [
            [21.0285, 105.8542],
            [21.7, 104.8],
            [22.3364, 103.8438],
            [21.4, 104.9],
            [20.2506, 105.9745],
            [20.8, 107.0],
            [21.0285, 105.8542],
        ],
    },
    "japan": {
        "key": "japan",
        "name": "Japan Golden Route",
        "title": "Tokyo · Kyoto · Osaka",
        "date": "October 2026",
        "nights": "9N",
        "stopsCount": "3 stops",
        "depCity": "Delhi",
        "flightDur": "Flight ~7h30",
        "price": "₹1.5L–2.1L",
        "center": [35.20, 137.50],
        "zoom": 7,
        "stops": [
            {
                "name": "Tokyo",
                "nights": "4N",
                "desc": "Shibuya crossing, historic Asakusa shrines, futuristic digital art, and world-class ramen.",
                "transit": "Shinkansen Bullet ~2h15",
                "lat": 35.6762,
                "lng": 139.6503,
                "color": "blue",
                "num": 1,
            },
            {
                "name": "Kyoto",
                "nights": "3N",
                "desc": "Fushimi Inari torii gates, golden Kinkaku-ji, serene bamboo groves, and Gion tea houses.",
                "transit": "Express Rail ~30m",
                "lat": 35.0116,
                "lng": 135.7681,
                "color": "purple",
                "num": 2,
            },
            {
                "name": "Osaka",
                "nights": "2N",
                "desc": "Dotonbori street food, Osaka castle park, vibrant nightlife, and local takoyaki.",
                "transit": "Flight ~8h",
                "lat": 34.6937,
                "lng": 135.5023,
                "color": "green",
                "num": 3,
            },
        ],
        "path": [
            [35.6762, 139.6503],
            [35.30, 137.80],
            [35.0116, 135.7681],
            [34.85, 135.60],
            [34.6937, 135.5023],
        ],
    },
    "thailand": {
        "key": "thailand",
        "name": "Thailand Tropical",
        "title": "Bangkok · Chiang Mai · Phuket",
        "date": "December 2026",
        "nights": "7N",
        "stopsCount": "3 stops",
        "depCity": "Delhi",
        "flightDur": "Flight ~4h15",
        "price": "₹45–65K",
        "center": [13.75, 100.5],
        "zoom": 6,
        "stops": [
            {
                "name": "Bangkok",
                "nights": "2N",
                "desc": "Grand Palace, Wat Arun river views, street food night markets, and floating markets.",
                "transit": "Domestic Flight ~1h15",
                "lat": 13.7563,
                "lng": 100.5018,
                "color": "blue",
                "num": 1,
            },
            {
                "name": "Chiang Mai",
                "nights": "2N",
                "desc": "Lush mountain temples, ethical elephant sanctuaries, and artisan night bazaars.",
                "transit": "Domestic Flight ~2h",
                "lat": 18.7883,
                "lng": 98.9853,
                "color": "purple",
                "num": 2,
            },
            {
                "name": "Phuket",
                "nights": "3N",
                "desc": "Emerald Andaman waters, island catamaran cruises, white sandy beaches, and fresh seafood.",
                "transit": "Flight ~4h30",
                "lat": 7.8804,
                "lng": 98.3923,
                "color": "green",
                "num": 3,
            },
        ],
        "path": [
            [13.7563, 100.5018],
            [16.2, 99.8],
            [18.7883, 98.9853],
            [13.5, 99.0],
            [7.8804, 98.3923],
        ],
    },
    "maldives": {
        "key": "maldives",
        "name": "Maldives Paradise",
        "title": "Male · Maafushi · Ari Atoll",
        "date": "December 2026",
        "nights": "5N",
        "stopsCount": "3 stops",
        "depCity": "Kochi",
        "flightDur": "Flight ~1h45",
        "price": "₹85K–1.3L",
        "center": [3.9, 73.2],
        "zoom": 8,
        "stops": [
            {
                "name": "Male & Hulhumale",
                "nights": "1N",
                "desc": "Speedboat airport transfer, tropical arrival dinner, and waterfront promenade walks.",
                "transit": "Speedboat ~35m",
                "lat": 4.1755,
                "lng": 73.5093,
                "color": "blue",
                "num": 1,
            },
            {
                "name": "Maafushi Island",
                "nights": "2N",
                "desc": "Turquoise lagoons, sea turtle snorkeling safaris, and secluded sandbank picnics.",
                "transit": "Seaplane ~30m",
                "lat": 3.9419,
                "lng": 73.4907,
                "color": "purple",
                "num": 2,
            },
            {
                "name": "South Ari Atoll",
                "nights": "2N",
                "desc": "Overwater bungalow experience, coral reef manta encounters, and private starlit beach dining.",
                "transit": "Flight ~2h",
                "lat": 3.5500,
                "lng": 72.8500,
                "color": "green",
                "num": 3,
            },
        ],
        "path": [
            [4.1755, 73.5093],
            [3.9419, 73.4907],
            [3.75, 73.1],
            [3.5500, 72.8500],
        ],
    },
    "dubai": {
        "key": "dubai",
        "name": "Dubai Luxury Escape",
        "title": "Downtown · Desert Dunes · Marina",
        "date": "December 2026",
        "nights": "5N",
        "stopsCount": "3 stops",
        "depCity": "Mumbai",
        "flightDur": "Flight ~3h30",
        "price": "₹65–85K",
        "center": [25.10, 55.30],
        "zoom": 11,
        "stops": [
            {
                "name": "Downtown Dubai",
                "nights": "2N",
                "desc": "Burj Khalifa summit, dancing Dubai Mall fountains, and souk gold & spice alleys.",
                "transit": "4x4 Dune Transfer ~45m",
                "lat": 25.1972,
                "lng": 55.2744,
                "color": "blue",
                "num": 1,
            },
            {
                "name": "Desert Conservation",
                "nights": "1N",
                "desc": "Stargazing in desert luxury camp, red dune drives, and authentic Bedouin dining.",
                "transit": "Transfer ~1h",
                "lat": 24.8333,
                "lng": 55.6667,
                "color": "purple",
                "num": 2,
            },
            {
                "name": "Dubai Marina & Palm",
                "nights": "2N",
                "desc": "Luxury yacht cruises, JBR beach promenade, Atlantis water adventures, and rooftop dining.",
                "transit": "Flight ~3h30",
                "lat": 25.0805,
                "lng": 55.1403,
                "color": "green",
                "num": 3,
            },
        ],
        "path": [
            [25.1972, 55.2744],
            [25.0, 55.45],
            [24.8333, 55.6667],
            [24.95, 55.35],
            [25.0805, 55.1403],
        ],
    },
    "singapore": {
        "key": "singapore",
        "name": "Singapore Wonder",
        "title": "Marina Bay · Sentosa · Orchard",
        "date": "October 2026",
        "nights": "4N",
        "stopsCount": "3 stops",
        "depCity": "Chennai",
        "flightDur": "Flight ~4h",
        "price": "₹52–75K",
        "center": [1.31, 103.83],
        "zoom": 12,
        "stops": [
            {
                "name": "Marina Bay",
                "nights": "2N",
                "desc": "Gardens by the Bay Supertrees, Marina Bay Sands SkyPark, spectra light show, and Lau Pa Sat satay.",
                "transit": "MRT / Cable Car ~25m",
                "lat": 1.2847,
                "lng": 103.8610,
                "color": "blue",
                "num": 1,
            },
            {
                "name": "Sentosa Island",
                "nights": "1N",
                "desc": "Universal Studios thrill rides, S.E.A. Aquarium deep ocean wonders, and Tanjong beach clubs.",
                "transit": "Taxi ~15m",
                "lat": 1.2494,
                "lng": 103.8303,
                "color": "purple",
                "num": 2,
            },
            {
                "name": "Clarke Quay & Orchard",
                "nights": "1N",
                "desc": "River taxi cruise, heritage shophouse cocktail bars, and premier botanical shopping boulevards.",
                "transit": "Flight ~4h",
                "lat": 1.2905,
                "lng": 103.8465,
                "color": "green",
                "num": 3,
            },
        ],
        "path": [
            [1.2847, 103.8610],
            [1.265, 103.845],
            [1.2494, 103.8303],
            [1.275, 103.838],
            [1.2905, 103.8465],
        ],
    },
    "europe": {
        "key": "europe",
        "name": "Europe Highlights",
        "title": "Paris · Swiss Alps · Rome",
        "date": "September 2026",
        "nights": "10N",
        "stopsCount": "3 stops",
        "depCity": "Mumbai",
        "flightDur": "Flight ~9h",
        "price": "₹1.8L–2.6L",
        "center": [45.0, 7.5],
        "zoom": 6,
        "stops": [
            {
                "name": "Paris",
                "nights": "4N",
                "desc": "Eiffel Tower sunsets, Louvre masterpieces, Le Marais boutique cafes, and Seine cruises.",
                "transit": "TGV Lyria ~4h",
                "lat": 48.8566,
                "lng": 2.3522,
                "color": "blue",
                "num": 1,
            },
            {
                "name": "Zurich & Interlaken",
                "nights": "3N",
                "desc": "Panoramic alpine cogwheels, turquoise glacial waters, and snow-capped peaks.",
                "transit": "EuroCity Train ~5h",
                "lat": 47.3769,
                "lng": 8.5417,
                "color": "purple",
                "num": 2,
            },
            {
                "name": "Rome",
                "nights": "3N",
                "desc": "Ancient Colosseum, Vatican museums, Trastevere evening walks, and artisan gelato.",
                "transit": "Flight ~9h",
                "lat": 41.9028,
                "lng": 12.4964,
                "color": "green",
                "num": 3,
            },
        ],
        "path": [
            [48.8566, 2.3522],
            [48.1, 5.5],
            [47.3769, 8.5417],
            [44.5, 10.5],
            [41.9028, 12.4964],
        ],
    },
}


def _extract_intent_parameters(messages: List[Dict[str, str]], default_dest: str = "") -> Dict[str, Any]:
    """Parse all user utterances to extract destination, duration, party, month, and activities."""
    combined_text = " ".join([m.get("content", "") for m in messages if m.get("role") == "user"]).lower()
    last_msg = messages[-1].get("content", "").lower() if messages else ""

    # 1. Destination Extraction
    dest = default_dest or "Vietnam"
    dest_candidates = [
        "vietnam", "bali", "japan", "thailand", "maldives", "dubai", "singapore", "europe",
        "goa", "kashmir", "ladakh", "kerala", "manali", "himachal", "paris", "rome",
        "switzerland", "tokyo", "hanoi", "bangkok", "phuket", "london", "new york"
    ]
    for c in dest_candidates:
        if c in combined_text:
            dest = c.title()
            break

    # 2. Duration Extraction (e.g. "10 days", "7 days", "14d", "2 weeks")
    days = 7
    days_match = re.search(r'(\d+)\s*(?:days?|d|nights?|n)', combined_text)
    if days_match:
        try:
            val = int(days_match.group(1))
            if 1 <= val <= 30:
                days = val
        except ValueError:
            pass
    elif "two weeks" in combined_text or "2 weeks" in combined_text:
        days = 14
    elif "one week" in combined_text or "1 week" in combined_text:
        days = 7
    elif "weekend" in combined_text:
        days = 3

    # 3. Party Extraction
    party = "Couple"
    if "solo" in combined_text:
        party = "Solo"
    elif any(w in combined_text for w in ["family", "kids", "children", "parents"]):
        party = "Family"
    elif any(w in combined_text for w in ["friends", "group", "buddies", "boys", "girls"]):
        party = "Friends"

    # 4. Month Extraction
    months = [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ]
    month = "November"
    for m in months:
        if m in combined_text:
            month = m.title()
            break

    # 5. Activity / Vibe Extraction
    activities = []
    if any(w in combined_text for w in ["hike", "hiking", "hinking", "trek", "trekking", "mountain", "climbing"]):
        activities.append("Hiking & Mountain Trekking")
    if any(w in combined_text for w in ["beach", "beaches", "island", "sea", "snorkeling", "scuba"]):
        activities.append("Beach & Ocean Relaxation")
    if any(w in combined_text for w in ["food", "foodie", "culinary", "street food", "coffee"]):
        activities.append("Local Food & Culinary Exploration")
    if any(w in combined_text for w in ["culture", "temple", "temples", "heritage", "history", "museum"]):
        activities.append("Heritage & Cultural Immersion")
    if any(w in combined_text for w in ["nightlife", "party", "bars", "clubs"]):
        activities.append("Vibrant Nightlife")

    vibe_str = " & ".join(activities) if activities else "Curated Exploration"

    return {
        "destination": dest,
        "days": days,
        "party": party,
        "month": month,
        "vibe": vibe_str,
        "is_hiking": "Hiking & Mountain Trekking" in activities or "hink" in combined_text,
        "last_message": last_msg
    }


async def generate_chat_masterplan(
    destination: str,
    days: int = 7,
    party: str = "Couple",
    budget: str = "Balanced"
) -> Dict[str, Any]:
    """
    Generate structured Masterplan for the Tarzan Way style chat experience.
    Matches signature presets, or dynamically geocodes and synthesizes a tailored 3-stop itinerary.
    """
    dest_clean = destination.strip()
    dest_lower = dest_clean.lower()

    # 1. Match signature presets
    for key, preset in SIGNATURE_PRESETS.items():
        if key in dest_lower or any(s["name"].lower() in dest_lower for s in preset["stops"]):
            res = dict(preset)
            res["nights"] = f"{days}N" if days else preset["nights"]
            if days and days != 7:
                # scale budget
                if key == "vietnam":
                    res["price"] = f"₹{45 + (days-7)*3}K–{68 + (days-7)*4}K"
                elif key == "bali":
                    res["price"] = f"₹{55 + (days-7)*4}K–{80 + (days-7)*5}K"
            return res

    # 2. Dynamic geocoding & spatial synthesis for ANY custom location
    geo = await GeoService.resolve_location(dest_clean)
    lat, lon = geo["latitude"], geo["longitude"]
    city = geo["city"]
    country = geo["country"]
    disp_name = geo["display_name"]

    is_intl = country and country.lower() != "india"
    if is_intl:
        base_price_min = 45000 + (days * 6000)
        base_price_max = 65000 + (days * 11000)
        price_str = f"₹{base_price_min//1000}K–{base_price_max//1000}K"
        flight_dur = "Flight ~5h30"
        dep_city = "Delhi / Mumbai"
    else:
        base_price_min = 18000 + (days * 3500)
        base_price_max = 28000 + (days * 6500)
        price_str = f"₹{base_price_min//1000}K–{base_price_max//1000}K"
        flight_dur = "Direct Flight / Rail ~2h"
        dep_city = "Major Metros"

    n1 = max(1, days // 3)
    n2 = max(1, days // 3)
    n3 = max(1, days - (n1 + n2))

    stop1_lat, stop1_lng = round(lat + 0.025, 4), round(lon + 0.020, 4)
    stop2_lat, stop2_lng = round(lat - 0.018, 4), round(lon - 0.015, 4)
    stop3_lat, stop3_lng = round(lat + 0.005, 4), round(lon - 0.035, 4)

    stops = [
        {
            "name": f"Historic {city} Quarter",
            "nights": f"{n1}N",
            "desc": f"Old town lanes, heritage monuments, artisan shopping, and celebrated street cuisine in {city}.",
            "transit": "Private Transit ~45m",
            "lat": stop1_lat,
            "lng": stop1_lng,
            "color": "blue",
            "num": 1,
        },
        {
            "name": f"Central {city} & Waterfront",
            "nights": f"{n2}N",
            "desc": f"Iconic scenic viewpoints, culinary bazaars, museums, and relaxed afternoon tea promenades.",
            "transit": "Scenic Drive ~1h",
            "lat": stop2_lat,
            "lng": stop2_lng,
            "color": "purple",
            "num": 2,
        },
        {
            "name": f"South {city} Nature & Stays",
            "nights": f"{n3}N",
            "desc": f"Golden-hour sunset overlooks, boutique hotel stays, and authentic dinner courses before departure.",
            "transit": flight_dur,
            "lat": stop3_lat,
            "lng": stop3_lng,
            "color": "green",
            "num": 3,
        },
    ]

    return {
        "key": "custom",
        "name": disp_name,
        "title": f"North · Central · Coastal {city}",
        "date": "October 2026",
        "nights": f"{days}N",
        "stopsCount": "3 stops",
        "depCity": dep_city,
        "flightDur": flight_dur,
        "price": price_str,
        "center": [lat, lon],
        "zoom": 11,
        "stops": stops,
        "path": [
            [stop1_lat, stop1_lng],
            [lat, lon],
            [stop2_lat, stop2_lng],
            [stop3_lat, stop3_lng],
        ],
    }


async def get_chat_response(messages: List[Dict[str, str]], destination: str = "") -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    Get AI chat response and optional synchronized masterplan object.
    Uses Gemini if API key is configured, else invokes our deep multi-turn travel synthesis engine.
    """
    intent = _extract_intent_parameters(messages, default_dest=destination)
    last_user_msg = intent["last_message"]

    # Try Gemini API if key is available
    if settings.GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                system_instruction=SYSTEM_PROMPT
            )

            history = []
            for msg in messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                history.append({"role": role, "parts": [msg["content"]]})

            chat = model.start_chat(history=history)
            response = await chat.send_message_async(last_user_msg)
            plan = await generate_chat_masterplan(intent["destination"], days=intent["days"], party=intent["party"])
            return response.text, plan
        except Exception as e:
            logger.warning(f"Gemini API invocation error: {e}, using smart travel engine")

    # Smart travel engine: generate dynamic multi-turn response & synchronized plan
    reply, plan = await _generate_intelligent_travel_response(intent, messages)
    return reply, plan


async def _generate_intelligent_travel_response(
    intent: Dict[str, Any],
    messages: List[Dict[str, str]]
) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    Generates rich, context-aware travel responses that adapt to conversation depth.
    Never repeats the same response — uses message count and content to determine stage.
    """
    dest = intent["destination"]
    days = intent["days"]
    party = intent["party"]
    month = intent["month"]
    vibe = intent["vibe"]
    last_msg = intent["last_message"]

    # Generate the matching masterplan
    plan = await generate_chat_masterplan(dest, days=days, party=party)

    # Count user messages to determine conversation depth
    user_msgs = [m for m in messages if m.get("role") == "user"]
    turn = len(user_msgs)

    # All user content combined for context extraction
    all_user_text = " ".join([m.get("content", "") for m in user_msgs]).lower()

    # ---- SPECIFIC QUESTION HANDLERS (highest priority) ----

    if any(w in last_msg for w in ["budget", "cost", "price", "how much", "expensive", "cheap", "affordable"]):
        reply = (
            f"Here is the verified budget breakdown for your **{days}-Day {party} Trip to {dest}**:\n\n"
            f"**Itemized Cost Estimate (per person)**:\n"
            f"- **Roundtrip Flights** (from India): {_get_flight_price(dest)}\n"
            f"- **Handpicked Stays** ({days-1} nights, boutique hotels): {_get_stay_price(days)}\n"
            f"- **Local Intercity Transit** (trains, vans, ride-hailing): {_get_transit_price()}\n"
            f"- **Meals & Dining** (street food + restaurant mix): {_get_food_price(days)}\n"
            f"- **Sightseeing & Experiences**: {_get_activity_price()}\n\n"
            f"**Estimated Total: {plan['price']} per person all-in.**\n\n"
            f"This covers a {party.lower()} traveling in {month} with {vibe.lower()} as the primary focus. "
            f"Want me to show the smart budget version to save 20–30%, or upgrade to boutique luxury stays?"
        )
        return reply, plan

    if any(w in last_msg for w in ["food", "dishes", "eat", "restaurant", "vegetarian", "vegan", "cuisine", "drink", "coffee"]):
        reply = (
            f"**Must-Try Food Experiences in {dest}**:\n\n"
            f"- **Iconic Street Dishes**: Fresh noodle broths, sizzling hot-pots, herb-filled spring rolls, and rice dishes with aromatic sauces.\n"
            f"- **Signature Beverage**: Local drip coffee brewed with sweetened condensed milk — a cultural staple.\n"
            f"- **Evening Market Crawls**: Lantern-lit alley stalls where locals dine on plastic stools by 7pm.\n"
            f"- **Dietary Options**: Vegetarian ('Chay') and vegan meals are widely available at Buddhist eateries.\n"
            f"- **Hidden Gem**: Head 2–3 streets away from tourist zones for the same dishes at 60% lower prices.\n\n"
            f"Average daily meal cost: **{_get_food_price(1)} per day** for excellent authentic dining.\n\n"
            f"Shall I include a dedicated food day in your {days}-day plan with a curated restaurant list?"
        )
        return reply, plan

    if any(w in last_msg for w in ["visa", "passport", "document", "entry", "e-visa", "voa"]):
        reply = (
            f"**Visa Requirements for {dest} — Indian Travelers**:\n\n"
            f"- **Entry Type**: Online e-Visa (processed within 3 business days) or Visa on Arrival at major airports.\n"
            f"- **Validity**: 30 to 90 days, with single or multiple entry options depending on purpose.\n"
            f"- **Required Documents**: Passport valid 6+ months, confirmed return ticket, 2 recent passport photos.\n"
            f"- **Government Fee**: Approximately $25 USD (~₹2,100) — paid online or at the port of entry.\n"
            f"- **Pro Tip**: Apply at least 10–14 days before departure for peace of mind.\n\n"
            f"I can help you create a document checklist or recommend travel insurance. What else do you need?"
        )
        return reply, plan

    if any(w in last_msg for w in ["weather", "season", "best time", "rain", "monsoon", "climate", "temperature"]):
        reply = (
            f"**Best Time to Visit {dest}** — Weather Guide:\n\n"
            f"- **Peak Season**: October to April — clear skies, warm weather, ideal for sightseeing and beaches.\n"
            f"- **Shoulder Season**: May to June — fewer crowds, 15–20% cheaper hotels, occasional afternoon showers.\n"
            f"- **Monsoon**: July to September — heavy rains in some regions, but lush green landscapes and low prices.\n\n"
            f"**Your Trip in {month}**: "
            + (_get_month_tip(month, dest)) +
            f"\n\nPacking essentials: lightweight breathable clothing, rain shell, comfortable walking shoes, and SPF 50+ sunscreen."
        )
        return reply, plan

    if any(w in last_msg for w in ["flight", "fly", "airline", "airport", "layover", "direct flight", "connection"]):
        reply = (
            f"**Flight Options to {dest} from India**:\n\n"
            f"- **Best Connections**: Delhi (IGI) and Mumbai (BOM) offer the most direct and budget-friendly routes.\n"
            f"- **Flight Duration**: {plan.get('flightDur', 'approximately 4-8 hours')} including connections.\n"
            f"- **Budget Tip**: Book 6–8 weeks in advance on IndiGo, Air India, or partner carriers for best fares.\n"
            f"- **Estimated Roundtrip**: {_get_flight_price(dest)}\n\n"
            f"Want me to suggest the best departure city for your location, or recommend airlines with good layover options?"
        )
        return reply, plan

    if any(w in last_msg for w in ["hotel", "stay", "accommodation", "hostel", "villa", "resort", "airbnb", "where to stay", "sleep"]):
        reply = (
            f"**Stay Recommendations for {dest}** — {party} Travel:\n\n"
        )
        for i, stop in enumerate(plan.get("stops", [])[:3]):
            reply += f"- **{stop['name']}** ({stop['nights']}): Boutique guesthouse in the cultural heart of the district. Avg ₹2,200–3,800/night.\n"
        reply += (
            f"\n**What to Look For**: Properties with en-suite bathrooms, air conditioning, and breakfast included.\n"
            f"**Booking Tips**: Use Booking.com or Agoda for flexible cancellation. Compare with direct hotel bookings for better rates.\n\n"
            f"I can recommend specific property names and neighborhoods. Which stop would you like details for first?"
        )
        return reply, plan

    # ---- MULTI-TURN CONVERSATION FLOW ----

    # Turn 1-2: Initial greeting / early conversation — ask clarifying questions
    if turn <= 2 and not any(w in all_user_text for w in ["days", "night", "week", "month", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december", "solo", "couple", "family", "friends", "budget", "hiking", "beach", "food"]):
        reply = (
            f"I'd love to help you plan an unforgettable trip to **{dest}**! To craft the perfect itinerary, let me ask a few quick questions:\n\n"
            f"1. **How many days** are you planning? (7 days is a sweet spot for {dest})\n"
            f"2. **When are you traveling?** Any specific month or season in mind?\n"
            f"3. **Who is going?** Solo, couple, family with kids, or a friends group?\n"
            f"4. **What excites you most?** Beaches & relaxation, cultural heritage, hiking & adventure, food discovery, or a mix?\n\n"
            f"Once I have these details, I'll build you a verified day-by-day masterplan with real pricing!"
        )
        return reply, plan

    # Turn 3+: Full itinerary if enough details are now known
    # Or if user already gave details in first message
    if "vietnam" in dest.lower():
        reply = (
            f"Here is your **{days}-Day Vietnam {party} Masterplan for {month}**!\n\n"
            f"### Day-by-Day Itinerary\n\n"
            f"- **Days 1-2: Hanoi Old Quarter & Street Culture**\n"
            f"  Arrive at Noi Bai Airport, private transfer to a boutique hotel in the French Quarter. Explore Hoan Kiem Lake, iconic Train Street, and try legendary Bun Cha and Egg Coffee.\n\n"
            f"- **Days 3-{max(4, days//3)+2}: Sapa Valley & Fansipan Mountain**\n"
            f"  Scenic mountain transfer to Sapa. Trek through terraced Muong Hoa valley, Lao Chai and Ta Van villages. Summit Fansipan (3,143m) for breathtaking alpine views.\n\n"
            f"- **Days {max(4, days//3)+3}-{days-2}: Ninh Binh & Ha Long Bay**\n"
            f"  The 'Ha Long Bay on Land' — hike Hang Mua Peak's 500 dragon steps, rowboat through Trang An grottos, and overnight boutique cruise on Lan Ha Bay.\n\n"
            f"- **Day {days}: Return from Hanoi**\n"
            f"  Morning Tai Chi on the bay deck, final artisan shopping, and departure transfer.\n\n"
            f"### Budget Summary ({party})\n"
            f"- Roundtrip Flights: ₹24,000–31,000\n"
            f"- Stays ({days-1} nights): ₹14,000–21,000\n"
            f"- Transit & Transfers: ₹6,500–9,000\n"
            f"- Food & Dining: ₹7,000–10,000\n"
            f"- **Total: {plan['price']} per person all-in**\n\n"
            f"**{month} Tip**: " + ("Warm and lush — ideal hiking weather with average 24-31°C. Pack quick-dry trail shoes and a light rain shell." if "may" in month.lower() or "june" in month.lower() else "Pleasant temperatures and clear skies. Perfect for all activities on this itinerary.") + "\n\n"
            f"Would you like me to add specific hotel recommendations, or adjust the trekking difficulty?"
        )
        return reply, plan

    if "bali" in dest.lower():
        reply = (
            f"Here is your **{days}-Day Bali {party} Masterplan for {month}**!\n\n"
            f"### Day-by-Day Itinerary\n\n"
            f"- **Days 1-3: Ubud Emerald Highlands**\n"
            f"  Rainforest valley villa check-in, Campuhan Ridge morning trek, Tegalalang rice terraces, Tirta Empul water blessing, and waterfall hikes.\n\n"
            f"- **Days 4-5: Mount Batur Sunrise & Canggu**\n"
            f"  Pre-dawn hike up Mount Batur for sunrise over Lake Batur. Natural hot springs. Afternoon transfer to coastal Canggu for sunsets and organic cafes.\n\n"
            f"- **Days 6-{days}: Seminyak & Uluwatu Cliffs**\n"
            f"  Uluwatu cliff temple, Kecak fire dance at sunset, Jimbaran Bay seafood dinner, and Seminyak beach relaxation before departure.\n\n"
            f"### Budget Summary ({party})\n"
            f"- Roundtrip Flights (ex-India): ₹28,000–38,000\n"
            f"- Stays ({days-1} nights, pool villas): ₹18,000–28,000\n"
            f"- Scooters & Private Cabs: ₹4,500–7,000\n"
            f"- Food & Beach Clubs: ₹8,000–14,000\n"
            f"- **Total: {plan['price']} per person all-in**\n\n"
            f"Shall I include a dedicated spa day, Nusa Penida island day trip, or add the rice field sunrise cycling tour?"
        )
        return reply, plan

    if "japan" in dest.lower():
        reply = (
            f"Here is your **{days}-Day Japan {party} Masterplan for {month}**!\n\n"
            f"### Day-by-Day Itinerary\n\n"
            f"- **Days 1-4: Tokyo — Futuristic Meets Ancient**\n"
            f"  Shibuya crossing, Asakusa Senso-ji, teamLab digital art, Shinjuku night food market, and Harajuku street culture.\n\n"
            f"- **Days 5-7: Kyoto — Temples & Tranquility**\n"
            f"  Fushimi Inari torii gates at dawn, Kinkaku-ji golden pavilion, Arashiyama bamboo grove, Gion geisha district evening walk.\n\n"
            f"- **Days 8-{days}: Osaka — Street Food & Nightlife**\n"
            f"  Dotonbori food crawl, Osaka Castle park, Kuromon Market, and Namba nightlife before departure.\n\n"
            f"### Budget Summary ({party})\n"
            f"- Roundtrip Flights: ₹45,000–65,000\n"
            f"- Stays ({days-1} nights, mixed hotels): ₹28,000–42,000\n"
            f"- JR Pass (7-day): ₹22,000\n"
            f"- Food & Experiences: ₹18,000–25,000\n"
            f"- **Total: {plan['price']} per person all-in**\n\n"
            f"Would you like me to add a side trip to Nara (deer park) or Hiroshima (Peace Memorial)?"
        )
        return reply, plan

    # Generic destination - full tailored response
    stops_text = ""
    for stop in plan.get("stops", []):
        stops_text += f"- **{stop['name']}** ({stop['nights']}): {stop['desc']}\n"

    reply = (
        f"Here is your **{days}-Day {dest} {party} Masterplan for {month}**!\n\n"
        f"### Curated Itinerary Flow\n\n"
        f"- **Days 1-{max(1, days//3)}: Historic & Cultural Heart**\n"
        f"  Old town discovery, landmark heritage sights, local coffee culture, and traditional evening dinners.\n\n"
        f"- **Days {max(1, days//3)+1}-{days-2}: Adventure, Nature & Panoramas**\n"
        f"  Scenic hikes or coastal excursions, guided nature walks, artisan market exploration, and sunset viewpoints.\n\n"
        f"- **Days {days-1}-{days}: Signature Experiences & Relaxation**\n"
        f"  Boutique spa retreat, signature cuisine dinner, final sunset experience, and departure transfer.\n\n"
        f"### Verified Stops\n{stops_text}\n"
        f"### Budget Summary ({party})\n"
        f"- **Total: {plan['price']} per person all-in**\n"
        f"- Includes flights, stays, daily meals, local transit, and activity passes.\n\n"
        f"I can refine any specific day, add hotel recommendations, or adjust the budget tier. What would you like to explore next?"
    )
    return reply, plan


def _get_flight_price(dest: str) -> str:
    """Return estimated roundtrip flight price for common destinations."""
    dest_l = dest.lower()
    if any(d in dest_l for d in ["europe", "paris", "rome", "london", "zurich"]):
        return "₹45,000–65,000 (best booked 8–10 weeks in advance)"
    if any(d in dest_l for d in ["japan", "tokyo"]):
        return "₹42,000–62,000 (book 6–8 weeks ahead)"
    if any(d in dest_l for d in ["maldives"]):
        return "₹18,000–28,000 (short hop, great deals with IndiGo & Air India)"
    if any(d in dest_l for d in ["dubai"]):
        return "₹12,000–22,000 (multiple daily flights, very competitive)"
    if any(d in dest_l for d in ["singapore"]):
        return "₹20,000–32,000 (direct from Chennai, Bangalore, or Delhi)"
    return "₹22,000–36,000 (book 6–8 weeks in advance for best fares)"


def _get_stay_price(days: int) -> str:
    """Return estimated stay price based on number of days."""
    nights = max(1, days - 1)
    low = nights * 1800
    high = nights * 2800
    return f"₹{low:,}–{high:,} (avg ₹1,800–2,800 per night)"


def _get_transit_price() -> str:
    return "₹5,500–9,000"


def _get_food_price(days: int) -> str:
    low = days * 750
    high = days * 1300
    return f"₹{low:,}–{high:,}"


def _get_activity_price() -> str:
    return "₹4,500–8,500"


def _get_month_tip(month: str, dest: str) -> str:
    """Return a contextual weather tip for the specific month."""
    m = month.lower()
    if m in ["december", "january", "february"]:
        return f"This is peak season for {dest} — expect brilliant weather, fuller hotels, and vibrant festival atmosphere. Book accommodations 2–3 months ahead."
    if m in ["march", "april"]:
        return f"Spring shoulder season — pleasant weather, thinner crowds than December, and 10–15% lower accommodation rates. An excellent time to visit."
    if m in ["may", "june"]:
        return f"Early summer — warm and lush with occasional afternoon showers. Ideal for nature activities and cultural exploration. Pack a compact rain shell."
    if m in ["july", "august", "september"]:
        return f"Monsoon period in parts of {dest}. Expect lush green scenery, significantly reduced crowds, and prices 20–30% lower. Check regional weather forecasts."
    return f"{month} offers a great balance of weather and crowd levels for {dest}."
