
import { useState } from 'react';
import { Star, StarHalf } from 'lucide-react';
import { Product } from '@/services/apiService';
import { cn } from '@/lib/utils';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

interface ProductCardProps {
  product: Product;
  onRate?: (productId: number, rating: number) => void;
}

const ProductCard = ({ product, onRate }: ProductCardProps) => {
  const [isHovering, setIsHovering] = useState(false);
  const [selectedRating, setSelectedRating] = useState(0);

  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;

    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <Star key={`star-${i}`} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
      );
    }

    if (hasHalfStar) {
      stars.push(
        <StarHalf key="half-star" className="h-4 w-4 fill-yellow-400 text-yellow-400" />
      );
    }

    // Add empty stars
    const emptyStars = 5 - stars.length;
    for (let i = 0; i < emptyStars; i++) {
      stars.push(
        <Star key={`empty-star-${i}`} className="h-4 w-4 text-gray-300" />
      );
    }

    return stars;
  };

  const renderRatingSelector = () => {
    return (
      <div className="flex items-center space-x-1">
        {[1, 2, 3, 4, 5].map((rating) => (
          <button
            key={`rate-${rating}`}
            onClick={() => {
              setSelectedRating(rating);
              if (onRate) onRate(product.id, rating);
            }}
            className="focus:outline-none"
            aria-label={`Rate ${rating} stars`}
          >
            <Star
              className={cn(
                "h-6 w-6 transition-colors",
                rating <= selectedRating
                  ? "fill-yellow-400 text-yellow-400"
                  : "text-gray-300 hover:text-yellow-300"
              )}
            />
          </button>
        ))}
      </div>
    );
  };

  return (
    <Card
      className={cn(
        "recommendation-card h-full flex flex-col",
        isHovering && "ring-1 ring-recommend-400"
      )}
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
    >
      <div className="relative pb-[56.25%] overflow-hidden bg-gray-100">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="absolute top-0 left-0 w-full h-full object-cover transition-transform duration-500"
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-200">
            <span className="text-gray-500">{product.name.charAt(0)}</span>
          </div>
        )}
        <div className="absolute top-2 right-2 bg-white dark:bg-gray-800 rounded-full px-2 py-1 text-xs font-semibold">
          {product.category}
        </div>
      </div>

      <CardHeader className="p-4 pb-0">
        <CardTitle className="text-lg">{product.name}</CardTitle>
      </CardHeader>

      <CardContent className="p-4 flex-grow">
        <div className="flex items-center mb-2">
          {renderStars(product.rating)}
          <span className="ml-2 text-sm text-gray-600">
            {product.rating.toFixed(1)}
          </span>
        </div>
        <p className="text-sm text-gray-600 line-clamp-2">
          {product.description}
        </p>
      </CardContent>

      {onRate && (
        <CardFooter className="p-4 pt-0 border-t">
          {renderRatingSelector()}
        </CardFooter>
      )}
    </Card>
  );
};

export default ProductCard;
