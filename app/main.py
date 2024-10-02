from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def root(page: str | None = "world"):
    return {"hello": "world"}
