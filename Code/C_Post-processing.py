import json
import boto3
import ast

def lambda_handler(event, context):
    print(event)
    # event = {'Records': [{'messageId': '2a2434e2-07af-463c-8bea-306f3b6a8472', 'receiptHandle': 'AQEBj6JmrS2o0MibbNMTwdy8c7M5uTRxHZHxbp2gyA2krFYZne360td0NrKU7BRbdcU885mUlXP3zvT3EzttVAdPiqkuUfyQnZArFBMz8F/JE0ZHyo05AL6gpMjDv17fzRjA8WRcXiX4WizrmNw75CvIAFuEogLcwEYnNkoumwB7uc0bRpdgQhB7waf7O5D75Q44HwF0FHnPCPp4+d6yz+iV1chNv1xpDJqbMqpqzceXZ6h0alfx8PxAO9Q2l2yNo10eZ4MAlDMHbh7rxZpCzfwZoEccTXFpImLM1TE0Pdpg1OpiacTiACuuGQ0FGH0VuwFkwZKVqroAaA8K2fgSL8Gi9+1zWKh3DNsh8mOwjl88oNeC9bfW6dRHxWlYfdYFEG9zI2E4sFT8gocKFfiEo9nbVw==', 'body': '{"bucket_name": "dev-data-integration-512888886024-ap-southeast-2-an", "file_name": "source/tcs_products-1000.csv"}', 'attributes': {'ApproximateReceiveCount': '1', 'AWSTraceHeader': 'Root=1-6ab24cd2-9405c43457bf42bd6819d793;Parent=2f0104738820f572;Sampled=0;Lineage=2:aaa9bd69:0', 'SentTimestamp': '1790069970893', 'SenderId': 'AROAXO2UPKMEGTQR4DCGF:lamda-processing', 'ApproximateFirstReceiveTimestamp': '1790069970901'}, 'messageAttributes': {}, 'md5OfBody': '0802fe850a8120ac42330c99dee7122f', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:ap-southeast-2:512888886024:post-processing', 'awsRegion': 'ap-southeast-2'}]}
    s3_client = boto3.client('s3')
    body = event['Records'][0]['body']
    data_dict = json.loads(body) # direct ga json.loads chalu, ast vaddu
    bucket = data_dict['bucket_name']
    key = data_dict['file_name']
    # print(data_dict)
    # print(type(data_dict))
    data_dict['status'] = 'processed'
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn='arn:aws:sns:ap-southeast-2:512888886024:Emailcommunication',
        Message= str(data_dict),
        Subject='File Processing completed'
    )
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }