
// API endpoints for our recommendation engine
const API_BASE_URL = 'http://127.0.0.1:8000';

// Types
export interface User {
  id: number;
  name: string;
}

export interface Product {
  id: number;
  name: string;
  category: string;
  description: string;
  rating: number;
  image_url: string;
}

export interface Rating {
  userId: number;
  productId: number;
  rating: number;
}

// API functions
export const getUsers = async (): Promise<User[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/users`);
    if (!response.ok) {
      throw new Error('Failed to fetch users');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching users:', error);
    return [];
  }
};

export const getProducts = async (): Promise<Product[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/products`);
    if (!response.ok) {
      throw new Error('Failed to fetch products');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching products:', error);
    return [];
  }
};

export const getRecommendations = async (userId: number): Promise<Product[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/recommendations/${userId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch recommendations');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    return [];
  }
};

export const submitRating = async (rating: Rating): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/ratings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(rating),
    });
    return response.ok;
  } catch (error) {
    console.error('Error submitting rating:', error);
    return false;
  }
};
