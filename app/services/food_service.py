import logging
from typing import Dict, Any, List, Optional
from app.models.schemas import FoodQuery

logger = logging.getLogger("voyage.food")

FOOD_KNOWLEDGE_BASE = {
    "rome": {
        "culinary_tradition": "Classic Roman Cucina Povera (Rich, seasonal, rustic pasta & charcuterie)",
        "signature_dishes": [
            {
                "name": "Carbonara Autentica",
                "pronunciation": "kahr-boh-NAH-rah",
                "type": "Primi (Pasta)",
                "price_range": "€12 - €16",
                "description": "Al dente rigatoni or spaghetti coated in silky egg yolks, crispy Guanciale (cured pork cheek), and sharp Pecorino Romano cheese with coarse black pepper. (Never heavy cream).",
                "dietary": ["Contains Pork", "Contains Dairy", "Contains Gluten", "Egg-based"],
                "must_try_spot": "Trattoria Da Enzo al 29 (Trastevere)",
                "image_tag": "pasta"
            },
            {
                "name": "Cacio e Pepe",
                "pronunciation": "KAH-choh eh PEH-peh",
                "type": "Primi (Pasta)",
                "price_range": "€10 - €14",
                "description": "Pure Roman alchemy using only three ingredients: tonnarelli pasta, freshly grated aged Pecorino Romano, and toasted freshly cracked black pepper emulsified into a creamy emulsion.",
                "dietary": ["Vegetarian", "Contains Dairy", "Contains Gluten"],
                "must_try_spot": "Felice a Testaccio",
                "image_tag": "pasta"
            },
            {
                "name": "Supplì al Telefono",
                "pronunciation": "soop-PLEE",
                "type": "Street Food / Antipasti",
                "price_range": "€2 - €4",
                "description": "Crispy fried rice croquette filled with rich tomato meat ragù and a melting mozzarella center that stretches like a telephone cord when pulled apart.",
                "dietary": ["Contains Dairy", "Contains Gluten", "Contains Meat"],
                "must_try_spot": "Supplizio Roma",
                "image_tag": "snack"
            },
            {
                "name": "Artisanal Gelato (Pistacchio & Stracciatella)",
                "pronunciation": "jeh-LAH-toh",
                "type": "Dessert",
                "price_range": "€3 - €6",
                "description": "Dense, naturally flavored Italian ice cream churned slowly without artificial coloring or puffed air.",
                "dietary": ["Vegetarian", "Contains Dairy", "Gluten-Free Options Available"],
                "must_try_spot": "Frigidarium or Giolitti",
                "image_tag": "dessert"
            }
        ],
        "street_food_tips": [
            "Order pizza 'al taglio' (by the slice and weight) for quick, delicious on-the-go lunches.",
            "Never order a cappuccino after 11:00 AM if you want to drink like a true local; opt for an espresso ('un caffè') at the bar."
        ],
        "dietary_friendliness": {
            "vegetarian": "Very High (Cacio e Pepe, Pizza Margherita, Carciofi alla Giudia)",
            "vegan": "High (Pizza Marinara, Pasta all'Arrabbiata)",
            "gluten_free": "Exceptional (AIC-certified gluten-free trattorias across Rome)",
            "halal": "Available (Certified lamb & kebab bistros near Termini & Esquilino)"
        }
    },
    "tokyo": {
        "culinary_tradition": "Washoku (UNESCO Heritage: Seasonality, Umami balance, precision knife craftsmanship)",
        "signature_dishes": [
            {
                "name": "Edomae Nigiri Sushi",
                "pronunciation": "SOO-shee",
                "type": "Main",
                "price_range": "¥2,500 - ¥15,000",
                "description": "Freshly sliced seasonal ocean fish (Toro, Uni, Shime-saba) delicately pressed over warm vinegared Akazu sushi rice with a touch of freshly grated wasabi.",
                "dietary": ["Contains Seafood", "Gluten-Free (request Tamari soy sauce)"],
                "must_try_spot": "Sushi Dai (Toyosu) or Manten Sushi (Marunouchi)",
                "image_tag": "sushi"
            },
            {
                "name": "Tonkotsu & Shoyu Ramen",
                "pronunciation": "RAH-men",
                "type": "Main",
                "price_range": "¥900 - ¥1,400",
                "description": "Springy wheat noodles in a 16-hour rich pork bone or savory soy broth topped with melt-in-mouth chashu pork, seasoned ajitama soft-boiled egg, and nori seaweed.",
                "dietary": ["Contains Pork", "Contains Gluten", "Egg-based"],
                "must_try_spot": "Afuri (Yuzu Shoyu) or Ichiran Shibuya",
                "image_tag": "ramen"
            },
            {
                "name": "A5 Wagyu Sukiyaki / Yakiniku",
                "pronunciation": "soo-kee-YAH-kee",
                "type": "Fine Dining",
                "price_range": "¥6,000 - ¥18,000",
                "description": "Heavily marbled Japanese black beef gently simmered in sweet dashi soy broth and dipped into whisked fresh raw egg for ultimate richness.",
                "dietary": ["Contains Beef", "Halal Wagyu Certified venues available in Ginza"],
                "must_try_spot": "Ningyocho Imahan",
                "image_tag": "meat"
            },
            {
                "name": "Matcha Parfait & Warabi Mochi",
                "pronunciation": "MAH-chah",
                "type": "Dessert / Tea",
                "price_range": "¥800 - ¥1,600",
                "description": "Ceremonial grade Uji green tea gelato layered with kinako soybean powder, adzuki red bean, and chewy bracken starch mochi.",
                "dietary": ["Vegetarian", "Dairy", "Gluten-Free"],
                "must_try_spot": "Suzukien Asakusa (7 intensity levels of Matcha)",
                "image_tag": "dessert"
            }
        ],
        "street_food_tips": [
            "In Japan, walking while eating is generally frowned upon; enjoy your snack right near the vendor stall before moving on.",
            "Slurping noodles loudly is considered a compliment to the chef and aerates the hot broth for fuller flavor."
        ],
        "dietary_friendliness": {
            "vegetarian": "Moderate (Look for Shojin Ryori Buddhist temple cuisine)",
            "vegan": "Growing (T's Tantan vegan ramen in Tokyo Station is legendary)",
            "gluten_free": "Moderate (Carry a Japanese celiac card due to ubiquitous soy sauce)",
            "halal": "High in major hubs (Halal Ramen Ouka, Halal Wagyu Panga)"
        }
    }
}

