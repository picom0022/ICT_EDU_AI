from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    id : int
    name : str
    price : float

items = [
    {"id": 1, "name": "Apple", "price":5000},
    {"id": 2, "name": "Mango", "price":6000},
    {"id": 3, "name": "Banana", "price":4500}
]

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# FastAPI 에게 반환할 응답의 데이터 모델이 Item 객체들의 리스트 형식
@app.get ("/items", response_model = List[Item])
def get_items():
    return items

@app.post("/items", response_model =List[Item])
def add_item(item: Item):
    # 중복 체크
    for existing_item in items:
        if existing_item['id'] == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items.append(item.dict())
    return items

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")