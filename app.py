from fastapi import FastAPI

from pydantic import BaseModel

from pymongo import MongoClient
from datetime import datetime
from time import perf_counter

import os

mongodb_url = os.environ['MONGODB_URL']

client = MongoClient(mongodb_url)
todos_collection = client.heroku_6njptcbp.todos

app = FastAPI()


class Item(BaseModel):
  item_id: int


def getTodoCounts(todos):
  total_count = 0
  pending_count = 0
  done_count = 0
  has_steps_count = 0
  for todo in todos:
    total_count += 1
    todo_status = todo['status']
    if todo_status == 'pending':
      pending_count += 1
    if todo_status == 'done':
      done_count += 1
    if len(todo['steps']) > 0:
      has_steps_count += 1
  return [total_count, pending_count, done_count, has_steps_count]


@app.get("/")
async def root():
  time_before = perf_counter()
  todos = todos_collection.find()
  [total_count, pending_count, done_count,
   has_steps_count] = getTodoCounts(todos)
  # count = todos_collection.count_documents({})
  # pending_count = todos_collection.count_documents({"status": "pending"})
  # done_count = todos_collection.count_documents({"status": "done"})
  # has_steps_count = todos_collection.count_documents(
  #     {"steps.0": {
  #         "$exists": True
  #     }})
  response_time = perf_counter() - time_before
  print(f"Total Time in response: {response_time}")
  return {
      "process_time": response_time,
      "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "name": "todo",
      "total": total_count,
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
