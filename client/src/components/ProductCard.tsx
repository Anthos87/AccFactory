"use client";

import { Product } from "../types/api";
import { Plus } from "lucide-react";

interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: string) => void;
}

export function ProductCard({ product, onAddToCart }: ProductCardProps) {
  return (
    <div className="group relative flex flex-col overflow-hidden rounded-lg border bg-background shadow-sm transition-all hover:shadow-md">
      <div className="aspect-square bg-muted/50 overflow-hidden">
        <img
          src={product.image_url || `https://ui-avatars.com/api/?name=${encodeURIComponent(product.title)}&background=random&size=300`}
          alt={product.title}
          className="h-full w-full object-cover object-center transition-transform group-hover:scale-105"
        />
      </div>
      <div className="flex flex-1 flex-col space-y-2 p-4">
        <div className="flex justify-between items-start gap-2">
          <h3 className="text-sm font-medium leading-none line-clamp-2">
            {product.title}
          </h3>
          <p className="text-base font-bold whitespace-nowrap">
            €{product.price.toFixed(2)}
          </p>
        </div>
        <p className="text-sm text-muted-foreground line-clamp-2 flex-1">
          {product.description}
        </p>
        
        <div className="mt-auto pt-4 flex items-center justify-between">
          <span className={`text-xs font-medium px-2 py-1 rounded-full ${
            product.availability 
              ? "bg-green-100 text-green-700" 
              : "bg-red-100 text-red-700"
          }`}>
            {product.availability ? "Disponibile" : "Esaurito"}
          </span>
          <button
            onClick={() => onAddToCart(product.id)}
            disabled={!product.availability}
            className="flex items-center gap-2 rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-colors"
          >
            <Plus className="w-4 h-4" /> Aggiungi
          </button>
        </div>
      </div>
    </div>
  );
}
