#!/bin/sh
echo "update Topic table"
/home/chris/anaconda3/envs/flaskpy3/bin/python /var/www/FlaskApp/mysql_python/updateTopicTable.py;
echo "update Demo table"
/home/chris/anaconda3/envs/flaskpy3/bin/python /var/www/FlaskApp/mysql_python/updateDemographicTable.py;
echo "update ldavis"
/home/chris/anaconda3/envs/flaskpy3/bin/python /var/www/FlaskApp/mysql_python/generateTopics.py
echo "processes complete"
