import logging
from typing import Dict, Any, List, Optional
from app.models.schemas import FoodQuery

logger = logging.getLogger("voyage.food")

FOOD_KNOWLEDGE_BASE = {
    "chennai": {
        "culinary_tradition": "Authentic South Indian and Tamil Gastronomy (Crispy fermented dosas, aromatic Chettinad spices, coastal seafood curries, and iconic filter coffee)",
        "signature_dishes": [
            {
                "name": "Authentic Chettinad Pepper Chicken",
                "pronunciation": "Chettinad Kozhi",
                "type": "Main Course",
                "price_range_inr": "₹280 - ₹480",
                "price_range_usd": "$3.4 - $5.8",
                "description": "Tender country chicken simmered in freshly stone-ground roasted spices, fiery black peppercorns, curry leaves, and toasted coconut paste.",
                "dietary": ["Non-Vegetarian", "Contains Poultry", "Gluten-Free", "Halal"],
                "must_try_spot": "The Raintree (St. Mary's Road) or Anjappar",
                "image_tag": "meat"
            },
            {
                "name": "Dindigul Thalappakatti Mutton Biryani",
                "pronunciation": "Seeraga Samba Biryani",
                "type": "Signature Main",
                "price_range_inr": "₹320 - ₹550",
                "price_range_usd": "$3.8 - $6.5",
                "description": "Fragrant short-grain Seeraga Samba rice slow-cooked with succulent tender mutton, whole spices, and caramelized shallots.",
                "dietary": ["Non-Vegetarian", "Contains Mutton/Meat", "Gluten-Free", "Halal"],
                "must_try_spot": "Thalappakatti (Nungambakkam) or Buhari",
                "image_tag": "meat"
            },
            {
                "name": "Marina Beach Tawa Fried Vanjaram (Kingfish)",
                "pronunciation": "Meen Varuval",
                "type": "Seafood / Coastal",
                "price_range_inr": "₹250 - ₹450",
                "price_range_usd": "$3 - $5.5",
                "description": "Fresh catch of Kingfish marinated in spicy red chili paste, turmeric, and lemon juice, shallow-fried to crispy perfection on iron tawa.",
                "dietary": ["Non-Vegetarian", "Contains Seafood", "Gluten-Free"],
                "must_try_spot": "Marina Beach Stalls or Sea Shell Restaurant",
                "image_tag": "meat"
            },
            {
                "name": "Crispy Ghee Podi Dosa with Sambar and Chutneys",
                "pronunciation": "Ghee POH-dee DOH-sah",
                "type": "Signature Breakfast / Dinner",
                "price_range_inr": "₹90 - ₹180",
                "price_range_usd": "$1.1 - $2.2",
                "description": "Crispy golden fermented rice and lentil crepe smeared with fragrant spiced gun powder (podi) and clarified butter (ghee), served alongside piping hot drumstick sambar and a trio of fresh chutneys.",
                "dietary": ["Vegetarian", "Contains Dairy (Ghee)", "Gluten-Free"],
                "must_try_spot": "Murugan Idli Shop (T. Nagar) or Saravana Bhavan",
                "image_tag": "snack"
            },
            {
                "name": "Madras Degree Filter Coffee and Medu Vada",
                "pronunciation": "Madras Kapi",
                "type": "Beverage & Snack",
                "price_range_inr": "₹40 - ₹90",
                "price_range_usd": "$0.5 - $1.1",
                "description": "Strong, rich chicory-infused decoction frothed with boiling whole milk served in a traditional brass dabarah and tumbler, paired with crisp savory lentil donuts.",
                "dietary": ["Vegetarian", "Contains Dairy", "Gluten-Free"],
                "must_try_spot": "Rayar's Mess (Mylapore) or Madras Coffee House",
                "image_tag": "snack"
            },
            {
                "name": "Idiyappam with Coconut Milk and Veg Kurma",
                "pronunciation": "Ih-dee-YAH-pahm",
                "type": "Main Course",
                "price_range_inr": "₹110 - ₹220",
                "price_range_usd": "$1.3 - $2.7",
                "description": "Steamed delicate rice noodle hoppers served with sweet cardamom-spiced fresh coconut milk or a fragrant vegetable kurma.",
                "dietary": ["Vegan", "Gluten-Free", "Plant-Based"],
                "must_try_spot": "Mylai Karpagambal Mess",
                "image_tag": "pasta"
            }
        ],
        "street_food_tips": [
            "Visit Marina Beach in the evening for freshly fried fish and crispy sundal (tempered spiced chickpeas).",
            "Always cool and mix your Madras filter coffee by pouring between the tumbler and dabarah from a height to create signature froth."
        ],
        "dietary_friendliness": {
            "non_vegetarian": "Exceptional (Celebrated coastal seafood, Chettinad chicken, and mutton biryanis)",
            "vegetarian": "Very High (World-renowned South Indian vegetarian paradise)",
            "vegan": "High (Idli, Vada, Appam, Idiyappam, Sambar, Coconut Chutney)",
            "gluten_free": "Exceptional (Rice and lentil-based batters are naturally gluten-free)",
            "halal": "Widespread (Numerous certified Chettinad and Biryani kitchens in Triplicane and Royapettah)"
        }
    },
    "delhi": {
        "culinary_tradition": "Rich North Indian & Mughlai Gastronomy (Slow-simmered gravies, tandoori marinades, seekh kebabs, and aromatic saffron biryanis)",
        "signature_dishes": [
            {
                "name": "Delhi Butter Chicken & Garlic Naan",
                "pronunciation": "Murg Makhani",
                "type": "Main Course",
                "price_range_inr": "₹350 - ₹650",
                "price_range_usd": "$4 - $8",
                "description": "Tender tandoor-roasted chicken simmered in a velvety, mildly spiced tomato, butter, and cashew gravy finished with dried fenugreek leaves (kasoori methi).",
                "dietary": ["Non-Vegetarian", "Contains Poultry", "Contains Dairy", "Gluten in Naan", "Halal"],
                "must_try_spot": "Moti Mahal (Daryaganj) or Gulati (Pandara Road)",
                "image_tag": "meat"
            },
            {
                "name": "Old Delhi Mutton Seekh & Galouti Kebabs",
                "pronunciation": "Seekh Kabab",
                "type": "Appetizer / Grill",
                "price_range_inr": "₹260 - ₹480",
                "price_range_usd": "$3.2 - $6",
                "description": "Finely minced spiced mutton skewers charred over charcoal embers, served with thin roomali roti, sliced onions, and mint chutney.",
                "dietary": ["Non-Vegetarian", "Contains Mutton/Meat", "Halal", "Gluten in Roti"],
                "must_try_spot": "Karim's (Jama Masjid) or Qureshi Kabab Corner",
                "image_tag": "meat"
            },
            {
                "name": "Chole Bhature",
                "pronunciation": "CHOH-lay bah-TOO-ray",
                "type": "Signature Breakfast / Lunch",
                "price_range_inr": "₹120 - ₹220",
                "price_range_usd": "$1.5 - $2.7",
                "description": "Fluffy, golden deep-fried sourdough bread served with spicy, dark chickpea curry, pickled onions, and mint chutney.",
                "dietary": ["Vegetarian", "Vegan Options", "Contains Gluten"],
                "must_try_spot": "Sita Ram Diwan Chand (Paharganj)",
                "image_tag": "snack"
            },
            {
                "name": "Crispy Aloo Tikki & Dahi Bhalla",
                "pronunciation": "AH-loo TIK-kee",
                "type": "Street Food Chaat",
                "price_range_inr": "₹80 - ₹160",
                "price_range_usd": "$1 - $2",
                "description": "Golden pan-fried spiced potato patties topped with whisked sweet yogurt, tamarind reduction, and roasted cumin.",
                "dietary": ["Vegetarian", "Contains Dairy", "Gluten-Free"],
                "must_try_spot": "Natraj Dahi Bhalla Corner (Chandni Chowk)",
                "image_tag": "snack"
            },
            {
                "name": "Shahi Tukda with Rabri",
                "pronunciation": "SHAH-hee TOOK-rah",
                "type": "Dessert",
                "price_range_inr": "₹90 - ₹180",
                "price_range_usd": "$1 - $2.2",
                "description": "Royal Mughal dessert: crisp fried bread steeped in saffron-cardamom syrup and blanketed in thick condensed milk rabri with pistachios.",
                "dietary": ["Vegetarian", "Contains Dairy", "Contains Nuts"],
                "must_try_spot": "Cool Point (Jama Masjid)",
                "image_tag": "dessert"
            }
        ],
        "street_food_tips": [
            "Opt for busy vendors where frying oil is fresh and food is prepared live in front of you.",
            "Ask for 'Kam Mirch' if you prefer milder spice levels in street curries and chaats."
        ],
        "dietary_friendliness": {
            "non_vegetarian": "World-Class (Famous Mughlai butter chicken, kebabs, nihari, and mutton curries)",
            "vegetarian": "Very High (Over 70% of menus are pure vegetarian friendly)",
            "vegan": "High (Chole, Rajma, Dal Tadka, and Tandoori Roti)",
            "gluten_free": "High (Rice, Biryani, Dosa, and Makki di Roti)",
            "halal": "Widespread (Certified halal meat in all major Mughlai eateries)"
        }
    },
    "rome": {
        "culinary_tradition": "Classic Roman Cucina Povera (Rich, seasonal, rustic pasta, cured pork & charcuterie)",
        "signature_dishes": [
            {
                "name": "Carbonara Autentica",
                "pronunciation": "kahr-boh-NAH-rah",
                "type": "Primi (Pasta)",
                "price_range_inr": "₹1,100 - ₹1,500",
                "price_range_usd": "$13 - $18",
                "description": "Al dente rigatoni or spaghetti coated in silky egg yolks, crispy Guanciale (cured pork cheek), and sharp Pecorino Romano cheese with coarse black pepper.",
                "dietary": ["Non-Vegetarian", "Contains Pork", "Contains Dairy", "Contains Gluten", "Egg-based"],
                "must_try_spot": "Trattoria Da Enzo al 29 (Trastevere)",
                "image_tag": "pasta"
            },
            {
                "name": "Saltimbocca alla Romana",
                "pronunciation": "sahl-teem-BOHK-kah",
                "type": "Secondi (Meat)",
                "price_range_inr": "₹1,400 - ₹2,100",
                "price_range_usd": "$17 - $25",
                "description": "Tender veal cutlets wrapped with salty prosciutto crudo and fresh sage leaves, pan-sautéed with dry white wine and butter.",
                "dietary": ["Non-Vegetarian", "Contains Meat (Veal/Pork)", "Contains Dairy"],
                "must_try_spot": "Armando al Pantheon",
                "image_tag": "meat"
            },
            {
                "name": "Supplì al Telefono",
                "pronunciation": "soop-PLEE",
                "type": "Street Food / Antipasti",
                "price_range_inr": "₹200 - ₹350",
                "price_range_usd": "$2.5 - $4",
                "description": "Crispy fried rice croquette filled with rich beef & tomato ragù and a melting mozzarella center that stretches like a telephone cord.",
                "dietary": ["Non-Vegetarian", "Contains Dairy", "Contains Gluten", "Contains Meat"],
                "must_try_spot": "Supplizio Roma",
                "image_tag": "snack"
            },
            {
                "name": "Cacio e Pepe",
                "pronunciation": "KAH-choh eh PEH-peh",
                "type": "Primi (Pasta)",
                "price_range_inr": "₹900 - ₹1,300",
                "price_range_usd": "$11 - $15",
                "description": "Pure Roman alchemy using three ingredients: tonnarelli pasta, aged Pecorino Romano, and toasted black pepper emulsified into a creamy sauce.",
                "dietary": ["Vegetarian", "Contains Dairy", "Contains Gluten"],
                "must_try_spot": "Felice a Testaccio",
                "image_tag": "pasta"
            },
            {
                "name": "Artisanal Gelato (Pistacchio & Stracciatella)",
                "pronunciation": "jeh-LAH-toh",
                "type": "Dessert",
                "price_range_inr": "₹280 - ₹550",
                "price_range_usd": "$3.5 - $6.5",
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
            "non_vegetarian": "Exceptional (Classic Roman guanciale, ragù, porchetta, and veal saltimbocca)",
            "vegetarian": "Very High (Cacio e Pepe, Pizza Margherita, Carciofi alla Giudia)",
            "vegan": "High (Pizza Marinara, Pasta all'Arrabbiata)",
            "gluten_free": "Exceptional (AIC-certified gluten-free trattorias across Rome)",
            "halal": "Available (Certified lamb & kebab bistros near Termini & Esquilino)"
        }
    },
    "tokyo": {
        "culinary_tradition": "Washoku (UNESCO Heritage: Fresh ocean seafood, succulent wagyu, ramen craft, and umami balance)",
        "signature_dishes": [
            {
                "name": "Edomae Nigiri Sushi & Sashimi",
                "pronunciation": "SOO-shee",
                "type": "Main (Seafood)",
                "price_range_inr": "₹1,800 - ₹9,500",
                "price_range_usd": "$22 - $115",
                "description": "Freshly sliced seasonal ocean fish (Otoro, Uni, Shime-saba, Salmon) delicately pressed over warm vinegared Akazu sushi rice with fresh wasabi.",
                "dietary": ["Non-Vegetarian", "Contains Seafood", "Gluten-Free (request Tamari)"],
                "must_try_spot": "Sushi Dai (Toyosu) or Manten Sushi (Marunouchi)",
                "image_tag": "sushi"
            },
            {
                "name": "Tonkotsu & Shoyu Ramen with Chashu",
                "pronunciation": "RAH-men",
                "type": "Main",
                "price_range_inr": "₹600 - ₹1,100",
                "price_range_usd": "$7 - $13",
                "description": "Springy wheat noodles in a 16-hour rich pork bone or savory soy broth topped with melt-in-mouth chashu pork, seasoned ajitama soft-boiled egg, and nori seaweed.",
                "dietary": ["Non-Vegetarian", "Contains Pork", "Contains Gluten", "Egg-based"],
                "must_try_spot": "Afuri (Yuzu Shoyu) or Ichiran Shibuya",
                "image_tag": "ramen"
            },
            {
                "name": "Charcoal Yakitori Skewers Platter",
                "pronunciation": "YAH-kee-TOH-ree",
                "type": "Izakaya / Grill",
                "price_range_inr": "₹450 - ₹950",
                "price_range_usd": "$5.5 - $11.5",
                "description": "Bite-sized chicken thigh, scallion (negima), and meatball skewers glazed in sweet tare soy or sea salt, grilled over white oak binchotan charcoal.",
                "dietary": ["Non-Vegetarian", "Contains Poultry", "Gluten in Tare (Salt option is GF)"],
                "must_try_spot": "Torikizoku or Omoide Yokocho (Shinjuku)",
                "image_tag": "meat"
            },
            {
                "name": "Shojin Ryori Seasonal Tempura & Tofu",
                "pronunciation": "SHOH-jeen RYOH-ree",
                "type": "Buddhist Heritage Meal",
                "price_range_inr": "₹1,200 - ₹2,400",
                "price_range_usd": "$15 - $29",
                "description": "Delicate temple vegetarian cuisine featuring crisp seasonal lotus root, sweet potato tempura, silken yuba tofu, and mountain vegetables.",
                "dietary": ["Vegetarian", "Vegan", "Plant-Based"],
                "must_try_spot": "Daigo (Minato City) or Komaki Shokudo",
                "image_tag": "snack"
            }
        ],
        "street_food_tips": [
            "In Japan, walking while eating is generally frowned upon; enjoy your snack right near the vendor stall before moving on.",
            "Slurping noodles loudly is considered a compliment to the chef and aerates the hot broth for fuller flavor."
        ],
        "dietary_friendliness": {
            "non_vegetarian": "Legendary (Wagyu beef, world-famous sashimi, yakitori, and tonkotsu ramen)",
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
                dish_text = (d.get("name", "") + " " + d.get("description", "") + " " + " ".join(d.get("dietary", []))).lower()
                
                is_match = True
                for pref in query.dietary_preferences:
                    pref_l = pref.lower().strip()
                    if pref_l in ["vegetarian", "veg"]:
                        if "vegetarian" not in diet_tags and "vegan" not in diet_tags and "plant-based" not in diet_tags:
                            is_match = False
                    elif pref_l in ["non-vegetarian", "non-veg", "nonveg", "meat"]:
                        is_non_veg = any(k in dish_text for k in [
                            "non-vegetarian", "non-veg", "chicken", "meat", "poultry", 
                            "seafood", "fish", "pork", "beef", "lamb", "mutton", "veal", 
                            "duck", "guanciale", "bacon", "prosciutto", "prawn", "crab", 
                            "shrimp", "sushi", "sashimi", "salmon", "tuna", "vanjaram"
                        ]) or "non-vegetarian" in diet_tags
                        if not is_non_veg:
                            is_match = False
                    elif pref_l in ["vegan", "plant-based"]:
                        if "vegan" not in diet_tags and "plant-based" not in diet_tags:
                            is_match = False
                    elif pref_l in ["gluten-free", "gluten free", "glutenfree"]:
                        if not any("gluten-free" in t for t in diet_tags):
                            is_match = False
                    elif pref_l in ["halal"]:
                        if not any("halal" in t for t in diet_tags) and not ("halal" in dish_text):
                            is_match = False

                if is_match:
                    filtered.append(d)
            if filtered:
                dishes = filtered

        return {
            "status": "success",
            "city": query.city.title(),
            "default_currency": "INR",
            "currency_symbol": "₹",
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
            "culinary_tradition": f"Authentic Regional Gastronomy of {city.title()} (Locally sourced meats, coastal catch, farm produce, and vibrant street markets)",
            "signature_dishes": [
                {
                    "name": f"Traditional {city.title()} Slow-Roasted Heritage Meat & Hearth Bread",
                    "pronunciation": f"{city.title()} Special",
                    "type": "Signature Non-Veg Main",
                    "price_range_inr": "₹450 - ₹950",
                    "price_range_usd": "$5 - $12",
                    "description": f"Slow-simmered tender cuts and aromatics in a rich reduction of regional spices, served alongside warm freshly baked hearth bread.",
                    "dietary": ["Non-Vegetarian", "Contains Meat / Poultry", "Local Specialty"],
                    "must_try_spot": f"Central Old Town Bistro & Grill in {city.title()}",
                    "image_tag": "meat"
                },
                {
                    "name": f"{city.title()} Pan-Seared Coastal Catch or Spiced Skewer",
                    "pronunciation": f"Marinara {city.title()}",
                    "type": "Seafood / Grill",
                    "price_range_inr": "₹380 - ₹780",
                    "price_range_usd": "$4.5 - $9.5",
                    "description": "Locally harvested fresh catch or skewer marinated in garlic herb emulsion and chargrilled to succulent perfection.",
                    "dietary": ["Non-Vegetarian", "Contains Seafood / Poultry", "Gluten-Free"],
                    "must_try_spot": f"Harbor & Market Taverns in {city.title()}",
                    "image_tag": "meat"
                },
                {
                    "name": f"Artisanal {city.title()} Farmhouse Cheese & Truffle Pasta",
                    "pronunciation": f"Formaggio {city.title()}",
                    "type": "Vegetarian Main Course",
                    "price_range_inr": "₹320 - ₹620",
                    "price_range_usd": "$3.8 - $7.5",
                    "description": "Handcrafted regional pasta or roasted vegetables tossed with aged local cheese, roasted garlic, and seasonal herbs.",
                    "dietary": ["Vegetarian", "Contains Dairy", "Vegetarian Favorite"],
                    "must_try_spot": "Old Town Artisan Trattorias",
                    "image_tag": "pasta"
                },
                {
                    "name": "Artisanal Street Delicacy & Spiced Sweet",
                    "pronunciation": "Dolcetto",
                    "type": "Street Food / Sweet",
                    "price_range_inr": "₹150 - ₹350",
                    "price_range_usd": "$2 - $4.5",
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
                "non_vegetarian": "Abundant (Local roast meats, skewers, and seafood delicacies)",
                "vegetarian": "High (Fresh farm-to-table salads, cheeses, roasted grains)",
                "vegan": "Moderate (Legume dishes and roasted vegetable platters)",
                "gluten_free": "Moderate (Rice and grilled dishes widely accessible)",
                "halal": "Accessible (Inquire at Mediterranean and Turkish district eateries)"
            }
        }
