# Runs on port 8000 by default

from typing import Union

from fastapi import FastAPI

items = [69, 420]

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {
        "item_id": item_id,
        "value": items[item_id],
        "q": q,
    }

# if __name__ == "__main__":
#     main()