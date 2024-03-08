import os
from datetime import datetime
from time import perf_counter

from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo import ReturnDocument

from movie_stats import MovieStats

mongodb_url = os.environ['MONGODB_URL']

client = MongoClient(mongodb_url)
database = client.heroku_6njptcbp
stat_collection = database.stats

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
      "name": "todo",
      "details": {
          "total": total_count,
          "pending": pending_count,
          "done": done_count,
          "has_steps_count": has_steps_count
      }
  }


@app.get("/")
async def root():
  time_before = perf_counter()
  todos_collection = database.todos
  todos = todos_collection.find()
  result = getTodoCounts(todos)
  response_time = perf_counter() - time_before
  print(f"Total Time in response: {response_time}")
  stat_collection.replace_one({"name": "todo"},
                                           result,
                                           upsert=True)
  result['response_time'] = response_time
  result["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
  movies_collection = database.visuals
  movies = list(movies_collection.find())
  movie_stats = MovieStats(movies)
  movie_result = movie_stats.get_stats()
  stat_collection.replace_one({"name": "movie"}, movie_result, upsert=True)
  return movie_result


@app.get("/expenses")
async def expenses_count():
  expenses_collection = database.transactions
  expenses = list(expenses_collection.find())
  result = {}
  for expense in expenses:
    date = expense["date"]
    price = expense["price"]
    category = expense["category"]
    yearMonthDate = date[:7]
    yearDate = date[:4]

    if yearDate not in result:
      result[yearDate] = {"total": price}
    else:
      result[yearDate]["total"] += price

    if category in result[yearDate]:
      result[yearDate][category] += price
    else:
      result[yearDate][category] = price

    if yearMonthDate not in result:
      result[yearMonthDate] = {"total": price}
    else:
      result[yearMonthDate]["total"] += price

    if category in result[yearMonthDate]:
      result[yearMonthDate][category] += price
    else:
      result[yearMonthDate][category] = price
  return result


@app.get("/places")
async def places_count():
  places_collection = database.places
  expenses_collecion = database.transactions
  places = list(places_collection.find())
  result = {}
  count = 0
  for place in places:
    expenses_count = expenses_collecion.count_documents(
        {'place': place['_id']})
    if place["name"]:
      result[place["name"]] = expenses_count
    count += 1
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
