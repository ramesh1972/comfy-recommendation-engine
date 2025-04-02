
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
from typing import List, Dict, Any, Optional
import os
from pathlib import Path
import json

app = FastAPI(title="Recommendation API")

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define data models
class User(BaseModel):
    id: int
    name: str

class Product(BaseModel):
    id: int
    name: str
    category: str
    description: str
    rating: float
    image_url: Optional[str] = None

class Rating(BaseModel):
    userId: int
    productId: int
    rating: float

# Sample data path
DATA_DIR = Path(__file__).parent / "data"
USERS_FILE = DATA_DIR / "users.json"
PRODUCTS_FILE = DATA_DIR / "products.json"
RATINGS_FILE = DATA_DIR / "ratings.json"
MODEL_FILE = DATA_DIR / "recommendation_model.pkl"

# Make sure the data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Sample data
sample_users = [
    {"id": 1, "name": "Alice Smith"},
    {"id": 2, "name": "Bob Johnson"},
    {"id": 3, "name": "Charlie Brown"},
    {"id": 4, "name": "Diana Prince"},
    {"id": 5, "name": "Ethan Hunt"},
    {"id": 6, "name": "Fiona Gallagher"},
    {"id": 7, "name": "George Bailey"},
    {"id": 8, "name": "Hannah Baker"},
]

sample_products = [
    {
        "id": 1,
        "name": "Comfortable Office Chair",
        "category": "Furniture",
        "description": "Ergonomic office chair with lumbar support and breathable mesh back.",
        "rating": 4.5,
        "image_url": "https://images.unsplash.com/photo-1589384267710-7a25bc5b4862?q=80&w=500&auto=format&fit=crop"
    },
    {
        "id": 2,
        "name": "Adjustable Standing Desk",
        "category": "Furniture",
        "description": "Electric height-adjustable desk with memory settings and spacious work surface.",
        "rating": 4.8,
        "image_url": "https://images.unsplash.com/photo-1518655048521-f130df041f66?q=80&w=500&auto=format&fit=crop"
    },
    {
        "id": 3,
        "name": "Mechanical Keyboard",
        "category": "Electronics",
        "description": "Tactile mechanical keyboard with customizable RGB lighting and programmable keys.",
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1561112078-7d24e04c3407?q=80&w=500&auto=format&fit=crop"
    },
    {
        "id": 4,
        "name": "Ultrawide Monitor",
        "category": "Electronics",
        "description": "34-inch curved ultrawide monitor with high resolution and excellent color accuracy.",
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1607706009771-cbcce7b9d83c?q=80&w=500&auto=format&fit=crop"
    },
    {
        "id": 5,
        "name": "Noise-Canceling Headphones",
        "category": "Audio",
        "description": "Premium wireless headphones with active noise cancellation and long battery life.",
        "rating": 4.6,
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?q=80&w=500&auto=format&fit=crop"
    },
    {
        "id": 6,
        "name": "Smart LED Desk Lamp",
        "category": "Lighting",
        "description": "Adjustable LED desk lamp with multiple color temperatures and brightness levels.",
        "rating": 4.2,
        "image_url": "https://images.unsplash.com/photo-1534105615256-13940a56ff44?q=80&w=500&auto=format&fit=crop"
    },
    {
        "id": 7,
        "name": "Laptop Stand",
        "category": "Accessories",
        "description": "Adjustable aluminum laptop stand for improved ergonomics and cooling.",
        "rating": 4.4,
        "image_url": "https://images.unsplash.com/photo-1675365889958-1f217bf8538e?q=80&w=500&auto=format&fit=crop"
    },
    {
        "id": 8,
        "name": "Wireless Mouse",
        "category": "Electronics",
        "description": "Ergonomic wireless mouse with adjustable DPI and quiet click buttons.",
        "rating": 4.1,
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?q=80&w=500&auto=format&fit=crop"
    },
    {
        "id": 9,
        "name": "Bluetooth Speaker",
        "category": "Audio",
        "description": "Portable Bluetooth speaker with rich bass and 20-hour battery life.",
        "rating": 4.3,
        "image_url": "https://images.unsplash.com/photo-1589001181560-f483fbc24338?q=80&w=500&auto=format&fit=crop"
    },
    {
        "id": 10,
        "name": "External SSD",
        "category": "Storage",
        "description": "Fast external SSD with USB-C connection and shock-resistant design.",
        "rating": 4.7,
        "image_url": "https://images.unsplash.com/photo-1597333193168-5d59bdff8e08?q=80&w=500&auto=format&fit=crop"
    },
    {
        "id": 11,
        "name": "Desk Organizer",
        "category": "Office",
        "description": "Multi-compartment desk organizer for pens, sticky notes, and small items.",
        "rating": 4.0,
        "image_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=500&auto=format&fit=crop"
    },
    {
        "id": 12,
        "name": "Webcam",
        "category": "Electronics",
        "description": "HD webcam with auto-focus and built-in noise-canceling microphone.",
        "rating": 4.2,
        "image_url": "https://images.unsplash.com/photo-1596314843256-ce8ef25b2cac?q=80&w=500&auto=format&fit=crop"
    }
]

