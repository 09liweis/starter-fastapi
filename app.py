import os
from datetime import datetime
from time import perf_counter

from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

from movie_stats import MovieStats

mongodb_url = os.environ['MONGODB_URL']

client = MongoClient(mongodb_url)

app = FastAPI()


class Todo(BaseModel):
  todo_id: str
  status: str


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
  return {
      "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "name": "todo",
      "total": total_count,
      "pending": pending_count,
      "done": done_count,
      "has_steps_count": has_steps_count
  }


@app.get("/")
async def root():
  time_before = perf_counter()
  todos_collection = client.heroku_6njptcbp.todos
  todos = todos_collection.find()
  result = getTodoCounts(todos)
  response_time = perf_counter() - time_before
  print(f"Total Time in response: {response_time}")
  result['response_time'] = response_time
  return result
  # count = todos_collection.count_documents({})
  # pending_count = todos_collection.count_documents({"status": "pending"})
  # done_count = todos_collection.count_documents({"status": "done"})
  # has_steps_count = todos_collection.count_documents(
  #     {"steps.0": {
  #         "$exists": True
  #     }})


@app.get("/movies")
async def movies_count():
  movies_collection = client.heroku_6njptcbp.visuals
  movies = list(movies_collection.find())
  movie_stats = MovieStats(movies)
  result = movie_stats.get_stats()
  return result


@app.get("/item/{item_id}")
async def read_item(item_id: int):
  return {"item_id": item_id}


@app.get("/items/")
async def list_items():
  return [{"item_id": 1, "name": "Foo"}, {"item_id": 2, "name": "Bar"}]


@app.post("/todos/")
async def create_todo(todo: Todo):
  return todo
