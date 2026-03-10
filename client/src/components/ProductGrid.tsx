"use client";

import { useState, useEffect } from "react";
import { Product } from "../types/api";
import { ProductCard } from "./ProductCard";
import { Loader2 } from "lucide-react";
import { useCart } from "@/context/CartContext";

export function ProductGrid() {
  const { addToCart } = useCart();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simuliamo una chiamata API. Quando ci sarà il backend, useremo fetch('http://localhost:8000/api/products')
    const fetchProducts = async () => {
      try {
        setLoading(true);
        // await fetch mock
        await new Promise(resolve => setTimeout(resolve, 800));
        
        const mockProducts: Product[] = [
          {
            id: "1",
            title: "Prodotto Demo 1",
            description: "Descrizione incredibile per un prodotto eccellente.",
            price: 29.99,
            availability: true,
            image_url: ""
          },
          {
            id: "2",
            title: "Prodotto Demo 2",
            description: "Prodotto esaurito per mostrarti lo stato disabilitato.",
            price: 49.50,
            availability: false,
            image_url: ""
          },
          {
            id: "3",
            title: "Smartphone Ultima Generazione",
            description: "Batteria a lunga durata e fotocamera 4K.",
            price: 799.00,
            availability: true,
            image_url: ""
          },
          {
            id: "4",
            title: "Cuffie Bluetooth",
            description: "Cancellazione attiva del rumore e suono spaziale.",
            price: 199.99,
            availability: true,
            image_url: ""
          }
        ];
        
        setProducts(mockProducts);
      } catch (error) {
        console.error("Errore nel fetch dei prodotti:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const handleAddToCart = (productId: string) => {
    addToCart(productId);
  };

  if (loading) {
    return (
      <div className="flex min-h-[400px] w-full items-center justify-center text-muted-foreground">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (products.length === 0) {
    return (
      <div className="flex min-h-[400px] w-full flex-col items-center justify-center gap-2 text-center">
        <h3 className="text-lg font-medium">Nessun prodotto trovato</h3>
        <p className="text-sm text-muted-foreground">Prova a cambiare filtri o cerca qualcos'altro.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {products.map((p) => (
        <ProductCard key={p.id} product={p} onAddToCart={handleAddToCart} />
      ))}
    </div>
  );
}
