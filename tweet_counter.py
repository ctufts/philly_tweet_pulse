import mysql.connector
import json
import collections
import configSettings as cs


def get_data():
	cnx = mysql.connector.connect(user=cs.user, password=cs.password,
                              host=cs.host,
                              database=cs.database,
                              charset = 'utf8mb4')


	cursor=cnx.cursor()

	query = ("select date_format(created_at, '%H:%i') as ts, \
		count(1) as timecount from tweetTable group by ts \
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