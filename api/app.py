from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4

app = FastAPI(title="Example Items API", version="1.0.0")

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    in_stock: bool = True

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: str

items_db: dict[str, Item] = {}

@app.get("/")
def root():
    return {"message": "Welcome to the Items API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate):
    item_id = str(uuid4())
    new_item = Item(id=item_id, **item.dict())
    items_db[item_id] = new_item
    return new_item

@app.get("/items", response_model=List[Item])
def list_items(
    min_price: Optional[float] = Query(None, gt=0),
    in_stock: Optional[bool] = None,
):
    results = list(items_db.values())
    if min_price is not None:
        results = [i for i in results if i.price >= min_price]
    if in_stock is not None:
        results = [i for i in results if i.in_stock == in_stock]
    return results

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: str, updated_item: ItemCreate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    item = Item(id=item_id, **updated_item.dict())
    items_db[item_id] = item
    return item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return
