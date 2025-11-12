from core.database import Database

db = Database()

# Insert product
pid = db.add_product(
    name="Teclado Mecânico Redragon Kumara",
    url="https://example.com/teclado",
    store="ExampleStore",
    target_price=200.00
)
print(f"Produto inserido com ID: {pid}")

# Update product price and history
db.update_price(pid, 249.90)
db.insert_price_history(pid, 249.90)

# List products
for p in db.get_products():
    print(dict(p))

# History
hist = db.get_price_history(pid)
print("Histórico: ", [dict(h) for h in hist])

db.close()
