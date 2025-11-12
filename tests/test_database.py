import tempfile
from core.database import Database


def test_database_connection():
    with tempfile.NamedTemporaryFile(suffix='.db') as tmp:
        # Creation
        db = Database(tmp.name)

        # Add Product
        pid = db.add_product("Item Teste", "url", "Loja", 100.0)
        assert pid is not None

        # Update Product
        db.update_price(pid, 90.0)
        db.insert_price_history(pid, 90.0)
        hist = db.get_price_history(pid)
        assert len(hist) == 1
        assert hist[0]['price'] == 90.0

        # Delete Product
        db.delete_product(pid)
        products = db.get_products(active_only=False)
        assert len(products) == 0

        # Close Database
        db.close()
