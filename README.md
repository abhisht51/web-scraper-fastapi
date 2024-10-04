# example-fastapi

Example of eventsourcing with FastAPI

## Getting Started

1. Install dependencies

```zsh
pip install -r requirements.txt
```

Ensure a redis server is running at localhost:6379 without authorisation

2. Start FastAPI process

```zsh
python main.py
```

3. Open local API docs [http://localhost:8000/docs](http://localhost:8000/docs)

4. To scrape from the web, use the following endpoint

```zsh
curl --location 'http://localhost:8000/pages?limit=2' \
--header 'Authorization: Bearer super-secret-token'
```

`save_img` flag is used to save all images locally on the server. This increases the API response time
