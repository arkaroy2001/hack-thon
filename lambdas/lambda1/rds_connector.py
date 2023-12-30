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
PASSWORD = "" # put in password (already in place within code uploaded in lambda function)

#gets the credentials from .aws/credentials
session = boto3.Session()

client = session.client('rds')

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

class RDS_connector:
	def __init__(self, input_str):
		self.sql_stmt = input_str
		self.error_mssg = ""
		try:
			self.conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=PASSWORD, sslrootcert="SSLCERTIFICATE")
			self.cur = self.conn.cursor()
		except Exception as e:
			self.error_mssg += "Connection error to RDS due to {}".format(e)

	def add_tuples(self):
		if (len(self.error_mssg) == 0):
			#connection was successful!
			self.cur.execute(self.sql_stmt)
			self.conn.commit()
			self.cur.close()
			self.conn.close()
			return self.error_mssg
		else:
			if self.cur is not None:
				self.cur.close()
			if self.conn is not None:
				self.conn.close()
			return self.error_mssg