import os
from datetime import datetime
from time import perf_counter

from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

mongodb_url = os.environ['MONGODB_URL']

client = MongoClient(mongodb_url)
todos_collection = client.heroku_6njptcbp.todos
movies_collection = client.heroku_6njptcbp.visuals

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


@app.get("/movies")
async def movies_count():
  movies = movies_collection.find()
  total = 0
  movie_count = 0
  tv_count = 0
  done_count = 0
  not_started_count = 0
  has_imdb_count = 0
  genres_count = {}
  countries_count = {}
  languages_count = {}
  for movie in movies:
    if 'genres' in movie:
      genres = movie['genres']
      for g in genres:
        if g in genres_count:
          genres_count[g] += 1
        else:
          genres_count[g] = 1

    if 'countries' in movie:
      countries = movie['countries']
      for c in countries:
        if c in countries_count:
          countries_count[c] += 1
        else:
          countries_count[c] = 1

    if 'languages' in movie:
      languages = movie['languages']
      for l in languages:
        if l in languages_count:
          languages_count[l] += 1
        else:
          languages_count[l] = 1

    if movie['visual_type'] == 'movie':
      movie_count += 1
    else:
      tv_count += 1

    if 'current_episode' in movie:
      if movie['current_episode'] == movie['episodes']:
        done_count += 1
      if movie['current_episode'] == 0:
        not_started_count += 1
    else:
      not_started_count += 1

    if 'imdb_id' in movie and movie['imdb_id'] != '':
      has_imdb_count += 1

    total += 1
  return {
      "total": total,
      "movie": movie_count,
      "tv": tv_count,
      "done": done_count,
      "not_started": not_started_count,
      "has_imdb": has_imdb_count,
      "genres": genres_count,
      "countries": countries_count,
      "languages": languages_count
  }


@app.get("/item/{item_id}")
async def read_item(item_id: int):
  return {"item_id": item_id}


@app.get("/items/")
async def list_items():
  return [{"item_id": 1, "name": "Foo"}, {"item_id": 2, "name": "Bar"}]


@app.post("/todos/")
async def create_todo(todo: Todo):
  return todo
