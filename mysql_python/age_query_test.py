# import mysql.connector
# import json
# import collections
# from mysql_python import configSettings as cs

import mysql.connector
import json
import collections
import configSettings as cs
import pandas as pd



cnx = mysql.connector.connect(user=cs.user, password=cs.password,
                          host=cs.host,
                          database=cs.database,
                          charset = 'utf8mb4')


cursor=cnx.cursor()

query = ("SELECT date_format(created_at, '%m/%d/%Y %H') as ts,\
  		case when age <= 17    then '0 - 17'\
       		when age > 17 and age <= 24  then '18-24'\
       		when age > 24 and age <= 34  then '25-34'\
       		when age > 34 and age <= 44  then '35-44'\
       		when age > 44 and age <= 54  then '45-54'\
       		when age > 54 and age <= 64  then '55-64'\
       		else '65+'\
  	    end ageRange,\
  		count(*) as Count\
		FROM tweetTable as t1 \
		INNER JOIN (demographics as demo)\
		ON (t1.id = demo.id)\
		GROUP BY ageRange, ts")

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
# print to json
print(df_spread.to_csv())



