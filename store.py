from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import json
import os
import stripe
from dotenv import load_dotenv

load_dotenv()

# Replace with your keys later
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")

app = FastAPI(title="TrendDrop - Trending Digital Goods")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        with open("data/products.json") as f:
            products = json.load(f)
    except:
        products = []
    
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>TrendDrop - Auto Trending Digital Store</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f4f4f9; }
        .product { border: 1px solid #ddd; padding: 20px; margin: 20px; border-radius: 8px; background: white; }
        .niche-select { padding: 10px; margin: 20px 0; }
    </style>
    <script>
    async function buyNow(productId) {
        try {
            const response = await fetch('/create-checkout-session', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({product_id: productId})
            });
            const data = await response.json();
            if (data.url) {
                window.location.href = data.url;
            }
        } catch(e) {
            alert('Checkout error - check console');
        }
    }
    </script>
    </head>
    <body>
    <h1>TrendDrop 🚀</h1>
    <p>Auto-updating digital products from current trends. Profits to $79cnoteee</p>
    
    <div class="niche-select">
        <label>Select Department/Niche: </label>
        <select onchange="window.location.href='?niche='+this.value">
            <option value="All Trending">All Trending Areas</option>
            <option value="Fitness & Health">Fitness & Health</option>
            <option value="Finance & Side Hustles">Finance & Side Hustles</option>
            <option value="Productivity">Productivity</option>
            <option value="Creative & Memes">Creative & Memes</option>
            <option value="Tech & AI">Tech & AI</option>
        </select>
    </div>
    
    <div id="products">
    """
    
    niche = request.query_params.get("niche", "All Trending")
    # Filter by niche in real impl
    for p in products[:8]:
        html += f"""
        <div class="product">
            <h3>{p['title']}</h3>
            <p>{p['description']}</p>
            <p><strong>${p['price']}</strong> - Instant Download</p>
            <button onclick="buyNow('{p['id']}')">Buy Now - ${p['price']}</button>
            <small>Niche: {p['niche']}</small>
        </div>
        """
    
    html += """
    </div>
    <footer><p>Auto-refreshes every 2 days. Built to sell itself.</p></footer>
    </body>
    </html>
    """
    return HTMLResponse(html)

@app.get("/update")
async def update_store():
    # Run updates
    from app.trend_scanner import get_current_trends
    from app.product_generator import generate_products
    trends = get_current_trends()["trends"]
    generate_products(8, trends)
    return {"status": "updated", "trends": len(trends)}

@app.post("/create-checkout-session")
async def create_checkout_session(product_id: str):
    try:
        # Load product
        with open("data/products.json") as f:
            products = json.load(f)
        product = next((p for p in products if p["id"] == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product['title'],
                    },
                    'unit_amount': int(product['price'] * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://yourdomain.com/",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)