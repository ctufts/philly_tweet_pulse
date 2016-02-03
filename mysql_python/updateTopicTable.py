# Author: Chris Tufts
# Date: 12/29/2015
#
# The analysis in this script uses the lexica provided by 
# wwbp.org/data.html and developed as shown in:
# Sap, M., Park, G., Eichstaedt, J. E., Kern, M. L., Stillwell, D. J.,
# Kosinski, M., Ungar, L. H., & Schwartz, H. A. (2014).
# Developing Age and Gender Predictive Lexica over Social Media. In EMNLP

import csv
import re
import happierfuntokenizing
import mysql.connector
import configSettings as cs
import collections
import pickle
import gensim
from nltk.tokenize import WhitespaceTokenizer
from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords
import os.path
import json
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
query = ("SELECT id, created_at, tweet FROM tweetTable WHERE retweeted = 0 \
	AND created_at >= (select date_sub(MAX(created_at), \
	 INTERVAL 24 hour)FROM tweetTable)")

curIn.execute(query)

############# place tweets in a list #################

# initialize lemmatizer()
lem = WordNetLemmatizer()
# initialize stopwords
stopwords = stopwords.words('english')
parent_directory = os.path.abspath(os.path.dirname(__file__))
bannedWords = json.loads(open(parent_directory + '/lexica/badWords.json').read())
stopwords = stopwords + bannedWords + ['philly','philadelphia','...']
#for sword in additional_stopwords:
#    stopwords.append(sword)
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
		stmt = "INSERT IGNORE INTO docMatrix \
		(word, frequency, tweet_length, \
			created_at, id) VALUES (%s, %s, %s, %s, %s)"
		curOut.execute(stmt, data)
	# get set of filtered tweets for 
	#tokenized_tweets.append([s for s in sentence 
	#	if s not in stopwords and len(s) > 2 ])
	sentence_topic_model = WhitespaceTokenizer().tokenize(tweet.lower())
	temp = []
	for w in sentence_topic_model:
		if w not in stopwords and \
			len(w) > 2 and \
    			not (re.match('@\\w',w)) and \
    			not (re.match('#\\w',w)) and \
    			not (re.match('htt\\w',w)) and \
    			not (re.match('[^A-Za-z0-9]+', w)):
    				temp += [words for words in word_tokenize(w) if \
    					len(words) > 2 and  words not in stopwords and
    					not (re.match('[^A-Za-z0-9]+', words))]
	
	if temp:
 		tokenized_tweets.append(temp)

cnx.commit()
cnx.close()

# create dictionary and corpus then write to pickle
dictionary = gensim.corpora.Dictionary(tokenized_tweets)
corpus = [dictionary.doc2bow(text) for text in tokenized_tweets]

########## write out corpus ###############
parent_directory = os.path.abspath(os.path.dirname(__file__))

file_Name = parent_directory + "/data/corpus"
# open the file for writing
fileObject = open(file_Name,'wb') 

pickle.dump(corpus,fileObject)
fileObject.close()

### write out dictionary #################
file_Name = parent_directory + "/data/dictionary"
# open the file for writing
fileObject = open(file_Name,'wb') 

pickle.dump(dictionary,fileObject)
fileObject.close()


