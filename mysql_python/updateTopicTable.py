# Author: Chris Tufts
# Date: 12/29/2015
#
# The analysis in this script uses the lexica provided by 
# wwbp.org/data.html and developed as shown in:
# Sap, M., Park, G., Eichstaedt, J. E., Kern, M. L., Stillwell, D. J.,
# Kosinski, M., Ungar, L. H., & Schwartz, H. A. (2014).
# Developing Age and Gender Predictive Lexica over Social Media. In EMNLP

import csv
import happierfuntokenizing
import mysql.connector
import configSettings as cs
import collections
import pickle
import gensim
from nltk.corpus import stopwords


################# read in tweets from main table ##################
cnx = mysql.connector.connect(user=cs.user, password=cs.password,
                              host=cs.host,
                              database=cs.database,
                              charset = 'utf8mb4')


# cursor=cnx.cursor()
curIn = cnx.cursor(buffered=True)
curOut = cnx.cursor(buffered=True)

# change query to get tweet id and tweets and date time
# ignore retweets
query = ("SELECT id, created_at, tweet FROM tweetTable WHERE retweeted = 0")

curIn.execute(query)

############# place tweets in a list #################


# initialize stopwords
stopwords = stopwords.words('english')
# create dataset to write to sql table #########
tok = happierfuntokenizing.Tokenizer()
tokenized_tweets = []
for id, created_at, tweet in curIn:
	# tokenize and get word frequency
	sentence =  list(tok.tokenize(tweet.lower()))
	tweet_length = len(sentence)
	words = collections.Counter(sentence)
	# write data to word frequency table
	for key, value in words.items():
		data = [key,value, tweet_length, created_at, id]
		print(data)
		stmt = "INSERT INTO docMatrix \
		(word, frequency, tweet_length, \
			created_at, id) VALUES (%s, %s, %s, %s, %s)"
		curOut.execute(stmt, data)
	# get set of filtered tweets for 
	tokenized_tweets.append([s for s in sentence 
		if s not in stopwords and len(s) > 2 ])	


# print(tweets[0])
cnx.commit()
cnx.close()

# create dictionary and corpus then write to pickle
dictionary = gensim.corpora.Dictionary(tokenized_tweets)
corpus = [dictionary.doc2bow(text) for text in tokenized_tweets]

########## write out corpus ###############
file_Name = "data/corpus"
# open the file for writing
fileObject = open(file_Name,'wb') 

pickle.dump(corpus,fileObject)
fileObject.close()

### write out dictionary #################
file_Name = "data/dictionary"
# open the file for writing
fileObject = open(file_Name,'wb') 

pickle.dump(dictionary,fileObject)
fileObject.close()


