from fastapi import FastAPI
from .scrapper import pages

app = FastAPI()


@app.get("/")
def root(page: str | None = "world"):
    return {"hello": "world"}


@app.get("/pages")
def pages_func(
    limit: int | None = 1, proxy_string: str | None = "", save_img: bool | None = False
):
    data = []
    page = 1
    while page <= limit:
        print(f"Scrapping data for page={page}")
        page_data = pages(page, proxy_string, save_img)
        data.extend(page_data)
        page += 1

    return {
        "message": f"Scrapped {len(data)} items from the first {limit} pages",
        "data": data,
    }
