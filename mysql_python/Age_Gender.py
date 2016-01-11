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


################# read in tweets from main table ##################
cnx = mysql.connector.connect(user=cs.user, password=cs.password,
                              host=cs.host,
                              database=cs.database,
                              charset = 'utf8mb4')


cursor=cnx.cursor()

query = ("SELECT tweet FROM tweetTable LIMIT 5")

cursor.execute(query)

############# place tweets in a list #################
tweets = []

tweets = [x[0] for x in cursor.fetchall()]
# print(tweets[0])
cursor.close()
cnx.close()



###################### read in age lexicon ######################
terms = []
weights = []
age_lex_dict = {}
with open('lexica/emnlp14age.csv', newline='') as csvfile:
     lexreader = csv.DictReader(csvfile)
     for row in lexreader:
     	terms.append(row['term'])
     	weights.append(row['weight'])
     	age_lex_dict[row['term']] = float(row['weight'])


#################### read in gender lexicon ######################
terms = []
weights = []
gender_lex_dict = {}
with open('lexica/emnlp14gender.csv', newline='') as csvfile:
     lexreader = csv.DictReader(csvfile)
     for row in lexreader:
     	terms.append(row['term'])
     	weights.append(row['weight'])
     	gender_lex_dict[row['term']] = float(row['weight'])

          


tok = happierfuntokenizing.Tokenizer()
for t in tweets:
	# tokenize and get word frequency
	sentence =  list(tok.tokenize(t.lower()))
	words = collections.Counter(sentence)
	
	# initialize estimate values to zero
	age_estimate = 0
	gender_estimate = 0

	#  calculate age score
	for key, value in age_lex_dict.items():
		if(words[key] > 0):
			age_estimate += value*words[key]/len(sentence)
	# calculate gender score
	for key, value in gender_lex_dict.items():
		if(words[key] > 0):
			gender_estimate+= value*words[key]/len(sentence)

	if age_estimate != 0:
		age_estimate += age_lex_dict['_intercept']
	if gender_estimate != 0:
		gender_estimate += gender_lex_dict['_intercept']
	print("age:" , age_estimate ,"  gender: ", gender_estimate)
print(sentence)
			

