import requests
from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware
import openai  # Import OpenAI library
import os

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# In-memory store for user thresholds
user_thresholds = {}

# Function to fetch data from Fake Store API
def fetch_fake_store_api():
    try:
        response = requests.get("https://fakestoreapi.com/products")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Fake Store API data: {e}")
        return {"error": "Failed to fetch data from Fake Store API"}

# Function to fetch data from Open Products API
def fetch_open_products_api():
    try:
        response = requests.get("https://api.escuelajs.co/api/v1/products")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Open Products API data: {e}")
        return {"error": "Failed to fetch data from Open Products API"}

# Function to normalize data from Fake Store API
def normalize_fake_store_data(data):
    return [
        {
            "id": item["id"],
            "title": item["title"],
            "price": item["price"],
            "image": item["image"],
            "source": "Fake Store API",
        }
        for item in data
    ]

# Function to normalize data from Open Products API
def normalize_open_products_data(data):
    return [
        {
            "id": item["id"],
            "title": item["title"],
            "price": item["price"],
            "image": item["images"][0] if item["images"] else None,
            "source": "Open Products API",
        }
        for item in data
    ]

# Function to get AI recommendations using OpenAI ChatCompletion
def get_ai_recommendations(query, products):
    try:
        # Format the product list into a prompt
        product_descriptions = "\n".join(
            [f"{p['title']} - ${p['price']}" for p in products]
        )
        messages = [
            {"role": "system", "content": "You are a helpful assistant providing product recommendations."},
            {"role": "user", "content": f"A user searched for '{query}'. Based on the following products:\n{product_descriptions}\nSuggest three alternative recommendations that are:\n1. Cheaper but good alternatives.\n2. Better value for slightly higher prices.\nProvide a clear explanation for each suggestion."},
        ]

        # Call OpenAI API with the correct syntax
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if you're using that model
            messages=messages,
            max_tokens=150,
        )

        # Extract and return recommendations
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating AI recommendations: {e}")
        return "Failed to generate recommendations."

# Endpoint to search for products with AI recommendations
@app.get("/search")
def search_products(query: str):
    fake_store_data = fetch_fake_store_api()
    open_products_data = fetch_open_products_api()

    # Check for errors
    if "error" in fake_store_data:
        raise HTTPException(status_code=500, detail=fake_store_data["error"])
    if "error" in open_products_data:
        raise HTTPException(status_code=500, detail=open_products_data["error"])

    # Normalize data
    normalized_fake_store = normalize_fake_store_data(fake_store_data)
    normalized_open_products = normalize_open_products_data(open_products_data)

    # Combine and filter results
    combined_products = normalized_fake_store + normalized_open_products
    filtered_products = [
        product
        for product in combined_products
        if query.lower() in product["title"].lower()
    ]

    # Get AI recommendations
    ai_recommendations = get_ai_recommendations(query, filtered_products)

    return {
        "products": filtered_products,
        "recommendations": ai_recommendations,
    }

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Product API"}
