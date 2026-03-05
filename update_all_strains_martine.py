#!/usr/bin/env python3
"""
Update Martine's 12 new strains with premium descriptions, tags, and metafields.
"""

from shopify_api import update_product_description, create_or_update_metafield

products_data = {
    "Blue Cheese": {
        "id": "9026937192660",
        "description": "Blue Cheese is a world-renowned indica hybrid that blends the savory, pungent aroma of UK Cheese with the sweet, berry notes of Blueberry. Expect a heavy, relaxing body high that melts away stress and prepares you for a peaceful night's sleep.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "Blueberry x UK Cheese (classic indica hybrid)",
            "flowering_time": "8–9 weeks",
            "profile": "80/20 Indica-Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±30%",
            "average_thc_levels": "18–22%",
            "flavours": "Pungent blue cheese, sweet blueberries, savory earth, creamy funk",
            "effects": "Relaxed • Euphoric • Sleepy • Happy • Hungry",
            "used_for": "Stress relief, pain management, insomnia, evening relaxation"
        }
    },
    "Sour Diesel D": {
        "id": "9026936897748",
        "description": "Sour Diesel D is the quintessential \"wake and bake\" strain, famous for its sharp, fuel-like aroma and invigorating cerebral high. This uplifting sativa delivers a surge of energy and creativity, making it the perfect companion for active days and social gatherings.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "Chemdawg x Super Skunk (classic gassy sativa)",
            "flowering_time": "10–11 weeks",
            "profile": "90/10 Sativa-Dominant Hybrid",
            "height": "Tall",
            "stretch_percentage": "±50%",
            "average_thc_levels": "20–26%",
            "flavours": "Pungent diesel, sharp citrus, earthy pine, skunky gas",
            "effects": "Energetic • Uplifted • Creative • Focused • Talkative",
            "used_for": "Daytime productivity, creative inspiration, social energy, fatigue relief"
        }
    },
    "Sour Diesel MS1": {
        "id": "9026936045780",
        "description": "Sour Diesel MS1 is a refined phenotype of the legendary Sour D, selected for its piercing citrus-gas aroma and rapid onset. Delivering a powerful cerebral buzz that sharpens focus and elevates the mood, it’s an elite choice for those seeking the ultimate sativa experience.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "Select phenotype of Sour Diesel (Chemdawg x Super Skunk)",
            "flowering_time": "10–11 weeks",
            "profile": "90/10 Sativa-Dominant Hybrid",
            "height": "Tall",
            "stretch_percentage": "±45%",
            "average_thc_levels": "22–26%",
            "flavours": "Intense gasoline, lemon zest, herbal spice, earthy diesel",
            "effects": "Cerebral • Energetic • Uplifted • Happy • Creative",
            "used_for": "Stress relief, mood elevation, creative focus, daytime activities"
        }
    },
    "Astro Grape": {
        "id": "9026935095508",
        "description": "Astro Grape is a stellar indica hybrid that launches you into a world of sweet grape flavors and gassy undertones. Its potent, sedating effects provide a grounding calm that’s perfect for exploring the cosmos from the comfort of your couch.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "Grape Pie x Jet Fuel Gelato (gassy purple hybrid)",
            "flowering_time": "8–9 weeks",
            "profile": "75/25 Indica-Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±35%",
            "average_thc_levels": "24–28%",
            "flavours": "Sweet grape candy, pungent gas, creamy berry, tart citrus",
            "effects": "Euphoric • Relaxed • Dreamy • Calm • Heavy body buzz",
            "used_for": "Evening wind-down, anxiety relief, insomnia, deep relaxation"
        }
    },
    "White Widow": {
        "id": "9026933293268",
        "description": "White Widow is a cannabis icon, beloved since the 90s for its resin-drenched buds and balanced, social high. Offering a perfect blend of cerebral stimulation and physical relaxation, it’s the go-to strain for sparking conversation and creative flow.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "Brazilian Sativa x South Indian Indica (legendary global hybrid)",
            "flowering_time": "8–9 weeks",
            "profile": "60/40 Sativa-Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±35%",
            "average_thc_levels": "18–25%",
            "flavours": "Woody pine, earthy spice, floral citrus, herbal musk",
            "effects": "Talkative • Creative • Uplifted • Energetic • Euphoric",
            "used_for": "Social activities, creative projects, stress relief, mood enhancement"
        }
    },
    "Mad Ghost": {
        "id": "9026932211924",
        "description": "Mad Ghost is a potent indica-leaning hybrid that haunts you with its complex profile of sweet lime and earthy pine. Expect a hauntingly beautiful high that starts with a euphoric mental lift before settling into a deep, ghostly body relaxation that banishes stress and pain.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "Ghost OG (OG Kush x Afghani)",
            "flowering_time": "8–10 weeks",
            "profile": "70/30 Indica-Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±30%",
            "average_thc_levels": "20–24%",
            "flavours": "Sweet lime, pine resin, kushy earth, tropical citrus",
            "effects": "Euphoric • Relaxed • Happy • Hungry • Sleepy",
            "used_for": "Pain management, stress relief, appetite stimulation, evening rest"
        }
    },
    "Girl Scout Cookies": {
        "id": "9026931261652",
        "description": "Girl Scout Cookies (GSC) is a legendary hybrid that redefined the modern cannabis landscape with its dessert-like aroma and potent, balanced effects. Indulge in its sweet, minty flavors and experience a wave of euphoria that leaves you feeling happy, relaxed, and ready to socialize.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "OG Kush x Durban Poison (industry-shifting hybrid)",
            "flowering_time": "9–10 weeks",
            "profile": "60/40 Indica-Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±35%",
            "average_thc_levels": "20–28%",
            "flavours": "Sweet dough, minty chocolate, cherry, earthy spice",
            "effects": "Euphoric • Happy • Relaxed • Creative • Tingly",
            "used_for": "Stress relief, pain management, appetite loss, social gatherings"
        }
    },
    "Christmas Cracker": {
        "id": "9026929983700",
        "description": "Christmas Cracker is a festive delight, offering a complex blend of roasted nuts, sweet vanilla, and a gassy kick. This uplifting hybrid deliver a \"crackling\" cerebral high that sparks joy and conversation, making it the life of any holiday party or social event.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "Dosi Dos x Project 4516 (festive gas-cake lineage)",
            "flowering_time": "8–10 weeks",
            "profile": "60/40 Sativa-Dominant Hybrid",
            "height": "Medium-Tall",
            "stretch_percentage": "±40%",
            "average_thc_levels": "22–27%",
            "flavours": "Roasted nuts, vanilla cream, spicy earth, gassy mint",
            "effects": "Uplifted • Happy • Talkative • Relaxed • Creative",
            "used_for": "Festive gatherings, mood elevation, creative inspiration, daytime social use"
        }
    },
    "SUPERCHEESE": {
        "id": "9026928935124",
        "description": "SUPERCHEESE is a nostalgia-heavy indica hybrid that brings back the legendary, pungent funk of the 1980s Amsterdam coffee shops. With its unapologetic aroma of aged cheddar and savory skunk, it delivers an upbeat, sociable high that gracefully transitions into deep, physical relaxation.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "Exodus Cheese x Super Skunk (the ultimate old-school funk)",
            "flowering_time": "8–9 weeks",
            "profile": "80/20 Indica-Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±35%",
            "average_thc_levels": "17–25%",
            "flavours": "Aged cheddar, savory skunk, sour cream, earthy musk",
            "effects": "Sociable • Relaxed • Euphoric • Hungry • Sleepy",
            "used_for": "Social gatherings, stress relief, appetite stimulation, evening relaxation"
        }
    },
    "ELVIS": {
        "id": "9026927984852",
        "description": "ELVIS is a rockstar sativa hybrid that hits the stage with a vibrant profile of sweet tropical fruit and spicy skunk. This energetic strain delivers a legendary performance, lifting your mood and boosting your creativity for a high that leaves you feeling like the King of the party.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "AK-47 x Skunk #1 (rockstar sativa power)",
            "flowering_time": "8–10 weeks",
            "profile": "70/30 Sativa-Dominant Hybrid",
            "height": "Tall",
            "stretch_percentage": "±45%",
            "average_thc_levels": "17–24%",
            "flavours": "Sweet tropical fruit, spicy skunk, citrus zest, pine resin",
            "effects": "Energetic • Uplifted • Talkative • Creative • Happy",
            "used_for": "Daytime productivity, creative focus, social energy, mood elevation"
        }
    },
    "Grandpa's Endgame": {
        "id": "9026926739668",
        "description": "Grandpa's Endgame is a sophisticated hybrid that marries the old-school tranquility of its heritage with modern potency. Offering a complex aroma of sandalwood and sour cherry, it provides a mellow, all-day high that balances cerebral clarity with physical ease.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "Grandpa's Stash x Endgame RBX (elite Ethos genetics)",
            "flowering_time": "8–10 weeks",
            "profile": "50/50 Balanced Hybrid",
            "height": "Medium",
            "stretch_percentage": "±35%",
            "average_thc_levels": "25–30%",
            "flavours": "Sandalwood, sour cherry, peppery spice, earthy tobacco",
            "effects": "Balanced • Mellow • Uplifted • Creative • Relaxed",
            "used_for": "Any-time use, stress relief, creative focus, balanced relaxation"
        }
    },
    "Purple Panda": {
        "id": "9026925658324",
        "description": "Purple Panda is an adorable but potent indica hybrid that wraps you in a calming embrace of sweet grape and cool mint. Perfect for a cozy evening in, its tingly, social effects keep you engaged and happy while deep relaxation settles in for the ultimate chill session.",
        "tags": ["New Strains", "Limited Collection", "Flower"],
        "metafields": {
            "lineage": "Purple Goji x Center (or GDP x Hindu Kush)",
            "flowering_time": "8–9 weeks",
            "profile": "70/30 Indica-Dominant Hybrid",
            "height": "Medium",
            "stretch_percentage": "±30%",
            "average_thc_levels": "18–22%",
            "flavours": "Sweet grape, ripe berries, cool mint, kushy spice",
            "effects": "Relaxed • Euphoric • Tingly • Social • Calm",
            "used_for": "Evening wind-down, gaming, movie nights, social relaxation"
        }
    }
}

def main():
    print("🚀 Starting bulk update for Martine's 12 strains...")
    print("=" * 60)
    
    for name, data in products_data.items():
        print(f"\n📦 Updating: {name} (ID: {data['id']})")
        
        # 1. Update Description and Tags
        # Prepend Profile text directly in bold (no label) to match Martine's style
        profile = data['metafields']['profile']
        full_description = f"<strong>{profile}</strong><br><br>{data['description']}"
        
        desc_success = update_product_description(
            data['id'], 
            full_description, 
            data['tags']
        )
        
        if desc_success:
            print(f"   ✅ Description & Tags updated")
        else:
            print(f"   ❌ Failed to update Description & Tags")
            
        # 2. Update Metafields
        print(f"   Updating metafields...")
        mf_success_count = 0
        for key, value in data['metafields'].items():
            if create_or_update_metafield(data['id'], "my_fields", key, value):
                mf_success_count += 1
            else:
                print(f"      ❌ Failed on {key}")
                
        print(f"   ✅ {mf_success_count}/{len(data['metafields'])} metafields updated")
        print("-" * 40)

    print("\n" + "=" * 60)
    print("🎉 Bulk update complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
