import json 
import boto3
import sys
import psycopg2
import csv
import logging
import io
import os

 # RDS database configuration values
endpoint = os.environ['endpoint']
db_user = os.environ['user']
db_password = os.environ['password']
db_name = os.environ['db_name']

# S3 bucket configuration
s3_bucket = "news-visualize-bucket"
s3_key = "input/input.csv"
s3 = boto3.resource('s3')

# Connect to RDS database outside of the handler to allow connections
# to be reused by subsequent function invocations
try:
    connection = psycopg2.connect(host=endpoint,dbname=db_name,user=db_user,password=db_password)
except psycopg2.Error as e:
    logging.error("ERROR: Unexpected error: Could not connect to Postgres instance")
    logging.error(e)
    sys.exit()

def lambda_handler(event, context):
    # Fetch data from the database
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM articles;")
    rows = cursor.fetchall()

    # for row in rows:
    #     print("{0} {1} {2}".format(row[0],row[1],row[2]))

    # Write data to CSV in-memory buffer
    csv_buffer = io.StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerows(rows)
    
    try:
        print("I WAS HERE")
        s3.Bucket(s3_bucket).put_object(Key=s3_key, Body=csv_buffer.getvalue())
        
        # Close database connection
        cursor.close()
        connection.close()
        
        return {
        'statusCode': 200,
        'body': 'Data uploaded successfully to S3.'
        }
    except Exception as e:
        print("Error from put_object:", e)
        
         # Close database connection
        cursor.close()
        connection.close()
        
        return {
        'statusCode': 500,
        'body': 'Error uploading CSV file to S3.'
        }