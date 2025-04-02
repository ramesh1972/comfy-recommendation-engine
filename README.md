
# Comfy Recommendation Engine

A collaborative filtering recommendation engine built with FastAPI backend and React frontend.

## Project Overview

This project demonstrates how to create a recommendation system using collaborative filtering techniques. The system recommends products to users based on their past ratings and the ratings of similar users.

## Features

- User-based collaborative filtering
- FastAPI backend that serves recommendations from a pre-trained model
- React frontend with a modern UI
- Rating system to provide feedback
- Responsive design

## Tech Stack

### Frontend
- React
- TypeScript
- Tailwind CSS
- shadcn/ui components
- React Query for data fetching

### Backend
- FastAPI
- Python
- Collaborative filtering with matrix factorization
- Pickle for model serialization

## How to Run

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend will run on http://localhost:8000 with API documentation available at http://localhost:8000/docs

### Frontend

```bash
npm run dev
```

The frontend development server will run on http://localhost:8080

## How It Works

1. The system loads user ratings data from a JSON file or database
2. A collaborative filtering model is built using this data
3. The model is saved as a pickle file for quick loading
4. When a user requests recommendations, the system:
   - Finds users with similar taste patterns
   - Recommends products that these similar users have rated highly
   - Returns personalized product recommendations

## API Endpoints

- GET `/users` - Get all users
- GET `/products` - Get all products
- GET `/recommendations/{user_id}` - Get recommendations for a specific user
- POST `/ratings` - Submit a new user rating
- POST `/generate_model` - Manually regenerate the recommendation model

## Demo Mode

If the backend is not running, the frontend will automatically switch to demo mode with sample data.
