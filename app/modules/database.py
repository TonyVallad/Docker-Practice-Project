import os
import time
import psycopg2
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

# Establish the PostgreSQL connection
def connect_with_retry(retries=10, delay=5):
    for i in range(retries):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            return conn, cursor
        except psycopg2.OperationalError as e:
            print(f"Database connection failed. Retrying {i + 1}/{retries}...")
            time.sleep(delay)
    raise Exception("Could not connect to the database after multiple retries")

# Establish connection with retry
conn, cursor = connect_with_retry()

# Database initialization function
def initialize_database():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            product_name TEXT,
            pnns_groups_1 TEXT,
            energy_kcal_100g FLOAT,
            fat_100g FLOAT,
            saturated_fat_100g FLOAT,
            sugars_100g FLOAT,
            fiber_100g FLOAT,
            proteins_100g FLOAT,
            salt_100g FLOAT,
            sodium_100g FLOAT,
            fruits_vegetables_nuts_estimate_from_ingredients_100g FLOAT,
            prediction_result TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()

# Function to insert prediction data
def insert_prediction(data, prediction):
    cursor.execute('''
        INSERT INTO predictions (
            product_name, pnns_groups_1, energy_kcal_100g, fat_100g,
            saturated_fat_100g, sugars_100g, fiber_100g, proteins_100g,
            salt_100g, sodium_100g, fruits_vegetables_nuts_estimate_from_ingredients_100g,
            prediction_result, timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        data['product_name'], data['pnns_groups_1'], data['energy_kcal_100g'],
        data['fat_100g'], data['saturated_fat_100g'], data['sugars_100g'],
        data['fiber_100g'], data['proteins_100g'], data['salt_100g'],
        data['sodium_100g'], data['fruits_vegetables_nuts_estimate_from_ingredients_100g'],
        prediction, datetime.now()
    ))
    conn.commit()
