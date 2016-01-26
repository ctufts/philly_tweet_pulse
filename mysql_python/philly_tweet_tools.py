#from mysql_python import configSettings as cs
import configSettings as cs
import mysql.connector
import json
import collections
import pandas as pd
import os.path


def get_data():
	cnx = mysql.connector.connect(user=cs.user, password=cs.password,
                              host=cs.host,
                              database=cs.database,
                              charset = 'utf8mb4')


	cursor=cnx.cursor()

	query = ("select date_format(created_at, '%H') as ts, \
		count(1) as timecount from Philly.tweetTable group by ts \
		order by minute(ts) desc    ")

	cursor.execute(query)

	query_list = []
	for (ts, timecount) in cursor:
		d = collections.OrderedDict()
		d['ts'] = ts
		d['timecount'] = str(timecount)
		query_list.append(d)

	j = json.dumps(query_list)
	

	cursor.close()
	cnx.close()
	return j

def get_gender_data():
	cnx = mysql.connector.connect(user=cs.user, password=cs.password,
                              host=cs.host,
                              database=cs.database,
                              charset = 'utf8mb4')


	cursor=cnx.cursor()
	query = ("SELECT if(gender >= 0, 'F','M') as GenderStr,\
		date_format(created_at, '%m/%d/%Y %H') as ts,\
		count(*) as Count \
		FROM \
        (SELECT * from tweetTable WHERE \
      	created_at >( select date_sub(max(created_at), interval 24 hour) \
      	from tweetTable) ) AS A JOIN ( SELECT * from demographics) as B \
	    ON( A.id = B.id) \
	    GROUP BY GenderStr, ts")

	# ORDER BY STR_TO_DATE(ts, '%m/%d/%Y %H')")
	# read from sql db
	df = pd.read_sql(query, con=cnx) 
	df.ts = df.ts + ":00"
	cursor.close()
	cnx.close()

	# convert dataframe to date time
	df['ts']= pd.to_datetime(df['ts'],format = '%m/%d/%Y %H:%M')
	df_spread = df.pivot(columns='GenderStr', index='ts')
	# remove extra pivot table labels
	df_spread.columns =[str(s2) for (s1,s2) in df_spread.columns.tolist()]
	# print to json
	parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	df_spread.to_csv(parent_directory + '/FlaskApp/static/gender_data.csv')
	return()
	# return(df_spread.to_csv())

def get_age_data():
	cnx = mysql.connector.connect(user=cs.user, password=cs.password,
                              host=cs.host,
                              database=cs.database,
                              charset = 'utf8mb4')


	cursor=cnx.cursor()

	query = ("SELECT date_format(created_at, '%m/%d/%Y %H') as ts,\
      	   case when age <= 17 then '0 - 17' \
           when age > 17 and age <= 24  then '18-24' \
           when age > 24 and age <= 34  then '25-34' \
           when age > 34 and age <= 44  then '35-44' \
           when age > 44 and age <= 54  then '45-54' \
           when age > 54 and age <= 64  then '55-64' \
           else '65+' \
      end ageRange,\
      count(*) as Count \
	  FROM \
	  (SELECT * from tweetTable WHERE \
	  created_at >( select date_sub(max(created_at), interval 24 hour) \
            from tweetTable) ) AS A \
	  JOIN \
	  ( SELECT * from demographics) as B \
	  ON( A.id = B.id) \
	  GROUP BY ageRange, ts \
	  ORDER BY STR_TO_DATE(ts, '%m/%d/%Y %H')")

	# read from sql db
	df = pd.read_sql(query, con=cnx) 
	df.ts = df.ts + ":00"
	cursor.close()
	cnx.close()

	# convert dataframe to date time
	df['ts']= pd.to_datetime(df['ts'],format = '%m/%d/%Y %H:%M')
	df_spread = df.pivot(columns='ageRange', index='ts')
	# remove extra pivot table labels
	df_spread.columns =[str(s2) for (s1,s2) in df_spread.columns.tolist()]
	# print to csv 
	parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	df_spread.to_csv(parent_directory + '/FlaskApp/static/age_data.csv')
	return()
	# return(df_spread.to_csv())



