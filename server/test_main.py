"""
QA Agent - Test Suite per AccFactory Backend (FastAPI)
Conforme al contratto API definito in /docs/api_contract.md
"""
import pytest
from fastapi.testclient import TestClient
from main import app, MOCK_CARTS

client = TestClient(app)


# ============================================================
# FIXTURE
# ============================================================
@pytest.fixture(autouse=True)
def reset_cart_state():
    """Resetta lo stato del carrello prima di ogni test."""
    MOCK_CARTS.clear()
    yield
    MOCK_CARTS.clear()


# ============================================================
# TEST: GET /api/products
# ============================================================
class TestGetProducts:

    def test_returns_all_products(self):
        """Deve restituire tutti i prodotti disponibili."""
        response = client.get("/api/products")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_product_schema(self):
        """Ogni prodotto deve avere i campi definiti nel contratto."""
        response = client.get("/api/products")
        product = response.json()[0]
        assert "id" in product
        assert "title" in product
        assert "description" in product
        assert "price" in product
        assert "availability" in product
        assert "image_url" in product

    def test_search_by_query_title(self):
        """Il parametro ?q= deve filtrare per titolo."""
        response = client.get("/api/products?q=Sneakers")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Sneakers X"

    def test_search_by_query_description(self):
        """Il parametro ?q= deve filtrare anche per descrizione."""
        response = client.get("/api/products?q=waterproof")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Zaino Z"

    def test_search_case_insensitive(self):
        """La ricerca deve essere case-insensitive."""
        response = client.get("/api/products?q=SNEAKERS")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_search_no_results(self):
        """Una query senza risultati deve restituire lista vuota."""
        response = client.get("/api/products?q=prodotto_inesistente_xyz")
        assert response.status_code == 200
        assert response.json() == []

    def test_page_param_accepted(self):
        """Il parametro ?page= deve essere accettato senza errori."""
        response = client.get("/api/products?page=1")
        assert response.status_code == 200

    def test_page_param_invalid(self):
        """Il parametro ?page=0 deve restituire 422 (ge=1)."""
        response = client.get("/api/products?page=0")
        assert response.status_code == 422


