import boto3
import sys
import psycopg2 
import numpy as np 
import psycopg2.extras as extras 
import pandas as pd
import os

 # RDS database configuration values
endpoint = "news-db-instance.ctyrvpc3gemg.us-east-1.rds.amazonaws.com"
db_user = "postgres"
db_password = "arkasoham"
db_name = "news_db"

# S3 bucket configuration
s3_bucket = "news-visualize-bucket"
s3_key = "output/output.csv"
s3 = boto3.client('s3')

# Connect to RDS database outside of the handler to allow connections
# to be reused by subsequent function invocations
try:
    connection = psycopg2.connect(host=endpoint, port="5432", database=db_name, user=db_user, password='arkasoham', sslrootcert="SSLCERTIFICATE")
    connection.set_session(autocommit=True)
except psycopg2.Error as e:
    print("ERROR: Unexpected error: Could not connect to Postgres instance")
    sys.exit()

def lambda_handler(event, context):
    s3.download_file(s3_bucket, s3_key, '/tmp/target.csv')
    
    df = pd.read_csv('/tmp/target.csv')
    df = df.dropna() #get rid of any rows which contain NaN
    execute_values(connection, df, 'processed_articles') 
    
    return {
        'statusCode': 200,
        'body': 'Data uploaded successfully to RDS!'
    }
    
def execute_values(conn, df, table): 
  
    tuples = [tuple(x) for x in df.to_numpy()] 
  
    cols = ','.join(list(df.columns)) 
    # SQL query to execute 
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols) 
    cursor = conn.cursor() 
    try: 
        extras.execute_values(cursor, query, tuples) 
        #conn.commit() 
    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error: %s" % error) 
        conn.rollback() 
        cursor.close() 
        return 1
    print("the dataframe is inserted") 
    cursor.close()