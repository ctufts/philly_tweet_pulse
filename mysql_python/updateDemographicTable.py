# Author: Chris Tufts
# Date: 12/29/2015
#
# The analysis in this script uses the lexica provided by 
# wwbp.org/data.html and developed as shown in:
# Sap, M., Park, G., Eichstaedt, J. E., Kern, M. L., Stillwell, D. J.,
# Kosinski, M., Ungar, L. H., & Schwartz, H. A. (2014).
# Developing Age and Gender Predictive Lexica over Social Media. In EMNLP

import csv
import mysql.connector
import configSettings as cs
import collections
import pickle
import pandas as pd
import os.path
import philly_tweet_tools
################# import db config settings ##################
cnx = mysql.connector.connect(user=cs.user, password=cs.password,
                              host=cs.host,
                              database=cs.database,
                              charset = 'utf8mb4')
# cursor for writing out to table
curOut = cnx.cursor(buffered=True)

# read in last 24 hours of data
df = pd.read_sql('SELECT * from docMatrix \
	WHERE created_at >= (select date_sub(MAX(created_at),\
	 INTERVAL 24 hour)FROM docMatrix) ;', con=cnx) 
df['frequency'] = df['frequency'].astype(int)


# import age and gender lexica
parent_directory = os.path.abspath(os.path.dirname(__file__))
age = pd.read_csv(parent_directory + '/lexica/emnlp14age.csv')
gender = pd.read_csv(parent_directory + '/lexica/emnlp14gender.csv')

# get intercept values 
age_intercept = age[age.term == '_intercept'].loc[0,'weight']
gender_intercept = gender[gender.term == '_intercept'].loc[0,'weight']

age.columns = ['age_term', 'age_weight']
gender.columns = ['gender_term', 'gender_weight']



merged_df = pd.merge(df,age,how = 'left', \
		left_on = 'word', right_on = 'age_term')
merged_df = pd.merge(merged_df,gender,how = 'left', \
		left_on = 'word', right_on = 'gender_term')


for name, group in merged_df.groupby('id'):
	# estimate age
	age_group = group.dropna(subset = ['age_weight'])
	if age_group.empty:
		estimated_age = age_intercept
	else:
		estimated_age = sum(age_group.age_weight*age_group.frequency/\
			age_group.tweet_length) + age_intercept

	gender_group = group.dropna(subset = ['gender_weight'])
	if gender_group.empty:
		estimated_gender = gender_intercept
	else:
		estimated_gender = sum(gender_group.gender_weight*gender_group.frequency/\
			gender_group.tweet_length) + gender_intercept
	
	# write data to table 
	data = [float(estimated_gender),float(estimated_age), name]
	stmt = "INSERT IGNORE INTO demographics \
	(gender, age, id) VALUES (%s, %s, %s)"
	curOut.execute(stmt, data)
	
cnx.commit()
cnx.close()
	

# get age and gender data and write to file for  web app
philly_tweet_tools.get_gender_data()
philly_tweet_tools.get_age_data()