# Initial ratings - this could be expanded for a more robust sample
sample_ratings = [
    {"userId": 1, "productId": 1, "rating": 4.5},
    {"userId": 1, "productId": 3, "rating": 5.0},
    {"userId": 1, "productId": 5, "rating": 4.0},
    {"userId": 2, "productId": 2, "rating": 4.5},
    {"userId": 2, "productId": 4, "rating": 5.0},
    {"userId": 2, "productId": 6, "rating": 3.5},
    {"userId": 3, "productId": 1, "rating": 3.5},
    {"userId": 3, "productId": 7, "rating": 4.5},
    {"userId": 3, "productId": 9, "rating": 4.0},
    {"userId": 4, "productId": 2, "rating": 5.0},
    {"userId": 4, "productId": 8, "rating": 4.0},
    {"userId": 4, "productId": 10, "rating": 4.5},
    {"userId": 5, "productId": 3, "rating": 3.5},
    {"userId": 5, "productId": 11, "rating": 4.0},
    {"userId": 5, "productId": 12, "rating": 4.5},
    {"userId": 6, "productId": 4, "rating": 4.0},
    {"userId": 6, "productId": 6, "rating": 3.0},
    {"userId": 6, "productId": 10, "rating": 5.0},
    {"userId": 7, "productId": 5, "rating": 4.5},
    {"userId": 7, "productId": 7, "rating": 3.5},
    {"userId": 7, "productId": 9, "rating": 4.0},
    {"userId": 8, "productId": 8, "rating": 3.0},
    {"userId": 8, "productId": 11, "rating": 4.5},
    {"userId": 8, "productId": 12, "rating": 4.0}
]

# Utility functions for data management
def initialize_data():
    """Initialize data files with sample data if they don't exist."""
    if not USERS_FILE.exists():
        with open(USERS_FILE, 'w') as f:
            json.dump(sample_users, f)
    
    if not PRODUCTS_FILE.exists():
        with open(PRODUCTS_FILE, 'w') as f:
            json.dump(sample_products, f)
    
    if not RATINGS_FILE.exists():
        with open(RATINGS_FILE, 'w') as f:
            json.dump(sample_ratings, f)

def load_data():
    """Load data from JSON files."""
    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        
        with open(PRODUCTS_FILE, 'r') as f:
            products = json.load(f)
        
        with open(RATINGS_FILE, 'r') as f:
            ratings = json.load(f)
        
        return users, products, ratings
    except Exception as e:
        print(f"Error loading data: {e}")
        return sample_users, sample_products, sample_ratings

def generate_recommendation_model():
    """Generate a simple recommendation model based on user ratings."""
    users, products, ratings = load_data()
    
    # Create a user-item matrix
    user_ids = [user["id"] for user in users]
    product_ids = [product["id"] for product in products]
    
    # Create mappings for user and product IDs to matrix indices
    user_to_idx = {user_id: i for i, user_id in enumerate(user_ids)}
    product_to_idx = {product_id: i for i, product_id in enumerate(product_ids)}
    idx_to_product = {i: product_id for product_id, i in product_to_idx.items()}
    
    # Create the ratings matrix (users x products)
    matrix = np.zeros((len(user_ids), len(product_ids)))
    
    # Fill in the ratings
    for rating in ratings:
        user_idx = user_to_idx.get(rating["userId"])
        product_idx = product_to_idx.get(rating["productId"])
        if user_idx is not None and product_idx is not None:
            matrix[user_idx, product_idx] = rating["rating"]
    
    # Create a simple model using collaborative filtering
    # For simplicity, we're just computing similarity between users
    # and will recommend products that similar users rated highly
    
    # Compute similarity matrix (cosine similarity)
    # Handle zero vectors to avoid division by zero
    norms = np.sqrt(np.sum(matrix ** 2, axis=1))
    norms[norms == 0] = 1  # Avoid division by zero
    normalized = matrix / norms[:, np.newaxis]
    
    # Calculate similarity matrix
    similarity = np.dot(normalized, normalized.T)
    
    # Create a simple model with the necessary components
    model = {
        "matrix": matrix,
        "similarity": similarity,
        "user_to_idx": user_to_idx,
        "product_to_idx": product_to_idx,
        "idx_to_product": idx_to_product
    }
    
    # Save the model
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    
    return model

