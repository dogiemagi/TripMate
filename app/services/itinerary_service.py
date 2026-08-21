import logging
from typing import Dict, Any, List
from app.models.schemas import ItineraryRequest

logger = logging.getLogger("voyage.itinerary")

CITY_ITINERARY_TEMPLATES = {
    "tokyo": [
        {
            "day": 1,
            "theme": "Historic Traditions & Futuristic Neon",
            "highlight": "Senso-ji Temple & Shibuya Sky Crossing",
            "activities": [
                {"time": "08:30 AM", "title": "Senso-ji Temple & Asakusa Nakamise", "category": "Culture", "duration": "2.5 hrs", "cost": "Free", "lat": 35.7147, "lon": 139.7967, "desc": "Tokyo's oldest Buddhist temple. Stroll through the iconic Kaminarimon gate and sample fresh ningyo-yaki sweets."},
                {"time": "12:00 PM", "title": "Tsukiji Outer Market Culinary Walk", "category": "Food", "duration": "2 hrs", "cost": "$25", "lat": 35.6655, "lon": 139.7706, "desc": "Savor flame-seared wagyu beef skewers, tamagoyaki omelet, and fresh king crab legs."},
                {"time": "03:00 PM", "title": "teamLab Planets Immersive Digital Art", "category": "Art", "duration": "2 hrs", "cost": "$30", "lat": 35.6517, "lon": 139.7891, "desc": "Wade through water and walk through infinite crystal mirrors in Toyosu."},
                {"time": "06:30 PM", "title": "Shibuya Sky Sunset & Scramble Crossing", "category": "Nightlife", "duration": "2.5 hrs", "cost": "$18", "lat": 35.6580, "lon": 139.7016, "desc": "360-degree open-air glass rooftop observatory overlooking Tokyo's kinetic pulse."}
            ]
        },
        {
            "day": 2,
            "theme": "Pop Culture, Shrines & Haute Cuisine",
            "highlight": "Meiji Jingu & Harajuku Takeshita Street",
            "activities": [
                {"time": "09:00 AM", "title": "Meiji Jingu Shrine & Yoyogi Forest", "category": "Nature & Culture", "duration": "2 hrs", "cost": "Free", "lat": 35.6764, "lon": 139.6993, "desc": "Peaceful tranquil cedar forest in the heart of metropolitan Tokyo."},
                {"time": "11:30 AM", "title": "Takeshita Street & Omotesando Architecture", "category": "Shopping", "duration": "2.5 hrs", "cost": "$20", "lat": 35.6702, "lon": 139.7027, "desc": "Trendy boutique fashion, artisan matcha cafes, and tree-lined luxury avenues."},
                {"time": "02:30 PM", "title": "Shinjuku Gyoen National Garden", "category": "Relaxation", "duration": "2 hrs", "cost": "$4", "lat": 35.6852, "lon": 139.7101, "desc": "Splendid traditional Japanese landscaped garden with tea houses."},
                {"time": "07:00 PM", "title": "Omoide Yokocho & Golden Gai Izakayas", "category": "Gastronomy", "duration": "3 hrs", "cost": "$40", "lat": 35.6938, "lon": 139.7003, "desc": "Historic atmospheric alleyways packed with intimate 6-seat yakitori bars."}
            ]
        },
        {
            "day": 3,
            "theme": "Anime Capital & Skyline Vistas",
            "highlight": "Akihabara Electric Town & Roppongi Hills",
            "activities": [
                {"time": "10:00 AM", "title": "Akihabara Tech & Retro Gaming District", "category": "Entertainment", "duration": "3 hrs", "cost": "$15", "lat": 35.6983, "lon": 139.7731, "desc": "Multi-floor arcades, vintage electronics, collectibles, and theme cafes."},
                {"time": "02:00 PM", "title": "Imperial Palace East Gardens", "category": "History", "duration": "2 hrs", "cost": "Free", "lat": 35.6852, "lon": 139.7528, "desc": "Ancient Edo Castle stone walls, moats, and pristine manicured bonsai."},
                {"time": "05:30 PM", "title": "Mori Art Museum & Roppongi Observation Deck", "category": "Art", "duration": "2.5 hrs", "cost": "$16", "lat": 35.6605, "lon": 139.7292, "desc": "Cutting-edge contemporary art with iconic Tokyo Tower night views."},
                {"time": "08:30 PM", "title": "Ginza Michelin Ramen or Kaiseki Dinner", "category": "Food", "duration": "2 hrs", "cost": "$55", "lat": 35.6719, "lon": 139.7640, "desc": "Refined dining experience in Tokyo's premier luxury district."}
            ]
        }
    ],
    "paris": [
        {
            "day": 1,
            "theme": "Iconic River Seine & Classical Grandeur",
            "highlight": "Louvre Museum & Eiffel Sunset",
            "activities": [
                {"time": "09:00 AM", "title": "Louvre Museum Masterpieces", "category": "Art", "duration": "3 hrs", "cost": "$22", "lat": 48.8606, "lon": 2.3376, "desc": "Mona Lisa, Winged Victory, and majestic French crown jewels."},
                {"time": "01:00 PM", "title": "Tuileries Garden & Angelina Hot Chocolate", "category": "Food", "duration": "1.5 hrs", "cost": "$18", "lat": 48.8634, "lon": 2.3275, "desc": "Famous Parisian African hot chocolate and Mont-Blanc pastry."},
                {"time": "03:30 PM", "title": "Musée d'Orsay Impressionist Gallery", "category": "Culture", "duration": "2 hrs", "cost": "$16", "lat": 48.8599, "lon": 2.3265, "desc": "World's finest collection of Monet, Van Gogh, Renoir, and Degas."},
                {"time": "07:00 PM", "title": "Eiffel Tower Summit & Seine River Cruise", "category": "Sightseeing", "duration": "3 hrs", "cost": "$35", "lat": 48.8584, "lon": 2.2945, "desc": "Romantic illuminated cruise past Notre-Dame and glittering Eiffel sparkles."}
            ]
        },
        {
            "day": 2,
            "theme": "Bohemian Art & Gothic History",
            "highlight": "Montmartre & Sacré-Cœur Basilica",
            "activities": [
                {"time": "09:30 AM", "title": "Sacré-Cœur Basilica & Place du Tertre", "category": "Art & Views", "duration": "2.5 hrs", "cost": "Free", "lat": 48.8867, "lon": 2.3431, "desc": "Hilltop panoramic vistas over Paris and street portrait painters."},
                {"time": "01:00 PM", "title": "Le Marais Historic Mansions & Falafel", "category": "Food & Walk", "duration": "2.5 hrs", "cost": "$15", "lat": 48.8575, "lon": 2.3592, "desc": "Cobblestone alleys, vintage boutiques, and legendary L'As du Fallafel."},
                {"time": "04:30 PM", "title": "Notre-Dame Cathedral & Île de la Cité", "category": "History", "duration": "2 hrs", "cost": "Free", "lat": 48.8529, "lon": 2.3500, "desc": "Gothic masterpiece in the historic heart of Paris."},
                {"time": "07:30 PM", "title": "Saint-Germain-des-Prés Literary Cafes", "category": "Dining", "duration": "2.5 hrs", "cost": "$45", "lat": 48.8540, "lon": 2.3333, "desc": "Dine at historic haunts of Hemingway and Sartre like Café de Flore."}
            ]
        }
    ]
}

