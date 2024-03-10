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
  stat_collection.replace_one({"name": "todo"}, result, upsert=True)
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
  result_details = {}
  for expense in expenses:
    date = expense["date"]
    price = expense["price"]
    category = expense["category"]
    yearMonthDate = date[:7]
    yearDate = date[:4]

    if yearDate not in result_details:
      result_details[yearDate] = {"total": price}
    else:
      result_details[yearDate]["total"] += price

    if category in result_details[yearDate]:
      result_details[yearDate][category] += price
    else:
      result_details[yearDate][category] = price

    if yearMonthDate not in result_details:
      result_details[yearMonthDate] = {"total": price}
    else:
      result_details[yearMonthDate]["total"] += price

    if category in result_details[yearMonthDate]:
      result_details[yearMonthDate][category] += price
    else:
      result_details[yearMonthDate][category] = price
  result = {"name": "expense", "details": result_details}
  stat_collection.replace_one({"name": "expense"}, result, upsert=True)
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
