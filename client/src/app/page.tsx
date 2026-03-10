import { ProductGrid } from "@/components/ProductGrid";

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      <div className="mb-8 space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Esplora il Catalogo</h1>
        <p className="text-muted-foreground text-lg">
          Scopri i nostri fantastici prodotti.
        </p>
      </div>
      <ProductGrid />
    </div>
  );
}
