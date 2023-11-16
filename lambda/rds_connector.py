import psycopg2
import sys
import boto3
import os

# this file ensures connection to our postgresql server
# we can then add to RDS
ENDPOINT="news-db-instance.ctyrvpc3gemg.us-east-1.rds.amazonaws.com"
PORT="5432"
USER="postgres"
REGION="us-east-1"
DBNAME="news_db"

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

class RDS_connector:
	def __init__(self, input_str):
		self.sql_stmt = input_str
		self.error_mssg = ""
		try:
		    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=token, sslrootcert="SSLCERTIFICATE")
		    self.cur = conn.cursor()
		except:
			self.error_mssg = "Connection error to RDS"

	def add_tuples(self):
		if (len(self.error_mssg) == 0):
			#connection was successful!
			self.cur.execute(self.sql_stmt)
			return self.cur.fetchall()
		else:
			return self.error_mssg