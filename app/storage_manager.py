from abc import ABC, abstractmethod
import json
import os
import redis
from .logger import Logger

logger = Logger("Atlys Storage: ")


class Storage(ABC):
    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def store_data(self, products):
        pass


class JSONFileStorage(Storage):
    def __init__(self, file_path="products.json"):
        self.file_path = file_path

        # Create the JSON file if it doesn't exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def load_data(self):
        with open(self.file_path, "r") as file:
            return json.load(file)

    def store_data(self, products):
        # Append new products to the JSON file
        with open(self.file_path, "w") as file:
            json.dump(products, file, indent=4)


# SQL Storage Class (Future Implementation)
class SQLStorage(Storage):
    def __init__(self, db_path="products.db"):
        self.db_path = db_path
        # uncomment after installing sqlite3 package
        # self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        # Boilerplate code for creating table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_title TEXT PRIMARY KEY,
                product_price REAL,
                path_to_image TEXT
            )
        """)
        self.connection.commit()

    def load_data(self):
        # Placeholder for retrieving data from SQL
        return None

    def store_data(self, products):
        # Placeholder for storing data in SQL
        logger.info("Storing data in SQL storage (not implemented).")

    def close_connection(self):
        # self.connection.close()
        pass


class RedisCache:
    def __init__(self, host="localhost", port=6379, db=0):
        self.redis_client = redis.Redis(
            host=host, port=port, db=db, decode_responses=True
        )

    def get_cached_products(self, product_titles):
        # Use pipeline to get multiple product prices in one call
        pipeline = self.redis_client.pipeline()
        for title in product_titles:
            pipeline.get(f"product:{title}")
        return pipeline.execute()

    def cache_products(self, products):
        # Use pipeline to set multiple product prices in one call
        pipeline = self.redis_client.pipeline()
        for product in products:
            pipeline.set(
                f"product:{product["product_title"]}", product["product_price"]
            )
        pipeline.execute()


class StorageManager:
    def __init__(self, storage: Storage, cache: RedisCache):
        self.storage = storage
        self.cache = cache

    def set_storage(self, storage: Storage):
        self.storage = storage  # Future

    def store_products(self, products):
        existing_data = self.storage.load_data()
        existing_titles = {
            product["product_title"]: product for product in existing_data
        }

        product_titles = [product["product_title"] for product in products]
        cached_prices = self.cache.get_cached_products(product_titles)

        products_to_update = []
        products_to_cache = []

        for product, cached_price in zip(products, cached_prices):
            product_title = product["product_title"]
            product_price = product["product_price"]

            # Check if the product is cached and if the price has changed
            if cached_price is not None and float(cached_price) == product_price:
                # Product is already cached and has the same price, skip it
                continue

            if (
                product_title not in existing_titles
                or existing_titles[product_title]["product_price"] != product_price
            ):
                existing_titles[product_title] = product
                products_to_update.append(product)

            products_to_cache.append(product)

        if products_to_update:
            updated_data = list(existing_titles.values())
            self.storage.store_data(updated_data)
            logger.info(
                f"Stored {len(products_to_update)} new or updated products to storage."
            )

        # Cache new or updated products in Redis
        if products_to_cache:
            self.cache.cache_products(products_to_cache)
            logger.info(
                f"Cached {len(products_to_cache)} new or updated products in Redis."
            )
