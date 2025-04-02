
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/ThemeToggle";

const Header = () => {
  return (
    <header className="w-full bg-white dark:bg-gray-900 shadow-sm">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-recommend-500 to-recommend-700 flex items-center justify-center">
            <span className="text-white font-bold text-lg">CR</span>
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-recommend-600 to-recommend-800 bg-clip-text text-transparent">
            Comfy Recommendations
          </h1>
        </div>
        
        <div className="flex items-center space-x-4">
          <Button variant="outline" size="sm">About</Button>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
};

export default Header;
