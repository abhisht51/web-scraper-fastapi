from fastapi import FastAPI, Depends
from .scrapper import pages
from .auth import verify_token
from .storage_manager import JSONFileStorage, RedisCache, StorageManager
from .logger import Logger

app = FastAPI()
logger = Logger("Atlys: ")


@app.get("/")
def root(page: str | None = "world"):
    return {"message": "Hello from web scrapper"}


@app.get("/pages", dependencies=[Depends(verify_token)])
def pages_func(
    limit: int | None = 1, proxy_string: str | None = "", save_img: bool | None = False
):
    data = []
    page = 1  # sometimes page 1 stops responding
    while page <= limit:
        logger.info(f"Scrapping data for page={page}")
        page_data = pages(page, proxy_string, save_img)
        data.extend(page_data)
        page += 1

    json_storage = JSONFileStorage()
    redis_cache = RedisCache()

    storage_manager = StorageManager(json_storage, redis_cache)
    storage_manager.store_products(data)

    return {
        "message": f"Scrapped {len(data)} items from the first {limit} page",
    }
