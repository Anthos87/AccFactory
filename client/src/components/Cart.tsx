"use client";

import { X, ShoppingBag, Trash2 } from "lucide-react";
import { useCart } from "@/context/CartContext";
import { CartItem } from "../types/api";

export function Cart() {
  const { isCartOpen, setIsCartOpen, cart, updateQuantity, removeFromCart } = useCart();
  
  if (!isCartOpen) return null;
  const onClose = () => setIsCartOpen(false);

  return (
    <>
      <div 
        className="fixed inset-0 bg-black/40 z-50 transition-opacity" 
        onClick={onClose}
      />
      <div className="fixed inset-y-0 right-0 z-50 flex w-full max-w-sm flex-col bg-background shadow-xl transition-transform duration-300 ease-in-out sm:max-w-md border-l">
        <div className="flex items-center justify-between border-b px-4 py-4 sm:px-6">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <ShoppingBag className="w-5 h-5" /> Carrello
          </h2>
          <button onClick={onClose} className="rounded-full p-2 hover:bg-muted transition-colors">
            <span className="sr-only">Close cart</span>
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6">
          {!cart || cart.items.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-4 text-muted-foreground">
              <ShoppingBag className="w-12 h-12 opacity-20" />
              <p>Il carrello è vuoto</p>
            </div>
          ) : (
            <div className="space-y-6">
              {cart.items.map((item) => (
                <div key={item.id} className="flex py-2">
                  <div className="flex flex-1 flex-col mx-4">
                    <div className="flex justify-between text-base font-medium">
                      <h3>{item.product?.title || "Prodotto"}</h3>
                      <p className="ml-4">€{((item.product?.price || 0) * item.quantity).toFixed(2)}</p>
                    </div>
                    <div className="flex flex-1 items-end justify-between mt-2 text-sm">
                      <p className="text-muted-foreground">Qtà: {item.quantity}</p>
                      <button type="button" onClick={() => removeFromCart(item.id)} className="font-medium text-destructive hover:text-destructive/80">
                        Rimuovi
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="border-t px-4 py-6 sm:px-6 space-y-4">
          <div className="flex justify-between text-base font-medium">
            <p>Subtotale</p>
            <p>€{cart?.subtotal?.toFixed(2) || "0.00"}</p>
          </div>
          <p className="text-sm text-muted-foreground">
            Spedizione e tasse calcolate al checkout.
          </p>
          <div className="mt-6">
            <button
              className="w-full flex items-center justify-center rounded-md border border-transparent bg-primary px-6 py-3 text-base font-medium text-primary-foreground shadow-sm hover:bg-primary/90 disabled:opacity-50"
              disabled
            >
              Checkout
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
