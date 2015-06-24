## Script which takes a phrase as an input and returns Spotify songs.
## User will provide a phrase or a poem, and this script will go create a playlist based on the keywords present.
##
##
## I have made two attempts to solve this via two methods:
##
## 1) Iterate over consecutive words or tokens.
## DIDNT HAVE TIME TO IMPLEMENT NLP BELOW.
## 2) Use Natural Language Processing (NLP) library to extract parts of speech.
##
## For part 1 logic is described below:
## Main assumptions:
##  1) Song titles can't be more than 6 words.
##  2) Song titles are not shorter than 3 words.
##  3) Strip out of all punctuation.
##  4) song title must be a 100% match to the phrase.
##
##TODO:
##  1) Add memoization to avoid same queries being sent to spotipy.
##  2) Add parallelization, so multiple queries can be sent to spotipy, to speed up.
##  3) Add ability to do % match. Currently song title has to match exactly the phrase.
##     Add ability to calculate percent of words matching, to show greater results.
##  4) Track phrases with no results. 
##
## author: Abdul Syed (abdul.baqi.syed@gmail.com)

import re
from sets import Set
import operator
import spotipy
import collections

class SpotifyPoetry(object):
  """Class to store functions/objects which will input poetry from users and output spotify playlist."""

  def __init__(self):
    """Initialize internal set which will hold all tokens.

    _tokens: set which will contain unique tokens(str) from a given phrase.
    """
    self._tokens = set()

  def _ReturnSpotifyService(self):
    """Returns spotify service."""
    return spotipy.Spotify()

  def _ProcessPhrase(self, phrase):
    """Helper function to removes any spaces or characters using RegExp.

    Args:
      phrase: str, a user inputted phrase to search.

    Returns:
      list of words in the phrase, removing any special characters.
    """
    return re.split(r"[\s\+*.,!\?]+", phrase.lower().replace("'",""))

  def _ReturnSongByTitle(self, phrase):
    """Returns results for songs.

    Args:
      phrase: str, a user inputted phrase to search.

    Returns:
      Response from Spotify service based on search token and type track.
    """
    return self._ReturnSpotifyService().search(q=phrase, type="track")
 
  def _TokenizePhrase(self, phrase, min_words_in_song=3, max_words_in_song=6):
    """Sets the internal set with tokenized phrases.

    Args:
      phrase: str, a user inputted search phrase.
      min_words_in_song: int, minimum words in a song title. Default to 3.
      max_words_in_song: int, maximum words in a song title. Default to 6
    """
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
    """Function which calls spotify service and returns songs. Songs are ordered by popularity field in results.
    Args:
      tokens: list of words.

    Returns:
      song_titles: list, containing unique songs and artists. 
    """
    song_titles = set()
    for row in tokens:
      try:
        search_token = row.lower().strip()
        result = self._ReturnSongByTitle(search_token)
        if result:
          len_of_results = len(result['tracks']['items'])
          for num in xrange(len_of_results):
            artist = str(result['tracks']['items'][num]['artists'][0]['name']).lower().strip()
            title = self._ProcessPhrase(str(result['tracks']['items'][num]['name']).lower())
            title = " ".join(title)
            #TODO (implement popularity rank)
            #popularity = result['tracks']['items'][0]['popularity']
            key = title + " by " + artist
            if search_token == title:
              song_titles.add(key)
      except:
        continue
    print "PLAYLIST FOR YOU <3<3<3"
    for entry in song_titles:
      print entry

  def GetPlaylist(self, phrase):
    """Input a phrase and output a playlist based on keywords."""
    phrase = self._ProcessPhrase(phrase)
    self._TokenizePhrase(phrase)
    playlist = self._GetSongs(self._tokens)

if __name__ == "__main__":
  phrase = input("Enter favorite poetry with quotes: ")
  t = SpotifyPoetry()
  t.GetPlaylist(phrase)
