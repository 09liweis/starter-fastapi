class MovieStats:

  def __init__(self, movies):
    self.movies = movies

  def count_movie_field(self, movie, field, count_dict):
    if field in movie:
      values = movie[field]
      for v in values:
        if v in count_dict:
          count_dict[v] += 1
        else:
          count_dict[v] = 1

  def get_stats(self):
    total = 0
    movie_count = 0
    tv_count = 0
    done_count = 0
    not_started_count = 0
    has_imdb_count = 0
    genres_count = {}
    countries_count = {}
    languages_count = {}
    for movie in self.movies:
      self.count_movie_field(movie, "genres", genres_count)

      self.count_movie_field(movie, "countries", countries_count)

      self.count_movie_field(movie, "languages", languages_count)

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
        "name": "movie",
        "details": {
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
    }