class ItineraryService:
    @staticmethod
    def generate_itinerary(req: ItineraryRequest) -> Dict[str, Any]:
        dest_clean = req.destination.split(",")[0].strip().lower()
        days_count = req.days

        if dest_clean in CITY_ITINERARY_TEMPLATES:
            base_days = CITY_ITINERARY_TEMPLATES[dest_clean]
        else:
            base_days = ItineraryService._synthesize_generic_itinerary(req.destination, days_count, req.travel_style)

        generated_days = []
        for d in range(1, days_count + 1):
            source_idx = (d - 1) % len(base_days)
            day_data = dict(base_days[source_idx])
            day_data["day"] = d
            day_data["theme"] = f"Day {d}: {day_data.get('theme', 'Exploration & Culture')}"
            generated_days.append(day_data)

        total_activities = sum(len(day["activities"]) for day in generated_days)
        estimated_daily_expense = {"Backpacker": 45, "Moderate": 120, "Premium": 280, "Luxury": 650}.get(req.budget_level, 120)

        return {
            "status": "success",
            "destination": req.destination.title(),
            "total_days": days_count,
            "travel_style": req.travel_style,
            "pace": req.pace,
            "budget_tier": req.budget_level,
            "estimated_total_cost_usd": estimated_daily_expense * days_count,
            "summary": {
                "total_curated_spots": total_activities,
                "recommended_transit_pass": "Unlimited Metro / Rail 3-Day Pass",
                "smart_tip": f"For a {req.pace.lower()} pace in {req.destination}, cluster your morning activities within the historic core and save scenic panoramic decks for golden hour."
            },
            "days": generated_days
        }

    @staticmethod
    def _synthesize_generic_itinerary(destination: str, days: int, style: str) -> List[Dict[str, Any]]:
        return [
            {
                "day": 1,
                "theme": f"Historic Core & Cultural Orientation in {destination}",
                "highlight": "Old Town Discovery & Local Food Stalls",
                "activities": [
                    {"time": "09:00 AM", "title": f"{destination} Historic City Center Walk", "category": "Culture", "duration": "2.5 hrs", "cost": "Free", "lat": 37.7749, "lon": -122.4194, "desc": "Marvel at central architectural landmarks and soak in morning street life."},
                    {"time": "12:30 PM", "title": "Traditional Market Lunch Experience", "category": "Food", "duration": "1.5 hrs", "cost": "$20", "lat": 37.7850, "lon": -122.4000, "desc": "Sample signature authentic delicacies from top-rated local stalls."},
                    {"time": "03:00 PM", "title": f"Premier {destination} Art & History Museum", "category": "Museum", "duration": "2 hrs", "cost": "$15", "lat": 37.7700, "lon": -122.4100, "desc": "Explore national treasures, paintings, and heritage artifacts."},
                    {"time": "06:30 PM", "title": "Sunset Viewpoint & Twilight Dinner", "category": "Relaxation", "duration": "2.5 hrs", "cost": "$35", "lat": 37.7600, "lon": -122.4200, "desc": "Unwind with panoramic city sunset views and craft beverages."}
                ]
            },
            {
                "day": 2,
                "theme": f"Hidden Gems, Artisan Neighborhoods & Waterfront",
                "highlight": "Scenic Promenade & Evening Music Lounge",
                "activities": [
                    {"time": "09:30 AM", "title": "Botanical Gardens or Waterfront Promenade", "category": "Nature", "duration": "2 hrs", "cost": "$8", "lat": 37.7650, "lon": -122.4300, "desc": "Lush greenery, fresh breeze, and tranquil morning photography."},
                    {"time": "12:00 PM", "title": "Artisanal Cafe & Bakery Tasting", "category": "Food", "duration": "1.5 hrs", "cost": "$14", "lat": 37.7750, "lon": -122.4250, "desc": "Freshly brewed specialty coffee and regional pastries."},
                    {"time": "02:30 PM", "title": "Boutique Craft Shopping & Local Galleries", "category": "Shopping", "duration": "2.5 hrs", "cost": "$25", "lat": 37.7800, "lon": -122.4150, "desc": "Discover handmade souvenirs, ceramics, and locally designed goods."},
                    {"time": "07:30 PM", "title": "Gastronomy Tasting Menu & Rooftop Lounge", "category": "Nightlife", "duration": "3 hrs", "cost": "$50", "lat": 37.7900, "lon": -122.4050, "desc": "Celebrate the journey with chef's signature regional courses."}
                ]
            }
        ]
