class Movie:

  def __init__(self, movie):
    self.douban_id = movie['douban_id']
    self.title = movie['title']
    self.year = movie.get('year', None)
    self.current_episode = movie.get('current_episode', None)
    self.episodes = movie['episodes']
    self.imdb_id = movie['imdb_id']
    self.genres = movie.get('genres', [])
    self.countries = movie.get('countries', [])
    self.languages = movie.get('languages', [])
    self.visual_type = movie['visual_type']

  def is_movie(self):
    return self.visual_type == 'movie'

  def get_year(self):
    return self.year

  def not_started(self):
    return self.current_episode == 0 or self.current_episode is None

  def in_progress(self):
    return self.current_episode is not None and self.episodes is not None and self.current_episode > 0 and self.current_episode < self.episodes

  def is_done(self):
    return self.current_episode == self.episodes

  def has_imdb(self):
    return self.imdb_id != ''

  def get_languages(self):
    return self.languages

  def get_genres(self):
    return self.genres

  def get_countris(self):
    return self.countries
