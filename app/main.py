from fastapi import FastAPI
from .scrapper import pages

app = FastAPI()


@app.get("/")
def root(page: str | None = "world"):
    return {"hello": "world"}


@app.get("/pages")
def pages_func(page: str | None = 1, save_img: bool | None = False):
    data = pages(page, save_img)

    return {"message": f"Scrapped {len(data)} items from page={page}", "data": data}
