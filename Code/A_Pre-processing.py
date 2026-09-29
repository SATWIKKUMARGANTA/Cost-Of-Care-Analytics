import json
import boto3

def lambda_handler(event, context):
    print(event)
    # event = {'Records': [{'eventVersion': '2.6', 'eventSource': 'aws:s3', 'awsRegion': 'ap-southeast-2', 'eventTime': '2026-09-22T06:10:47.235Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'A3LUP53QLLVJGK'}, 'requestParameters': {'sourceIPAddress': '49.204.237.136'}, 'responseElements': {'x-amz-request-id': 'Q5QBAKHED84JWNBJ', 'x-amz-id-2': 'N+McHo1KN8kA/AaLku4KQYbw7T7vWwHYIQvpuCDxRRs+vOpWNSVJUCOBZ9zyH082H7FJEaAjrgViUnQwZ1bSa6noy8Wd3WgSizqpA5MeLxg='}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': '4a252ce8-76cc-4feb-b9d1-ea55bbf5d2bb', 'bucket': {'name': 'dev-data-integration-512888886024-ap-southeast-2-an', 'ownerIdentity': {'principalId': 'A3LUP53QLLVJGK'}, 'arn': 'arn:aws:s3:::dev-data-integration-512888886024-ap-southeast-2-an'}, 'object': {'key': 'source/ingestion_hii.csv', 'size': 171225, 'eTag': '6e10696e468d0b34398a5dc6bc2bfc1b', 'sequencer': '006AB21BE734F4C7EF'}}}]}
    body = event['Records'][0]
    print(body)
    bucket = body['s3']['bucket']['name']
    file_path = body['s3']['object']['key']
    print(bucket)
    print(file_path)
    data = {'bucket_name': bucket, 'file_path': file_path}
    print(data)
    file_name = file_path.split('/')[-1]
    print(file_name)
    s3_client = boto3.client('s3')
    try:
        fileformat = file_name.split('.')[-1]
        print(fileformat)
        if fileformat.lower() == 'csv' or fileformat.lower() == 'txt':
            print("inside txt and csv")
            if file_name.lower().startswith('tcs_') or file_name.lower().startswith('ingestion_'):
                print("valid file name")
                sqs_client = boto3.client('sqs')
                sqs_client.send_message(
                    QueueUrl='https://sqs.ap-southeast-2.amazonaws.com/512888886024/pre-processing',
                    MessageBody=json.dumps(data)
                )
            else:
                raise Exception("invalid filename")
        else:
            raise Exception("unsupported file format")
    except Exception as e:
        print(str(e))
        print("error in reading data")
        folder_path = 'failure'
        error_folder_path = folder_path + '/' + file_name
        s3_client.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': file_path}, Key=error_folder_path)
        s3_client.delete_object(Bucket=bucket, Key=file_path)
        raise Exception(str(e))

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }