import json
import boto3
import os
import ast
import pandas as pd
import numpy as np
import io
from sqlalchemy import create_engine

def lambda_handler(event, context):
    print(event)
    s3_client = boto3.client('s3')
    # event = {'Records': [{'messageId': '4289bfce-388c-4916-95c5-ab01eb47fd31', 'receiptHandle': 'AQEB1mADmUnwKXerAmUCS3lg+vAyOdkzo60LRzWEss5PH+7Kg4N42uFDUqUekl+2xbApeNoW+/7Z0L0bRB783t8OCSP+aUSLTWZ1C2gaePc5YBrgqFC/xO9+SG3nLsowAkN1PrJIHguq6GKs40xjb5MFyhQBXkUVs8AfEYBzbJ+eNCkK5+JSfzigIlQoctUi5j9QIWbzb/ofITX25r96KWRFIJ8KbXgkrMsRcrujrG6ZGhcteuw4OFUwco5nfh4He3/0lY7dQWJ7rGYoMS9SEJWhLcnie4EiSO/auz/9x9fj51ndseilLKWfkYBr3C6YE1XXJKpFMMd9d9fs0G7uuysXwJoDKd7dPl6E5/CkggsV/EfOmtH4+6avq7X+zHglkit8///9lC9kyTcNmC0U1N5Kpg==', 'body': '{"bucket_name": "dev-data-integration-512888886024-ap-southeast-2-an", "file_path": "source/ingestion_hii.csv"}', 'attributes': {'ApproximateReceiveCount': '6', 'AWSTraceHeader': 'Root=1-6ab24ab1-53465f0a171d2f226c6852ce;Parent=7e78fbd4d8aedad0;Sampled=0;Lineage=1:4d5784b7:0', 'SentTimestamp': '1790069428488', 'SenderId': 'AROAXO2UPKMEGTQR4DCGF:pre-processing', 'ApproximateFirstReceiveTimestamp': '1790069428496'}, 'messageAttributes': {}, 'md5OfBody': 'e791a60ded736093e4dc2f0418edb5d2', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:ap-southeast-2:512888886024:pre-processing', 'awsRegion': 'ap-southeast-2'}]}
    body = event['Records'][0]['body']
    json_body  = ast.literal_eval(body)
    print(json_body)
    bucket_name = json_body['bucket_name']
    print(bucket_name)
    file_name = json_body['file_path']
    print(file_name)
    data = {'bucket_name': bucket_name, 'file_name': file_name}
    print(data)
    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    print(response)
    file_stream = io.BytesIO(response['Body'].read())
    df = pd.read_csv(file_stream)
    print(df)
    secretet = boto3.client('secretsmanager')
    response_secret = secretet.get_secret_value(SecretId=os.environ['lambdacredentials'])
    #print(response_secret)
    secret = json.loads(response_secret['SecretString'])
    print(secret)

    host = secret['host']
    engine = secret['engine']
    password = secret['password']
    username = secret['username']
    port = secret['port']
    engine = create_engine('postgresql://'+username+':'+password+'@'+host+':'+str(port)+'/'+engine)
    df.to_sql('standard', engine, if_exists='append', index=False)
    sqs_client = boto3.client('sqs')
    sqs_client.send_message(
        QueueUrl='https://sqs.ap-southeast-2.amazonaws.com/512888886024/post-processing',
        MessageBody=json.dumps(data)
     )
    # # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }