import json
import random
from datetime import datetime
import os

NICHE_DEPARTMENTS = {
    "Fitness & Health": ["workout plans", "meal prep templates", "fitness trackers", "yoga guides"],
    "Finance & Side Hustles": ["budget planners", "crypto trackers", "passive income guides", "investment templates"],
    "Productivity": ["notion templates", "daily planners", "habit trackers", "goal setting packs"],
    "Creative & Memes": ["canva templates", "meme packs", "wallpaper bundles", "social media kits"],
    "Parenting & Lifestyle": ["family schedules", "recipe books", "home organization"],
    "Tech & AI": ["prompt packs", "ai tool guides", "chatgpt templates"],
    "All Trending": []  # Special: pulls from all
}

def generate_product_idea(trends, niche="All Trending"):
    if niche == "All Trending" or niche not in NICHE_DEPARTMENTS:
        niche_keywords = [kw for sublist in NICHE_DEPARTMENTS.values() if sublist for kw in sublist]
    else:
        niche_keywords = NICHE_DEPARTMENTS[niche]
    
    trend = random.choice(trends) if trends else "viral"
    keyword = random.choice(niche_keywords)
    
    product = {
        "id": f"prod_{datetime.now().strftime('%Y%m%d%H%M')}",
        "title": f"{trend.title()} {keyword.title()} Bundle 2026",
        "description": f"Instant download: {keyword} tailored to current {trend} trends. Editable, high-quality digital files. Perfect for passive income seekers.",
        "price": round(random.uniform(4.99, 19.99), 2),
        "niche": niche,
        "tags": [trend.lower(), keyword.lower(), "digital", "instant"],
        "generated_at": datetime.now().isoformat()
    }
    return product

def generate_products(num=5, trends=None, niche="All Trending"):
    if not trends:
        try:
            with open("trenddrop/data/trends.json") as f:
                trends_data = json.load(f)
                trends = trends_data.get("trends", [])
        except:
            trends = ["AI", "viral", "trending"]
    
    products = [generate_product_idea(trends, niche) for _ in range(num)]
    
    os.makedirs("data", exist_ok=True)
    with open("data/products.json", "w") as f:
        json.dump(products, f, indent=2)
    
    return products

if __name__ == "__main__":
    trends = ["AI tools", "fitness challenge", "side hustle"]
    print(generate_products(3, trends, "Fitness & Health"))