class FoodService:
    @staticmethod
    def get_city_gastronomy(query: FoodQuery) -> Dict[str, Any]:
        dest_clean = query.city.strip().lower()

        if dest_clean in FOOD_KNOWLEDGE_BASE:
            data = FOOD_KNOWLEDGE_BASE[dest_clean]
        else:
            data = FoodService._synthesize_food_profile(query.city)

        dishes = data.get("signature_dishes", [])
        if query.dietary_preferences:
            filtered = []
            for d in dishes:
                diet_tags = [tag.lower() for tag in d.get("dietary", [])]
                matches_all = True
                for pref in query.dietary_preferences:
                    pref_l = pref.lower()
                    if pref_l in ["vegetarian", "vegan", "gluten-free", "halal"]:
                        if not any(pref_l in tag for tag in diet_tags) and not any(pref_l in str(d).lower() for _ in [1]):
                            matches_all = False
                if matches_all or len(filtered) < 2:
                    filtered.append(d)
            if filtered:
                dishes = filtered

        return {
            "status": "success",
            "city": query.city.title(),
            "culinary_tradition": data["culinary_tradition"],
            "total_dishes_featured": len(dishes),
            "signature_dishes": dishes,
            "street_food_tips": data["street_food_tips"],
            "dietary_breakdown": data["dietary_friendliness"],
            "foodie_rating": 9.6
        }

    @staticmethod
    def _synthesize_food_profile(city: str) -> Dict[str, Any]:
        return {
            "culinary_tradition": f"Authentic Regional Gastronomy of {city.title()} (Locally sourced produce, heritage cooking techniques, and bustling market culture)",
            "signature_dishes": [
                {
                    "name": f"Traditional {city.title()} Heritage Stew & Hearth Bread",
                    "pronunciation": f"{city.title()} speh-chee-AHL",
                    "type": "Main Course",
                    "price_range": "$14 - $22",
                    "description": "Slow-cooked seasonal vegetables and tender choice cuts in a deeply aromatic simmered herbal reduction, served with wood-fired crusty bread.",
                    "dietary": ["Hearty", "Local Specialty", "Gluten in Bread"],
                    "must_try_spot": f"Central Old Town Bistro & Tavern in {city.title()}",
                    "image_tag": "meat"
                },
                {
                    "name": "Artisanal Street Pastry & Spiced Delicacy",
                    "pronunciation": "dohl-CHEE-toh",
                    "type": "Street Food / Sweet",
                    "price_range": "$3 - $6",
                    "description": "Crisp flaky pastry shell dusted with spiced sugars, infused with regional fruit compote or creamy custard.",
                    "dietary": ["Vegetarian", "Contains Dairy", "Contains Gluten"],
                    "must_try_spot": "Old Market Square Bakeries",
                    "image_tag": "snack"
                }
            ],
            "street_food_tips": [
                "Seek out food stalls where local residents and workers queue during noon lunch hour.",
                "Always ask for the regional house beverage or freshly pressed local fruit press."
            ],
            "dietary_friendliness": {
                "vegetarian": "High (Fresh farm-to-table salads, cheeses, roasted grains)",
                "vegan": "Moderate (Legume dishes and roasted vegetable platters)",
                "gluten_free": "Moderate (Rice and grilled meat dishes widely accessible)",
                "halal": "Accessible (Inquire at Mediterranean and Turkish district eateries)"
            }
        }
