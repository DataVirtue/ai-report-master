import os
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine, text
from faker import Faker
import random
from backend.settings import (
    SOURCE_DB_USER,
    SOURCE_DB_PASSWORD,
    SOURCE_DB_HOST,
    SOURCE_DB_PORT,
    SOURCE_DB_TYPE,
)

class Command(BaseCommand):
    help = "Creates the ecommerce_seed database and populates it with sample data"

    def handle(self, *args, **kwargs):
        db_name = "ecommerce_seed"
        db_type = 'postgresql' if 'postgres' in SOURCE_DB_TYPE.lower() else SOURCE_DB_TYPE
        
        # Connect to default postgres DB to create the new database
        try:
            self.stdout.write(self.style.NOTICE(f"Connecting to default postgres database to create '{db_name}'..."))
            engine_default = create_engine(
                f"{db_type}://{SOURCE_DB_USER}:{SOURCE_DB_PASSWORD}@{SOURCE_DB_HOST}:{SOURCE_DB_PORT}/postgres"
            )
            with engine_default.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
                res = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'"))
                if not res.fetchone():
                    self.stdout.write(self.style.NOTICE(f"Creating database {db_name}..."))
                    conn.execute(text(f"CREATE DATABASE {db_name}"))
                    self.stdout.write(self.style.SUCCESS(f"Database {db_name} created successfully."))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Database {db_name} already exists."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating database: {e}"))
            return

        # Connect to the newly created seed database
        self.stdout.write(self.style.NOTICE(f"Connecting to {db_name} to generate schema and data..."))
        engine_seed = create_engine(
            f"{db_type}://{SOURCE_DB_USER}:{SOURCE_DB_PASSWORD}@{SOURCE_DB_HOST}:{SOURCE_DB_PORT}/{db_name}"
        )

        with engine_seed.connect() as conn:
            # Create Schema
            self.stdout.write(self.style.NOTICE("Creating tables..."))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                email VARCHAR(200) UNIQUE,
                date_joined TIMESTAMP,
                country VARCHAR(100)
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200),
                category VARCHAR(100),
                price DECIMAL(10, 2),
                stock_quantity INT,
                created_at TIMESTAMP
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                customer_id INT REFERENCES customers(id),
                status VARCHAR(50),
                total_amount DECIMAL(10, 2),
                order_date TIMESTAMP
            );
            """))
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id INT REFERENCES orders(id),
                product_id INT REFERENCES products(id),
                quantity INT,
                unit_price DECIMAL(10, 2)
            );
            """))
            conn.commit()
            
            # Check if data already exists to prevent duplicate seeding
            res = conn.execute(text("SELECT COUNT(*) FROM customers"))
            if res.scalar() > 0:
                self.stdout.write(self.style.SUCCESS("Database is already seeded. Exiting."))
                return

            self.stdout.write(self.style.NOTICE("Injecting data... this may take a moment."))
            fake = Faker()
            
            # Insert Customers
            customers_data = []
            for _ in range(100):
                customers_data.append({
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'email': fake.unique.email(),
                    'date_joined': fake.date_time_between(start_date='-2y', end_date='now').strftime("%Y-%m-%d %H:%M:%S"),
                    'country': fake.country()
                })
            conn.execute(text("""
                INSERT INTO customers (first_name, last_name, email, date_joined, country) 
                VALUES (:first_name, :last_name, :email, :date_joined, :country)
            """), customers_data)
            
            # Insert Products
            categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Toys']
            products_data = []
            for _ in range(50):
                products_data.append({
                    'name': fake.catch_phrase(),
                    'category': random.choice(categories),
                    'price': round(random.uniform(5.0, 500.0), 2),
                    'stock_quantity': random.randint(0, 1000),
                    'created_at': fake.date_time_between(start_date='-3y', end_date='-2y').strftime("%Y-%m-%d %H:%M:%S")
                })
            conn.execute(text("""
                INSERT INTO products (name, category, price, stock_quantity, created_at)
                VALUES (:name, :category, :price, :stock_quantity, :created_at)
            """), products_data)

            # Insert Orders & Order Items
            res = conn.execute(text("SELECT id FROM customers"))
            customer_ids = [row[0] for row in res.fetchall()]
            
            res = conn.execute(text("SELECT id, price FROM products"))
            products = {row[0]: row[1] for row in res.fetchall()}
            product_ids = list(products.keys())

            statuses = ['Pending', 'Shipped', 'Delivered', 'Cancelled']
            
            orders_data = []
            for _ in range(300):
                orders_data.append({
                    'customer_id': random.choice(customer_ids),
                    'status': random.choice(statuses),
                    'total_amount': 0, # Will update later or ignore for simple seed
                    'order_date': fake.date_time_between(start_date='-1y', end_date='now').strftime("%Y-%m-%d %H:%M:%S")
                })
            
            # We insert orders one by one to get their IDs, returning ids is easier in PostgreSQL
            if orders_data:
                order_ids = []
                for order in orders_data:
                    res = conn.execute(text("""
                        INSERT INTO orders (customer_id, status, total_amount, order_date)
                        VALUES (:customer_id, :status, :total_amount, :order_date)
                        RETURNING id
                    """), [order])
                    order_ids.append(res.scalar())

                order_items_data = []
                for order_id in order_ids:
                    # 1 to 5 items per order
                    num_items = random.randint(1, 5)
                    order_total = 0
                    
                    chosen_products = random.sample(product_ids, num_items)
                    for pid in chosen_products:
                        qty = random.randint(1, 3)
                        price = products[pid]
                        order_total += float(price) * qty
                        order_items_data.append({
                            'order_id': order_id,
                            'product_id': pid,
                            'quantity': qty,
                            'unit_price': price
                        })
                    
                    # Update order total
                    conn.execute(text("UPDATE orders SET total_amount = :total WHERE id = :id"), [{'total': order_total, 'id': order_id}])

                if order_items_data:
                    conn.execute(text("""
                        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                        VALUES (:order_id, :product_id, :quantity, :unit_price)
                    """), order_items_data)

            conn.commit()
            self.stdout.write(self.style.SUCCESS("Data successfully injected!"))
