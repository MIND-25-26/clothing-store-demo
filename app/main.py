from fastapi import FastAPI, HTTPException
import os, psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

def get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)

# Data migration (better to move to separate file...)
with get_conn() as conn, conn.cursor() as cur:
    cur.execute("""
        -- ============================
        -- CREATE TABLES
        -- ============================

        -- Categories (just primary key)
        CREATE TABLE IF NOT EXISTS categories (
            category_id SERIAL PRIMARY KEY
        );

        -- Products (primary key + foreign key)
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            category_id INT REFERENCES categories(category_id)
        );

        -- Customers (primary key)
        CREATE TABLE IF NOT EXISTS customers (
            customer_id SERIAL PRIMARY KEY
        );

        -- Orders (primary key + foreign key)
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES customers(customer_id)
        );

        -- Order Items (primary key + foreign keys)
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id SERIAL PRIMARY KEY,
            order_id INT REFERENCES orders(order_id),
            product_id INT REFERENCES products(product_id)
        );

        -- ============================
        -- Add remaining columns
        -- 
        -- NOTE: If you need more columns, just add them here and run this whole file again!
        -- 
        -- ============================

        -- Categories
        ALTER TABLE categories ADD COLUMN IF NOT EXISTS name VARCHAR NOT NULL;

        -- Products
        ALTER TABLE products ADD COLUMN IF NOT EXISTS name VARCHAR NOT NULL;
        ALTER TABLE products ADD COLUMN IF NOT EXISTS price NUMERIC NOT NULL;
        ALTER TABLE products ADD COLUMN IF NOT EXISTS stock INT NOT NULL;

        -- Customers
        ALTER TABLE customers ADD COLUMN IF NOT EXISTS first_name VARCHAR NOT NULL;
        ALTER TABLE customers ADD COLUMN IF NOT EXISTS last_name VARCHAR NOT NULL;
        ALTER TABLE customers ADD COLUMN IF NOT EXISTS email VARCHAR UNIQUE NOT NULL;
        ALTER TABLE customers ADD COLUMN IF NOT EXISTS city VARCHAR;

        -- Orders
        ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_date DATE DEFAULT CURRENT_DATE;

        -- Order Items
        ALTER TABLE order_items ADD COLUMN IF NOT EXISTS quantity INT NOT NULL;
    """)

@app.get("/")
def get_root():
    return { "msg": "Clothing Store v0.1" }

# GET /categories 
@app.get("/categories")
def get_categories():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT category_id, name 
            FROM categories 
            ORDER BY category_id""")
        return cur.fetchall()

# GET /categories/{id}
@app.get("/categories/{category_id}")
def get_category(category_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT category_id, name 
            FROM categories 
            WHERE category_id = %s""", (category_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Category not found")
        return row

# POST /categories
@app.post("/categories", status_code=201)
def create_category(data: dict):
    name = data.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Missing 'name'")
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO categories (
                name
            ) VALUES (
                %s
            ) RETURNING category_id""", (name,))
        return cur.fetchone()