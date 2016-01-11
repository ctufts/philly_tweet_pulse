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
import pandas as pd
from nltk.corpus import stopwords








################# import db config settings ##################
cnx = mysql.connector.connect(user=cs.user, password=cs.password,
                              host=cs.host,
                              database=cs.database,
                              charset = 'utf8mb4')
# cursor for writing out to table
curOut = cnx.cursor(buffered=True)

# read in data as pd dataframe
df = pd.read_sql('SELECT * from docMatrix;', con=cnx) 
df['frequency'] = df['frequency'].astype(int)

# import age and gender lexica
age = pd.read_csv('lexica/emnlp14age.csv')
gender = pd.read_csv('lexica/emnlp14gender.csv')

# get intercept values 
age_intercept = age[age.term == '_intercept'].loc[0,'weight']
gender_intercept = gender[gender.term == '_intercept'].loc[0,'weight']


for name, group in df.groupby('id'):
	# estimate age
	merged_df = pd.merge(age, group, how = 'inner', \
		left_on = 'term', right_on = 'word')
	if merged_df.empty:
		estimated_age = age_intercept
	else:
		estimated_age = sum(merged_df.weight*merged_df.frequency/\
			merged_df.tweet_length) + age_intercept
	
	#estimate gender
	merged_df = pd.merge(gender, group, how = 'inner', \
		left_on = 'term', right_on = 'word')
	if merged_df.empty:
		estimated_gender = gender_intercept
	else:
		estimated_gender = sum(merged_df.weight*merged_df.frequency/\
			merged_df.tweet_length) + gender_intercept

	# write data to table 
	data = [float(estimated_gender), float(estimated_age), name]
	stmt = "INSERT INTO demographics \
	(gender, age, id) VALUES (%s, %s, %s)"
	curOut.execute(stmt, data)
	
cnx.commit()
cnx.close()
	

