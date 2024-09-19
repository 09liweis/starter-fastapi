from datetime import datetime
import os
from time import perf_counter

from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo import ReturnDocument

from models.MovieStats import MovieStats
from models.TodoList import TodoList
from models.ExpenseList import ExpenseList

mongodb_url = os.environ['MONGODB_URL']

client = MongoClient(mongodb_url)
database = client.heroku_6njptcbp
stat_collection = database.stats

app = FastAPI()


class Todo(BaseModel):
  todo_id: str
  status: str


@app.get("/")
async def root():
  time_before = perf_counter()
  todos_collection = database.todos
  todo_list_collection = database.todolists
  todo_lists = todo_list_collection.find()

  todos = todos_collection.find()
  todoList = TodoList(todos)
  result = todoList.getTodoCounts()
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
  expenseList = ExpenseList(expenses)
  result = expenseList.getExpenseCounts()
  stat_collection.replace_one({"name": "expense"}, result, upsert=True)
  return result


@app.get("/places")
async def places_count():
  places_collection = database.places
  expenses_collecion = database.transactions
  places = list(places_collection.find())
  result = {"count": 0}
  for place in places:
    expenses_count = expenses_collecion.count_documents(
        {'place': place['_id']})
    if place["name"]:
      result[place["name"]] = expenses_count
    result["count"] += 1
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
