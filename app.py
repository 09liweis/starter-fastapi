from fastapi import FastAPI

from pydantic import BaseModel

from pymongo import MongoClient
from datetime import datetime

import os

mongodb_url = os.environ['MONGODB_URL']

client = MongoClient(mongodb_url)
todos_collection = client.heroku_6njptcbp.todos

app = FastAPI()


class Item(BaseModel):
  item_id: int


@app.get("/")
async def root():
  count = todos_collection.count_documents({})
  pending_count = todos_collection.count_documents({"status": "pending"})
  done_count = todos_collection.count_documents({"status": "done"})
  has_steps_count = todos_collection.count_documents(
      {"steps.0": {
          "$exists": True
      }})
  return {
      "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "name": "todo",
      "total": count,
      "pending": pending_count,
      "done": done_count,
      "has_steps_count": has_steps_count
  }


@app.get("/item/{item_id}")
async def read_item(item_id: int):
  return {"item_id": item_id}


@app.get("/items/")
async def list_items():
  return [{"item_id": 1, "name": "Foo"}, {"item_id": 2, "name": "Bar"}]


@app.post("/items/")
async def create_item(item: Item):
  return item