# ============================================================
# TEST: GET /api/products/{product_id}
# ============================================================
class TestGetProductById:

    def test_existing_product(self):
        """Deve restituire il prodotto corretto per un ID valido."""
        response = client.get("/api/products/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "1"
        assert data["title"] == "Sneakers X"
        assert data["price"] == 99.99

    def test_all_mock_products_accessible(self):
        """Tutti i prodotti mock devono essere accessibili."""
        for pid in ["1", "2", "3"]:
            response = client.get(f"/api/products/{pid}")
            assert response.status_code == 200

    def test_product_not_found(self):
        """Deve restituire 404 per un ID inesistente."""
        response = client.get("/api/products/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Prodotto non trovato"

    def test_product_availability_field(self):
        """Il campo availability deve essere il valore corretto."""
        r_available = client.get("/api/products/1")
        assert r_available.json()["availability"] is True

        r_unavailable = client.get("/api/products/3")
        assert r_unavailable.json()["availability"] is False


# ============================================================
# TEST: GET /api/cart/{session_id}
# ============================================================
class TestGetCart:

    def test_new_session_creates_empty_cart(self):
        """Una sessione nuova deve creare un carrello vuoto."""
        response = client.get("/api/cart/session_test_new")
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "session_test_new"
        assert data["items"] == []
        assert data["subtotal"] == 0.0
        assert data["tax"] == 0.0
        assert data["total"] == 0.0

    def test_cart_schema(self):
        """Il carrello deve rispettare lo schema del contratto API."""
        response = client.get("/api/cart/session_schema_test")
        data = response.json()
        assert "session_id" in data
        assert "items" in data
        assert "subtotal" in data
        assert "tax" in data
        assert "total" in data


# ============================================================
# TEST: POST /api/cart/{session_id}/items
# ============================================================
class TestAddToCart:

    def test_add_valid_product(self):
        """Deve aggiungere un prodotto valido al carrello."""
        response = client.post(
            "/api/cart/session_add/items",
            json={"product_id": "1", "quantity": 2}
        )
        assert response.status_code == 201
        assert "message" in response.json()

    def test_add_product_updates_cart(self):
        """Dopo l'aggiunta, il carrello deve contenere l'item."""
        client.post("/api/cart/session_upd/items", json={"product_id": "1", "quantity": 1})
        cart = client.get("/api/cart/session_upd").json()
        assert len(cart["items"]) == 1
        assert cart["items"][0]["product"]["id"] == "1"

    def test_add_same_product_increases_quantity(self):
        """Aggiungere lo stesso prodotto due volte deve incrementare la quantità."""
        sid = "session_qty"
        client.post(f"/api/cart/{sid}/items", json={"product_id": "2", "quantity": 1})
        client.post(f"/api/cart/{sid}/items", json={"product_id": "2", "quantity": 3})
        cart = client.get(f"/api/cart/{sid}").json()
        assert len(cart["items"]) == 1
        assert cart["items"][0]["quantity"] == 4

    def test_add_nonexistent_product(self):
        """Deve restituire 404 per un product_id inesistente."""
        response = client.post(
            "/api/cart/session_err/items",
            json={"product_id": "999", "quantity": 1}
        )
        assert response.status_code == 404

    def test_cart_totals_calculated_after_add(self):
        """I totali del carrello devono essere calcolati correttamente (IVA 22%)."""
        sid = "session_totals"
        # Sneakers X: 99.99 * 1
        client.post(f"/api/cart/{sid}/items", json={"product_id": "1", "quantity": 1})
        cart = client.get(f"/api/cart/{sid}").json()
        assert cart["subtotal"] == 99.99
        expected_tax = round(99.99 * 0.22, 2)
        assert cart["tax"] == expected_tax
        assert cart["total"] == round(99.99 + expected_tax, 2)


# ============================================================
# TEST: PUT /api/cart/{session_id}/items/{item_id}
# ============================================================
class TestUpdateCartItem:

    def setup_cart(self, session_id: str, product_id: str = "1", quantity: int = 1):
        client.post(f"/api/cart/{session_id}/items", json={"product_id": product_id, "quantity": quantity})
        cart = client.get(f"/api/cart/{session_id}").json()
        return cart["items"][0]["id"]

    def test_update_quantity(self):
        """Deve aggiornare la quantità dell'item."""
        sid = "session_put"
        item_id = self.setup_cart(sid, "1", 1)
        response = client.put(f"/api/cart/{sid}/items/{item_id}", json={"quantity": 5})
        assert response.status_code == 200
        data = response.json()
        item = next(i for i in data["items"] if i["id"] == item_id)
        assert item["quantity"] == 5

    def test_update_recalculates_totals(self):
        """L'aggiornamento della quantità deve ricalcolare i totali."""
        sid = "session_put_totals"
        item_id = self.setup_cart(sid, "2", 1)  # T-Shirt Y: 19.99
        client.put(f"/api/cart/{sid}/items/{item_id}", json={"quantity": 3})
        cart = client.get(f"/api/cart/{sid}").json()
        expected_subtotal = round(19.99 * 3, 2)
        assert cart["subtotal"] == expected_subtotal

    def test_update_cart_not_found(self):
        """Deve restituire 404 se la sessione non esiste."""
        response = client.put("/api/cart/ghost_session/items/item_1", json={"quantity": 2})
        assert response.status_code == 404

    def test_update_item_not_found(self):
        """Deve restituire 404 se l'item_id non esiste nel carrello."""
        sid = "session_put_err"
        self.setup_cart(sid, "1", 1)
        response = client.put(f"/api/cart/{sid}/items/item_inesistente", json={"quantity": 2})
        assert response.status_code == 404


# ============================================================
# TEST: DELETE /api/cart/{session_id}/items/{item_id}
# ============================================================
class TestDeleteCartItem:

    def setup_cart(self, session_id: str, product_id: str = "1", quantity: int = 1):
        client.post(f"/api/cart/{session_id}/items", json={"product_id": product_id, "quantity": quantity})
        cart = client.get(f"/api/cart/{session_id}").json()
        return cart["items"][0]["id"]

    def test_delete_existing_item(self):
        """Deve rimuovere l'item e restituire 204."""
        sid = "session_del"
        item_id = self.setup_cart(sid, "1", 1)
        response = client.delete(f"/api/cart/{sid}/items/{item_id}")
        assert response.status_code == 204

    def test_cart_empty_after_delete(self):
        """Dopo la cancellazione, il carrello deve essere vuoto."""
        sid = "session_del_check"
        item_id = self.setup_cart(sid, "1", 1)
        client.delete(f"/api/cart/{sid}/items/{item_id}")
        cart = client.get(f"/api/cart/{sid}").json()
        assert len(cart["items"]) == 0
        assert cart["total"] == 0.0

    def test_delete_cart_not_found(self):
        """Deve restituire 404 se la sessione non esiste."""
        response = client.delete("/api/cart/ghost_session/items/item_1")
        assert response.status_code == 404

    def test_delete_item_not_found(self):
        """Deve restituire 404 se l'item_id non esiste."""
        sid = "session_del_err"
        self.setup_cart(sid, "1", 1)
        response = client.delete(f"/api/cart/{sid}/items/item_inesistente")
        assert response.status_code == 404

    def test_totals_recalculated_after_delete(self):
        """I totali devono essere ricalcolati dopo la rimozione."""
        sid = "session_del_totals"
        # Aggiungo due prodotti diversi
        client.post(f"/api/cart/{sid}/items", json={"product_id": "1", "quantity": 1})  # 99.99
        client.post(f"/api/cart/{sid}/items", json={"product_id": "2", "quantity": 1})  # 19.99
        cart = client.get(f"/api/cart/{sid}").json()
        item1_id = cart["items"][0]["id"]
        # Rimuovo il primo
        client.delete(f"/api/cart/{sid}/items/{item1_id}")
        cart_after = client.get(f"/api/cart/{sid}").json()
        assert cart_after["subtotal"] == 19.99
