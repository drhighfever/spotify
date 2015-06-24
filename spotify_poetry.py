## Script which takes a phrase as an input and returns Spotify songs.
## User will provide a phrase or a poem, and this script will go create a playlist based on the keywords present.
##
##
## I have made two attempts to solve this via two methods:
##
## 1) Iterate over consecutive words or tokens.
## 2) Use Natural Language Processing (NLP) library to extract parts of speech.
##
## For part 1 logic is described below:
## Main assumptions:
##  1) Song titles can't be more than 6 words.
##  2) Song titles are not shorter than  
## author: Abdul Syed (abdul.baqi.syed@gmail.com)

import re
from sets import Set
import operator
import spotipy
import collections

class SpotifyPoetry(object):
  """Class to store functions/objects which will input poetry from users and output spotify playlist."""

  def __init__(self):
    """Initialize internal set which will hold all tokens."""
    self._tokens = set()

  def _ReturnSpotifyService(self):
    """Returns spotify service."""
    return spotipy.Spotify()

  def _ProcessPhrase(self, phrase):
    """Removes any spaces or characters using RegExp and returns a list of words in the phrase."""
    return re.split(r"[\s\+*.,!\?]+", phrase)

  def _ReturnSongByTitle(self, phrase):
    """Returns results for songs."""
    return self._ReturnSpotifyService().search(q=phrase, type="track")
 
  def _TokenizePhrase(self, phrase, min_words_in_song=3, max_words_in_song=6):
    """Sets the internal set with tokenized phrases."""
    total_words = len(phrase)
    # Go backwards
    total_range = range(min(total_words, max_words_in_song), min_words_in_song - 1, -1)
    for num in total_range:
      token = " ".join(phrase[0:num])
      self._tokens.add(token)
      if token:
        result = self._TokenizePhrase(phrase[num:], min_words_in_song, max_words_in_song)

  #TODO: Need to add better exception handling. Right now, it's just continuing.
  def _GetSongs(self, tokens):
    """Function which calls spotify service and returns songs."""
    song_titles = {}
    for row in tokens:
      try:
        result = self._ReturnSongByTitle(row.lower().strip())
        if result:
          length = len(result['tracks']['items'])
          for num in xrange(length):
            artist = str(result['tracks']['items'][num]['artists'][0]['name']).lower().strip()
            title = str(result['tracks']['items'][num]['name']).lower()
            popularity = result['tracks']['items'][0]['popularity']
            if title == row.lower().strip():
              key = title + " by " + artist
              if popularity not in song_titles:
                song_titles[popularity] = [key]
              else:
                song_titles[popularity].append(key)
            else:
              print title +" by" + artist + " != " + row
      except:
        continue
    return song_titles


  def GetPlaylist(self, phrase):
    """Input a phrase and output a playlist based on keywords."""
    phrase = self._ProcessPhrase("If I can't let it go out of my mind")
    self._TokenizePhrase(phrase)
    playlist = self._GetSongs(self._tokens)
    sorted_playlist_by_popularity = sorted(playlist.items())
    sorted_set = set()
    for row in list(reversed(sorted_playlist_by_popularity)):
      for entry in row[1]:
        sorted_set.add(entry)
    for row in sorted_set:
      print row

if __name__ == "__main__":
  phrase = input("Enter favorite poetry with quotes: ")
  phrase = str(phrase).lower()
  t = SpotifyPoetry()
  t.GetPlaylist(phrase)

