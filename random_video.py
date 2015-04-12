from gdata.youtube import service
import urlparse
import random

#-------------------------------------------------------------------------
def PrintVideo(entry):
  """
  Prints YouTube video details
  """

  #print 'Video title: %s' % entry.media.title.text
  #print 'Video watch page: %s' % entry.media.player.url
  url_data = urlparse.urlparse(entry.media.player.url)
  query = urlparse.parse_qs(url_data.query)
  video = query["v"][0]
  #print 'Video ID is %s' % video
  return video

#-------------------------------------------------------------------------  
def PrintVideoFeed(feed):
  """
  Returns a list of videos, select the first
  """

  for i, entry in enumerate(feed.entry):
    # Only select the first video
    if i > 0: break
    return PrintVideo(entry)

  # case when the word queries doesn't produce any videos:
  return False

#-------------------------------------------------------------------------  
def GenerateSearchWord():
  """
  Generate random search term for the YouTube query
  """

  f = open('/usr/share/dict/words')
  words = f.readlines()
  words_length = len(words)
  rand_int = random.randint(0, words_length)
  #print 'The randomly generated word is: {0}'.format(words[rand_int].strip('\n'))
  return words[rand_int].strip('\n')

#-------------------------------------------------------------------------  
def GenerateVideo():
  """
  Returns a random video list after taking a randomly-generated search term as input
  """

  yt_service = service.YouTubeService()
  query = service.YouTubeVideoQuery()
  query.vq = GenerateSearchWord()
  query.orderby = 'relevance'
  query.racy = 'include'
  feed = yt_service.YouTubeQuery(query)
  return PrintVideoFeed(feed)
#-------------------------------------------------------------------------  



def main():
  print GenerateVideo()

if __name__ == '__main__':
  main()


