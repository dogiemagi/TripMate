import logging
from typing import Dict, Any, List
from app.models.schemas import PackingChecklistRequest

logger = logging.getLogger("voyage.packing")

class PackingService:
    @staticmethod
    def generate_checklist(req: PackingChecklistRequest) -> Dict[str, Any]:
        dest = req.destination.title()
        season = req.season.title()
        days = req.days

        essentials = [
            {"item": "Passport & Physical/Digital Visas", "category": "Documents", "essential": True},
            {"item": "Travel Insurance Policy Card & Emergency Contacts", "category": "Documents", "essential": True},
            {"item": "Universal Travel Power Plug Adapter (Type C/G/A)", "category": "Electronics", "essential": True},
            {"item": "High-Capacity 10,000+ mAh Power Bank", "category": "Electronics", "essential": True},
            {"item": "Noise-Canceling Headphones / Earplugs", "category": "Electronics", "essential": False},
            {"item": "Compact First-Aid Kit (Pain relievers, antacids, band-aids)", "category": "Health", "essential": True},
            {"item": "TSA-Compliant Clear Toiletry Pouch (< 100ml)", "category": "Toiletries", "essential": True}
        ]

        clothing = []
        if season in ["Summer", "Spring"]:
            clothing.extend([
                {"item": f"{min(days + 2, 7)}x Breathable Cotton/Linen T-Shirts & Tops", "category": "Clothing", "essential": True},
                {"item": "2x Lightweight Chinos or Casual Shorts", "category": "Clothing", "essential": True},
                {"item": "1x Smart Evening Outfit for Dining", "category": "Clothing", "essential": False},
                {"item": "1x Light Cardigan or Packable Windbreaker", "category": "Clothing", "essential": True},
                {"item": "UV400 Polarized Sunglasses & Wide-Brim Sun Hat", "category": "Accessories", "essential": True},
                {"item": "Broad-Spectrum SPF 50+ Sunscreen", "category": "Health", "essential": True}
            ])
        else:
            clothing.extend([
                {"item": "2-3x Merino Wool Base Layers / Thermal Tops", "category": "Clothing", "essential": True},
                {"item": "1x Insulated Down Jacket or Windproof Wool Coat", "category": "Clothing", "essential": True},
                {"item": f"{min(days + 1, 6)}x Warm Sweaters or Fleeces", "category": "Clothing", "essential": True},
                {"item": "Thermal Socks & Waterproof Insulated Boots", "category": "Footwear", "essential": True},
                {"item": "Fleece Beanie, Scarf & Touchscreen Gloves", "category": "Accessories", "essential": True},
                {"item": "Lip Balm & Hydrating Moisturizer", "category": "Health", "essential": True}
            ])

        clothing.extend([
            {"item": "1x Ultra-Comfortable Walking Sneakers (15,000+ steps/day)", "category": "Footwear", "essential": True},
            {"item": "1x Dress Shoes or Loafers for Fine Dining", "category": "Footwear", "essential": False}
        ])

        activity_items = []
        for act in req.activities:
            act_l = act.lower()
            if "swim" in act_l or "beach" in act_l or "snorkel" in act_l:
                activity_items.append({"item": "Quick-Dry Swimsuit & Microfiber Beach Towel", "category": "Beach Gear", "essential": True})
                activity_items.append({"item": "Waterproof Phone Pouch Case", "category": "Beach Gear", "essential": True})
            elif "hiking" in act_l or "trek" in act_l or "nature" in act_l:
                activity_items.append({"item": "Lightweight Collapsible Trekking Poles", "category": "Outdoor", "essential": False})
                activity_items.append({"item": "2L Hydration Bladder or Insulated Flask", "category": "Outdoor", "essential": True})
                activity_items.append({"item": "Insect Repellent Spray", "category": "Outdoor", "essential": True})
            elif "temple" in act_l or "church" in act_l or "culture" in act_l:
                activity_items.append({"item": "Modest Shoulder Wrap / Scarf (Knee & Shoulder cover)", "category": "Culture", "essential": True})
                activity_items.append({"item": "Easy Slip-On Shoes (frequent shoe removal)", "category": "Footwear", "essential": True})
            elif "photo" in act_l or "camera" in act_l:
                activity_items.append({"item": "Camera Body, Wide Lens & Extra SD Cards", "category": "Photography", "essential": True})
                activity_items.append({"item": "Compact Carbon-Fiber Travel Tripod", "category": "Photography", "essential": False})

        all_items = essentials + clothing + activity_items

        return {
            "status": "success",
            "destination": dest,
            "season": season,
            "trip_duration_days": days,
            "total_items": len(all_items),
            "checklist": all_items,
            "luggage_advice": (
                "For a " + str(days) + "-day trip, a 40L carry-on backpack or a 21-inch rolling suitcase "
                "is optimal. Use compression packing cubes to reduce volume by 40%."
            )
        }
