## Script which takes a phrase as an input and returns Spotify.
## User will provide a phrase or a poem, and this script will effectively and go create a playlist.
## Logic is described below:
##   Assumptions: Maximum of 20 songs will be returned.
##   
## author: Abdul Syed (abdul.baqi.syed@gmail.com)

import re
from sets import Set
import spotipy

class SpotifyPoetry(object):
  """Inputs phrases and outputs associated songs related to a phrase."""

  def __init__(self):
    self._tokens = set()

  def _ReturnSpotifyService(self):
    """Returns spotify service."""
    return spotipy.Spotify()

  def _ProcessPhrase(self, phrase):
    """Removes any spaces or characters using RegExp and sets a list."""
    return re.split(r"[\s\+*.,!\?]+", phrase)

  def _ReturnSongByTitle(self, phrase):
    """Returns results for songs."""
    return self._ReturnSpotifyService().search(q=phrase, type="track")
 
  def _TokenizePhrase(self, phrase, min_song_size=3, max_song_size=6):
    """Returns a list with all tokens to search for"""
    total_words = len(phrase)
    # Go backwards
    total_range = range(min(total_words, max_song_size), min_song_size - 1, -1)
    for num in total_range:
      token = " ".join(phrase[0:num])
      self._tokens.add(token)
      if token:
        result = self._TokenizePhrase(phrase[num:], min_song_size, max_song_size)
  def _GetSongs(self, tokens):
    for row in tokens:
      try:
        artist = self._ReturnSongByTitle(row)['tracks']['items'][0]['artists']['name']
        title = self._ReturnSongByTitle(row)['tracks']['items'][0]['name']
        print artist, title
        song_titles.add([artist, title])
      except:
        continue


  def testFunction(self):
    phrase = self._ProcessPhrase("If I can't let it go out of my mind")
    self._TokenizePhrase(phrase)
    self._GetSongs(self._tokens)

t = SpotifyPoetry()
t.testFunction()




name = 'Drake'
results = spotify.search(q='artist:' + name, type='artist')
print results
