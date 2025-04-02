
import { useState, useEffect } from 'react';
import { toast } from "sonner";
import { User, Product, getUsers, getProducts, getRecommendations, submitRating } from '@/services/apiService';
import Header from '@/components/Header';
import UserSelector from '@/components/UserSelector';
import RecommendationList from '@/components/RecommendationList';
import ExplanationSection from '@/components/ExplanationSection';
import { Button } from '@/components/ui/button';

const Index = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [recommendations, setRecommendations] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');

  // Fetch users from API
  useEffect(() => {
    const fetchUsers = async () => {
      const usersList = await getUsers();
      if (usersList.length > 0) {
        setUsers(usersList);
        setBackendStatus('connected');
      } else {
        setBackendStatus('disconnected');
      }
    };
    
    fetchUsers();
  }, []);

  // Fetch recommendations when user changes
  useEffect(() => {
    if (selectedUserId !== null) {
      fetchRecommendationsForUser(selectedUserId);
    }
  }, [selectedUserId]);

  const fetchRecommendationsForUser = async (userId: number) => {
    setIsLoading(true);
    
    try {
      const recommendedProducts = await getRecommendations(userId);
      setRecommendations(recommendedProducts);
      if (recommendedProducts.length > 0) {
        toast.success(`Found ${recommendedProducts.length} recommendations for user!`);
      } else {
        toast.info("No recommendations found for this user.");
      }
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      toast.error("Failed to fetch recommendations. Is the backend running?");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectUser = (userId: number) => {
    setSelectedUserId(userId);
  };

  const handleRateProduct = async (productId: number, rating: number) => {
    if (!selectedUserId) {
      toast.error("Please select a user first");
      return;
    }

    const success = await submitRating({
      userId: selectedUserId,
      productId,
      rating
    });

    if (success) {
      toast.success(`You rated product #${productId} with ${rating} stars!`);
    } else {
      toast.error("Failed to submit rating");
    }
  };

  // Show demo data when backend is not available
  const loadDemoData = () => {
    // Generate mock users
    const mockUsers: User[] = [
      { id: 1, name: "Alice Smith" },
      { id: 2, name: "Bob Johnson" },
      { id: 3, name: "Charlie Brown" },
      { id: 4, name: "Diana Prince" },
    ];
    
    setUsers(mockUsers);
    setBackendStatus('disconnected');
    
    // Mock recommendations will be loaded when a user is selected
  };

  // Generate mock recommendations
  const loadMockRecommendations = () => {
    const mockProducts: Product[] = [
      {
        id: 1,
        name: "Comfortable Office Chair",
        category: "Furniture",
        description: "Ergonomic office chair with lumbar support and breathable mesh back.",
        rating: 4.5,
        image_url: "https://images.unsplash.com/photo-1589384267710-7a25bc5b4862?q=80&w=500&auto=format&fit=crop"
      },
      {
        id: 2,
        name: "Adjustable Standing Desk",
        category: "Furniture",
        description: "Electric height-adjustable desk with memory settings and spacious work surface.",
        rating: 4.8,
        image_url: "https://images.unsplash.com/photo-1518655048521-f130df041f66?q=80&w=500&auto=format&fit=crop"
      },
      {
        id: 3,
        name: "Mechanical Keyboard",
        category: "Electronics",
        description: "Tactile mechanical keyboard with customizable RGB lighting and programmable keys.",
        rating: 4.3,
        image_url: "https://images.unsplash.com/photo-1561112078-7d24e04c3407?q=80&w=500&auto=format&fit=crop"
      },
      {
        id: 4,
        name: "Ultrawide Monitor",
        category: "Electronics",
        description: "34-inch curved ultrawide monitor with high resolution and excellent color accuracy.",
        rating: 4.7,
        image_url: "https://images.unsplash.com/photo-1607706009771-cbcce7b9d83c?q=80&w=500&auto=format&fit=crop"
      },
      {
        id: 5,
        name: "Noise-Canceling Headphones",
        category: "Audio",
        description: "Premium wireless headphones with active noise cancellation and long battery life.",
        rating: 4.6,
        image_url: "https://images.unsplash.com/photo-1546435770-a3e426bf472b?q=80&w=500&auto=format&fit=crop"
      },
      {
        id: 6,
        name: "Smart LED Desk Lamp",
        category: "Lighting",
        description: "Adjustable LED desk lamp with multiple color temperatures and brightness levels.",
        rating: 4.2,
        image_url: "https://images.unsplash.com/photo-1534105615256-13940a56ff44?q=80&w=500&auto=format&fit=crop"
      },
      {
        id: 7,
        name: "Laptop Stand",
        category: "Accessories",
        description: "Adjustable aluminum laptop stand for improved ergonomics and cooling.",
        rating: 4.4,
        image_url: "https://images.unsplash.com/photo-1675365889958-1f217bf8538e?q=80&w=500&auto=format&fit=crop"
      },
      {
        id: 8,
        name: "Wireless Mouse",
        category: "Electronics",
        description: "Ergonomic wireless mouse with adjustable DPI and quiet click buttons.",
        rating: 4.1,
        image_url: "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?q=80&w=500&auto=format&fit=crop"
      }
    ];
    
    setIsLoading(true);
    setTimeout(() => {
      setRecommendations(mockProducts);
      setIsLoading(false);
      toast.info("Showing demo recommendations (backend not connected)");
    }, 1000);
  };

  const handleSelectUserInDemoMode = (userId: number) => {
    setSelectedUserId(userId);
    loadMockRecommendations();
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      
      <main className="flex-grow container mx-auto px-4 py-8">
        <section className="mb-10">
          <h1 className="text-4xl font-bold mb-6 text-center">
            Personalized Product Recommendations
          </h1>
          <p className="text-lg text-center mb-8 max-w-2xl mx-auto text-muted-foreground">
            Experience AI-powered recommendations based on collaborative filtering.
            Select a user to see products recommended just for them.
          </p>
          
          {backendStatus === 'checking' && (
            <div className="text-center mb-8">
              <p className="text-gray-500">Checking connection to backend...</p>
            </div>
          )}
          
          {backendStatus === 'disconnected' && (
            <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-8 max-w-2xl mx-auto">
              <h3 className="font-medium text-amber-800 mb-2">Backend Not Connected</h3>
              <p className="text-amber-700 mb-4">
                The recommendation engine backend is not connected. 
                This demo is running in standalone mode with mock data.
              </p>
              <div className="flex justify-center">
                <Button onClick={loadDemoData} variant="outline" className="bg-amber-100">
                  Load Demo Data
                </Button>
              </div>
            </div>
          )}
          
          <div className="mb-8">
            <UserSelector 
              users={users} 
              onSelectUser={backendStatus === 'connected' ? handleSelectUser : handleSelectUserInDemoMode} 
            />
          </div>
        </section>
        
        <section className="mb-12">
          <h2 className="text-2xl font-semibold mb-6">Recommended for You</h2>
          <RecommendationList 
            products={recommendations} 
            isLoading={isLoading} 
            onRate={handleRateProduct}
          />
        </section>
        
        <section className="mb-10">
          <ExplanationSection />
        </section>
      </main>
      
      <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 py-6">
        <div className="container mx-auto px-4">
          <div className="text-center text-gray-500 dark:text-gray-400">
            <p>Collaborative Filtering Recommendation Engine Demo</p>
            <p className="text-sm mt-2">Powered by FastAPI and React</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
