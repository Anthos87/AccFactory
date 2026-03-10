import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/Header";
import { CartProvider } from "@/context/CartContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AccFactory Shop MVP",
  description: "Catalogo Prodotti e Gestione Carrello MVP",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="it">
      <body className={`${inter.className} min-h-screen bg-background antialiased text-foreground flex flex-col`}>
        <CartProvider>
          <Header />
          <main className="flex-1">
            {children}
          </main>
        </CartProvider>
      </body>
    </html>
  );
}
