# code for streaming twitter to a mysql db
# for Python 3 and will support emoji characters (utf8mb4)
# based on the Python 2 code 
# supplied by http://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
# for further information on how to use python 3, twitter's api, and 
# mysql together visit: http://miningthedetails.com/blog/python/TwitterStreamsPythonMySQL/


from tweepy import Stream
from tweepy import OAuthHandler
import configSettings as cs
from tweepy.streaming import StreamListener
import mysql.connector
from mysql.connector import errorcode
import time
import json



# set up connection to db
# make sure to set charset to 'utf8mb4' to support emoji
cnx = mysql.connector.connect(user=cs.user, password=cs.password,
                              host=cs.host,
                              database=cs.database,
                              charset = 'utf8mb4')


cursor=cnx.cursor()


#consumer key, consumer secret, access token, access secret.
ckey=cs.ckey
csecret=cs.csecret
atoken=cs.atoken
asecret=cs.asecret

# set up stream listener
class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
		# collect all desired data fields 
        if 'text' in all_data:
          tweet         = all_data["text"]
          tweet_id      = all_data["id_str"]
          created_at    = time.strftime('%Y-%m-%d %H:%M:%S', 
            time.strptime(all_data['created_at'],
              '%a %b %d %H:%M:%S +0000 %Y'))
          retweeted     = False
          quoted        = False
          rt_id         = None
          quoted_id     = None
          username      = all_data["user"]["screen_name"]
          user_tz       = all_data["user"]["time_zone"]
          user_location = all_data["user"]["location"]
          user_coordinates   = all_data["coordinates"]
          
		      
		  # if coordinates are not present store blank value
		  # otherwise get the coordinates.coordinates value
          if user_coordinates is None:
            final_coordinates = user_coordinates
          else:
            final_coordinates = str(all_data["coordinates"]["coordinates"])
      
      # check if the tweet is a quoted or retweeted status
          if 'retweeted_status' in all_data:
            retweeted = True
            rt_id     = all_data["retweeted_status"]["id_str"]
          
          if 'quoted_status' in all_data:
            quoted = True
            quoted_id = all_data["quoted_status"]["id_str"] 
          
          # protect against opt-in links which exceed well over 140 
          # characters
          if len(tweet) > 250:
            tweet = tweet[0:250]


    		  # inser values into the db
          cursor.execute("INSERT INTO tweetTable (id, created_at, username,tweet, \
            coordinates, userTimeZone, retweeted) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (tweet_id, created_at, username, tweet, final_coordinates, user_tz, retweeted))
          cnx.commit()
          
          print((username,retweeted, quoted, quoted_id, rt_id))
          
          return True
        else:
          return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# create stream and filter on a searchterm
twitterStream = Stream(auth, listener())
twitterStream.filter(track=['philly, philadelphia'],
  languages = ["en"], stall_warnings = True)