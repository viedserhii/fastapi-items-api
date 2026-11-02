from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Vied KS42 REST API", description="CRUD операції")

class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Назва елемента")
    description: str = Field(default="", max_length=500, description="Опис елемента")

class Item(ItemCreate):
    id: int

items: dict[int, Item] = {}
next_id = 1

@app.get("/api/items", response_model=list[Item], tags=["items"])
def list_items():
    return list(items.values())

@app.get("/api/items/{item_id}", response_model=Item, tags=["items"])
def get_item(item_id: int):
    item = items.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@app.post("/api/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["items"])
def create_item(payload: ItemCreate):
    global next_id
    item = Item(id=next_id, **payload.model_dump())
    items[next_id] = item
    next_id += 1
    return item

@app.put("/api/items/{item_id}", response_model=Item, tags=["items"])
def update_item(item_id: int, payload: ItemCreate):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    item = Item(id=item_id, **payload.model_dump())
    items[item_id] = item
    return item

@app.delete("/api/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["items"])
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del items[item_id]
    return None

@app.get("/health", tags=["service"])
def health():
    return {"status": "ok"}