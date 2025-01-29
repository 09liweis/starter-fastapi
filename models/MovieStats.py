from models.Movie import Movie


class MovieStats:

  def __init__(self, movies):
    self.movies = [Movie(movie) for movie in movies]

  def count_movie_field(self, field_datas, field, count_dict):
    if len(field_datas) > 0:
      for v in field_datas:
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
    years_count = {}
    for movie in self.movies:
      self.count_movie_field(movie.get_genres(), "genres", genres_count)

      self.count_movie_field(movie.get_countris(), "countries",
                             countries_count)

      self.count_movie_field(movie.get_languages(), "languages",
                             languages_count)

      if year := movie.get_year():
        if year in years_count:
          years_count[year] += 1
        else:
          years_count[year] = 1

      if movie.is_movie():
        movie_count += 1
      else:
        tv_count += 1

      if movie.is_done():
        done_count += 1
      if movie.not_started():
        not_started_count += 1

      if movie.has_imdb():
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
            "languages": languages_count,
            "years": years_count
        }
    }
