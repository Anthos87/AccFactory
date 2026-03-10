"use client";

import Link from "next/link";
import { ShoppingCart } from "lucide-react";
import { Cart } from "./Cart";
import { useCart } from "@/context/CartContext";

export function Header() {
  const { cart, setIsCartOpen } = useCart();
  const itemCount = cart?.items.reduce((acc, item) => acc + item.quantity, 0) || 0;

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between p-4 px-8">
        <Link href="/" className="flex items-center space-x-2">
          <span className="inline-block font-bold text-xl">AccFactory Shop</span>
        </Link>
        <div className="flex flex-1 items-center justify-end space-x-4">
          <button
            onClick={() => setIsCartOpen(true)}
            className="flex items-center gap-2 rounded-md hover:bg-muted p-2 transition-colors relative"
          >
            <ShoppingCart className="h-5 w-5" />
            <span className="sr-only">Toggle cart</span>
            {itemCount > 0 && (
              <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-primary text-[10px] font-bold text-primary-foreground">
                {itemCount}
              </span>
            )}
          </button>
        </div>
      </div>
      <Cart />
    </header>
  );
}
