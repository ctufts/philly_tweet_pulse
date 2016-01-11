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

query = ("SELECT if(gender >= 0, 'F','M') as GenderStr,\
	date_format(created_at, '%m/%d/%Y %H') as ts, \
	count(*) as Count \
	FROM tweetTable as t1 \
	INNER JOIN (demographics as demo) \
	ON (t1.id = demo.id) \
	GROUP BY GenderStr, ts \
	ORDER BY STR_TO_DATE(ts, '%m/%d/%Y %H')")

	
print('start query')
# read from sql db
df = pd.read_sql(query, con=cnx) 
df.ts = df.ts + ":00"
cursor.close()
cnx.close()
print(df.head())

# convert dataframe to date time
df['ts']= pd.to_datetime(df['ts'],format = '%m/%d/%Y %H:%M')
df_spread = df.pivot(columns='GenderStr', index='ts')
# print to json
print(type(df_spread.index))
print(df_spread)

# remove pivot labels
df_spread.columns =[str(s2) for (s1,s2) in df_spread.columns.tolist()]

print(df_spread.to_csv())
# df_spread.to_json('yo.json', date_format='iso', date_unit='s')


