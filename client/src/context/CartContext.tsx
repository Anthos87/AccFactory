"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { Cart, CartItem } from "../types/api";

interface CartContextType {
  cart: Cart | null;
  addToCart: (productId: string) => void;
  removeFromCart: (itemId: string) => void;
  updateQuantity: (itemId: string, quantity: number) => void;
  isCartOpen: boolean;
  setIsCartOpen: (isOpen: boolean) => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [cart, setCart] = useState<Cart | null>(null);
  const [isCartOpen, setIsCartOpen] = useState(false);

  // Mock initial load
  useEffect(() => {
    setCart({
      session_id: "mock-session-123",
      items: [],
      subtotal: 0,
      tax: 0,
      total: 0,
    });
  }, []);

  const addToCart = (productId: string) => {
    console.log("Adding to cart globally:", productId);
    setIsCartOpen(true);
    // API Call goes here: POST /cart/{session_id}/items
    // Mocking update:
    setCart((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        items: [...prev.items, { id: Math.random().toString(), product: { id: productId } as any, quantity: 1 }],
      };
    });
  };

  const removeFromCart = (itemId: string) => {
    // API Call: DELETE /cart/{session_id}/items/{item_id}
  };

  const updateQuantity = (itemId: string, quantity: number) => {
    // API Call: PUT /cart/{session_id}/items/{item_id}
  };

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, updateQuantity, isCartOpen, setIsCartOpen }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
}
