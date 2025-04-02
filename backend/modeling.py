
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
import pickle
from pathlib import Path

def create_recommendation_model(ratings_df):
    """
    Create and save a collaborative filtering recommendation model.
    
    Args:
        ratings_df: DataFrame with columns userId, productId, rating
    
    Returns:
        The trained model
    """
    print("Creating user-item matrix...")
    # Create user-item matrix
    user_item_matrix = ratings_df.pivot(
        index='userId', 
        columns='productId', 
        values='rating'
    ).fillna(0)
    
    # Normalize the data (subtract mean rating for each user)
    user_ratings_mean = np.mean(user_item_matrix.values, axis=1)
    ratings_demeaned = user_item_matrix.values - user_ratings_mean.reshape(-1, 1)
    
    print("Performing SVD decomposition...")
    # Perform SVD
    U, sigma, Vt = svds(ratings_demeaned, k=min(min(ratings_demeaned.shape)-1, 10))
    
    # Convert sigma to diagonal matrix
    sigma = np.diag(sigma)
    
    # Predict ratings for all users
    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    
    # Convert to DataFrame
    preds = pd.DataFrame(
        all_user_predicted_ratings, 
        index=user_item_matrix.index,
        columns=user_item_matrix.columns
    )
    
    # Create a model dictionary
    model = {
        'user_item_matrix': user_item_matrix,
        'predictions': preds,
        'user_ids': list(user_item_matrix.index),
        'product_ids': list(user_item_matrix.columns),
        'user_ratings_mean': user_ratings_mean
    }
    
    # Save the model to disk
    model_path = Path(__file__).parent / 'data' / 'recommendation_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"Model saved to {model_path}")
    
    return model

def recommend_products(model, user_id, n_recommendations=5):
    """
    Recommend products for a user based on the trained model.
    
    Args:
        model: Trained recommendation model
        user_id: ID of the user
        n_recommendations: Number of recommendations to return
        
    Returns:
        List of product IDs
    """
    # Get user's index
    try:
        user_idx = model['user_ids'].index(user_id)
    except ValueError:
        print(f"User {user_id} not found in the model")
        return []
    
    # Get products the user has already rated
    user_data = model['user_item_matrix'].iloc[user_idx]
    rated_products = user_data[user_data > 0].index.tolist()
    
    # Get predictions for this user
    user_predictions = model['predictions'].iloc[user_idx]
    
    # Filter out products the user has already rated
    unrated_products = user_predictions.drop(rated_products)
    
    # Get top n recommendations
    top_recommendations = unrated_products.sort_values(ascending=False).index[:n_recommendations]
    
    return top_recommendations.tolist()

def create_sample_dataset():
    """
    Create a sample dataset with users, products, and ratings.
    
    Returns:
        Tuple of (users_df, products_df, ratings_df)
    """
    # Sample users
    users = pd.DataFrame([
        {'id': 1, 'name': 'Alice Smith'},
        {'id': 2, 'name': 'Bob Johnson'},
        {'id': 3, 'name': 'Charlie Brown'},
        {'id': 4, 'name': 'Diana Prince'},
        {'id': 5, 'name': 'Ethan Hunt'},
        {'id': 6, 'name': 'Fiona Gallagher'},
        {'id': 7, 'name': 'George Bailey'},
        {'id': 8, 'name': 'Hannah Baker'},
    ])
    
    # Sample products (using the same products from the main.py file)
    products = pd.DataFrame([
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
        # ...Add all products from main.py...
    ])
    
    # Sample ratings
    ratings = pd.DataFrame([
        {"userId": 1, "productId": 1, "rating": 4.5},
        {"userId": 1, "productId": 3, "rating": 5.0},
        {"userId": 1, "productId": 5, "rating": 4.0},
        {"userId": 2, "productId": 2, "rating": 4.5},
        {"userId": 2, "productId": 4, "rating": 5.0},
        {"userId": 2, "productId": 6, "rating": 3.5},
        {"userId": 3, "productId": 1, "rating": 3.5},
        # ...Add all ratings from main.py...
    ])
    
    return users, products, ratings

def main():
    """
    Main function to demonstrate creating a recommendation model.
    """
    # Create a data directory if it doesn't exist
    data_dir = Path(__file__).parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Create sample dataset
    users, products, ratings = create_sample_dataset()
    
    # Save the data
    users.to_json(data_dir / 'users.json', orient='records')
    products.to_json(data_dir / 'products.json', orient='records')
    ratings.to_json(data_dir / 'ratings.json', orient='records')
    
    # Create and save the model
    create_recommendation_model(ratings)
    
    print("Sample dataset and recommendation model created successfully")

if __name__ == "__main__":
    main()
