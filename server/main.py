from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI(title="MVP E-commerce API", version="1.0.0")

# Modelli Pydantic (Mock)
class Product(BaseModel):
    id: str
    title: str
    description: str
    price: float
    availability: bool
    image_url: str

class CartItem(BaseModel):
    id: str
    product: Product
    quantity: int

class Cart(BaseModel):
    session_id: str
    items: List[CartItem]
    subtotal: float
    tax: float
    total: float

class AddToCartRequest(BaseModel):
    product_id: str
    quantity: int

class UpdateCartItemRequest(BaseModel):
    quantity: int

# Mock Database Segment
MOCK_PRODUCTS = [
    Product(id="1", title="Sneakers X", description="Sneakers da corsa", price=99.99, availability=True, image_url="https://via.placeholder.com/150"),
    Product(id="2", title="T-Shirt Y", description="Maglietta in cotone", price=19.99, availability=True, image_url="https://via.placeholder.com/150"),
    Product(id="3", title="Zaino Z", description="Zaino waterproof", price=49.99, availability=False, image_url="https://via.placeholder.com/150"),
]

@app.get("/api/products", response_model=List[Product])
def get_products(
    page: int = Query(1, ge=1),
    category: Optional[str] = None,
    q: Optional[str] = None
):
    results = MOCK_PRODUCTS
    if q:
        results = [p for p in results if q.lower() in p.title.lower() or q.lower() in p.description.lower()]
    # Implementazione mock della paginazione e categoria...
    return results

@app.get("/api/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    for p in MOCK_PRODUCTS:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Prodotto non trovato")

MOCK_CARTS = {}

def calculate_totals(cart: Cart):
    subtotal = sum(item.product.price * item.quantity for item in cart.items)
    tax = subtotal * 0.22  # Assuming 22% VAT
    total = subtotal + tax
    cart.subtotal = round(subtotal, 2)
    cart.tax = round(tax, 2)
    cart.total = round(total, 2)

@app.get("/api/cart/{session_id}", response_model=Cart)
def get_cart(session_id: str):
    if session_id not in MOCK_CARTS:
        MOCK_CARTS[session_id] = Cart(session_id=session_id, items=[], subtotal=0.0, tax=0.0, total=0.0)
    return MOCK_CARTS[session_id]

@app.post("/api/cart/{session_id}/items", status_code=201)
def add_to_cart(session_id: str, item: AddToCartRequest):
    if session_id not in MOCK_CARTS:
        MOCK_CARTS[session_id] = Cart(session_id=session_id, items=[], subtotal=0.0, tax=0.0, total=0.0)
    
    cart = MOCK_CARTS[session_id]
    
    # Check if item exists
    for cart_item in cart.items:
        if cart_item.product.id == item.product_id:
            cart_item.quantity += item.quantity
            calculate_totals(cart)
            return {"message": "Item quantity updated in cart"}

    # Find product
    product = next((p for p in MOCK_PRODUCTS if p.id == item.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_item = CartItem(id=f"item_{len(cart.items) + 1}", product=product, quantity=item.quantity)
    cart.items.append(new_item)
    calculate_totals(cart)
    return {"message": "Item added to cart"}

@app.put("/api/cart/{session_id}/items/{item_id}", response_model=Cart)
def update_cart_item(session_id: str, item_id: str, req: UpdateCartItemRequest):
    if session_id not in MOCK_CARTS:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart = MOCK_CARTS[session_id]
    for cart_item in cart.items:
        if cart_item.id == item_id:
            cart_item.quantity = req.quantity
            calculate_totals(cart)
            return cart
    
    raise HTTPException(status_code=404, detail="Item not found in cart")

@app.delete("/api/cart/{session_id}/items/{item_id}", status_code=204)
def delete_cart_item(session_id: str, item_id: str):
    if session_id not in MOCK_CARTS:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart = MOCK_CARTS[session_id]
    initial_length = len(cart.items)
    cart.items = [item for item in cart.items if item.id != item_id]
    
    if len(cart.items) == initial_length:
        raise HTTPException(status_code=404, detail="Item not found in cart")
        
    calculate_totals(cart)
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