def load_or_create_model():
    """Load the recommendation model, or create it if it doesn't exist."""
    if MODEL_FILE.exists():
        try:
            with open(MODEL_FILE, 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
    
    print("Creating new recommendation model")
    return generate_recommendation_model()

def get_recommendations(user_id: int, num_recommendations: int = 5):
    """Get recommendations for a user based on collaborative filtering."""
    model = load_or_create_model()
    users, products, _ = load_data()
    
    # Check if the user exists
    if user_id not in model["user_to_idx"]:
        return []
    
    user_idx = model["user_to_idx"][user_id]
    similarity = model["similarity"][user_idx]
    matrix = model["matrix"]
    
    # Get the most similar users
    # Exclude the user's own similarity (which is 1.0)
    similar_users = [(i, sim) for i, sim in enumerate(similarity) if i != user_idx]
    similar_users.sort(key=lambda x: x[1], reverse=True)
    similar_users = similar_users[:3]  # Top 3 similar users
    
    # Get products the user hasn't rated yet
    user_ratings = matrix[user_idx]
    unrated_products = [i for i, rating in enumerate(user_ratings) if rating == 0]
    
    # Compute weighted ratings for unrated products
    product_scores = {}
    for product_idx in unrated_products:
        weighted_sum = 0
        sim_sum = 0
        
        for sim_user_idx, sim_score in similar_users:
            # Get the similar user's rating for this product
            rating = matrix[sim_user_idx, product_idx]
            if rating > 0:  # The similar user has rated this product
                weighted_sum += rating * sim_score
                sim_sum += sim_score
        
        # Calculate the predicted rating if we have data
        if sim_sum > 0:
            product_scores[product_idx] = weighted_sum / sim_sum
    
    # Sort products by predicted rating
    recommended_product_indices = sorted(product_scores.keys(), 
                                        key=lambda x: product_scores[x],
                                        reverse=True)[:num_recommendations]
    
    # Convert indices back to product IDs
    recommended_product_ids = [model["idx_to_product"][idx] for idx in recommended_product_indices]
    
    # Get full product details
    product_lookup = {product["id"]: product for product in products}
    recommendations = [product_lookup[product_id] for product_id in recommended_product_ids 
                    if product_id in product_lookup]
    
    return recommendations

def add_rating(rating: Rating):
    """Add a new rating and update the data file."""
    try:
        _, _, ratings = load_data()
        
        # Check if this rating already exists
        for i, r in enumerate(ratings):
            if r["userId"] == rating.userId and r["productId"] == rating.productId:
                # Update existing rating
                ratings[i]["rating"] = rating.rating
                break
        else:
            # Add new rating
            ratings.append({
                "userId": rating.userId,
                "productId": rating.productId,
                "rating": rating.rating
            })
        
        # Save updated ratings
        with open(RATINGS_FILE, 'w') as f:
            json.dump(ratings, f)
        
        # We could regenerate the model here, but for simplicity
        # we'll skip that for now since it could be computationally expensive
        return True
    except Exception as e:
        print(f"Error adding rating: {e}")
        return False

# Initialize the API
@app.on_event("startup")
async def startup_event():
    """Initialize data and model when the API starts."""
    initialize_data()
    load_or_create_model()

# API Endpoints
@app.get("/users", response_model=List[User])
async def get_users():
    """Get all users."""
    users, _, _ = load_data()
    return users

@app.get("/products", response_model=List[Product])
async def get_products():
    """Get all products."""
    _, products, _ = load_data()
    return products

@app.get("/recommendations/{user_id}", response_model=List[Product])
async def get_user_recommendations(user_id: int, limit: int = 8):
    """Get recommendations for a specific user."""
    if limit > 20:
        limit = 20  # Cap the number of recommendations
    
    recommendations = get_recommendations(user_id, limit)
    if not recommendations:
        # If no recommendations, return some random products
        _, products, _ = load_data()
        import random
        random.shuffle(products)
        return products[:limit]
    
    return recommendations

@app.post("/ratings")
async def add_user_rating(rating: Rating):
    """Add or update a rating from a user."""
    success = add_rating(rating)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save rating")
    return {"success": True}

@app.post("/generate_model")
async def regenerate_model():
    """Manually trigger model regeneration."""
    try:
        generate_recommendation_model()
        return {"success": True, "message": "Model regenerated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to regenerate model: {str(e)}")

# Route to check if the API is running
@app.get("/")
async def root():
    return {"status": "Recommendation API is running", "version": "1.0"}

# Run the API with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
