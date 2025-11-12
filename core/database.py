import sqlite3
from pathlib import Path
from core.config import Config
from datetime import datetime


class Database:
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or Config.DATABASE_PATH
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.executescript("""
                             CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                url TEXT UNIQUE,
                                store TEXT,
                                target_price REAL,
                                last_price REAL,
                                active INTEGER DEFAULT 1
                             );

                             CREATE TABLE IF NOT EXISTS price_history (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                product_id INTEGER,
                                price REAL,
                                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY(product_id) REFERENCES products(id)
                            );
                             """)
        self.conn.commit()

    def add_product(
        self, name: str, url: str, store: str, target_price: float
    ):
        cursor = self.conn.cursor()
        cursor.execute("""
                       INSERT OR IGNORE INTO products (name, url, store,
                       target_price)
                       VALUES (?, ?, ?, ?)
                          """, (name, url, store, target_price))
        self.conn.commit()
        return cursor.lastrowid

    def get_products(self, active_only=True):
        cursor = self.conn.cursor()
        if active_only:
            cursor.execute("SELECT * FROM products WHERE active=1")
        else:
            cursor.execute("SELECT * FROM products")
        return cursor.fetchall()

    def update_price(self, product_id: int, new_price: float):
        cursor = self.conn.cursor()
        cursor.execute("""
                       UPDATE products
                       SET last_price = ?
                       WHERE id = ?
                       """, (new_price, product_id))
        self.conn.commit()

    def delete_product(self, product_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.conn.commit()

    def insert_price_history(self, product_id: int, price: float):
        cursor = self.conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
                       INSERT INTO price_history (product_id, price, date)
                       VALUES (?, ?, ?)
                       """, (product_id, price, now))
        self.conn.commit()

    def get_price_history(self, product_id: int, limit=10):
        cursor = self.conn.cursor()
        cursor.execute("""
                       SELECT price, date
                       FROM price_history
                       WHERE product_id = ?
                       ORDER BY date DESC
                       LIMIT ?
                       """, (product_id, limit))
        return cursor.fetchall()

    def close(self):
        self.conn.close()