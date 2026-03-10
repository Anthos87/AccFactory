export interface Product {
  id: string;
  title: string;
  description: string;
  price: number;
  availability: boolean;
  image_url: string;
}

export interface CartItem {
  id: string;
  product: Product;
  quantity: number;
}

export interface Cart {
  session_id: string;
  items: CartItem[];
  subtotal: number;
  tax: number;
  total: number;
}
