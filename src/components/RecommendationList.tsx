
import { Product } from '@/services/apiService';
import ProductCard from './ProductCard';
import { Skeleton } from "@/components/ui/skeleton";

interface RecommendationListProps {
  products: Product[];
  isLoading: boolean;
  onRate?: (productId: number, rating: number) => void;
}

const RecommendationList = ({ products, isLoading, onRate }: RecommendationListProps) => {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {Array.from({ length: 8 }).map((_, index) => (
          <div key={index} className="recommendation-card">
            <div className="w-full h-48 bg-gray-200 animate-pulse-light"></div>
            <div className="p-4">
              <Skeleton className="h-5 w-3/4 mb-2" />
              <div className="flex items-center mb-2">
                <Skeleton className="h-4 w-24" />
              </div>
              <Skeleton className="h-4 w-full mb-1" />
              <Skeleton className="h-4 w-3/4" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (products.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-xl text-gray-500">No recommendations available.</p>
        <p className="text-gray-400">Please select a user to see recommendations.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {products.map((product) => (
        <ProductCard 
          key={product.id} 
          product={product} 
          onRate={onRate} 
        />
      ))}
    </div>
  );
};

export default RecommendationList;
