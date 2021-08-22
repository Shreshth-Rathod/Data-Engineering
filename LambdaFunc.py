import json
import csv
import boto3
import mysql.connector

s3client=boto3.client('s3')

Hostname = *****
DBName = *****
UserID = *****
PortNumber = *****
Password = *****

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file = event['Records'][0]['s3']['object']['key']
    response = s3client.get_object(Bucket=bucket, Key=csv_file)
    lines = response['Body'].read().decode('utf-8').split('\n')
    results = []
    for row in csv.DictReader(lines):
        results.append(row.values())
    print(results)
    
    connection = mysql.connector.connect(host = Hostname,
                                         database = DBName,
                                         port = PortNumber,
                                         user = UserID,
                                         passwd = Password)

    mysql_insert = """INSERT INTO Uk_Ecommerce_Data(Unique_id, InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    try:
        cursor = connection.cursor()
        cursor.executemany(mysql_insert, results)
        connection.commit()    
    except:
        connection.rollback()
        
    finally:
        connection.close()    
    
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
