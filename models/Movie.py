class Movie:

  def __init__(self, movie):
    self.douban_id = movie['douban_id']
    self.title = movie['title']
    self.year = movie['year']
    self.current_episode = movie['current_episode']
    self.episodes = movie['episodes']
    self.type = movie['visual_type']
    self.imdb_id = movie['imdb_id']
    self.genres = movie['genres']
    self.countries = movie['countries']
    self.languages = movie['languages']
    self.visual_type = movie['visual_type']

  def isMovie(self):
    return self.visual_type == 'movie'

  def getYear(self):
    return self.year

  def isDone(self):
    return self.current_episode == self.episodes
