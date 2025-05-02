'''
import json

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
'''

'''
import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Read the visitor count
    if event['requestContext']['http']['method'] == 'GET':
        response = table.get_item(Key={'id': 'visitor'})
        count = response.get('Item', {}).get('count', 0)
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            },
            'body': json.dumps({'count': count})
        }

    # Increment the visitor count
    elif event['requestContext']['http']['method'] == 'POST':
        table.update_item(
            Key={'id': 'visitor'},
            UpdateExpression='ADD #c :inc',
            ExpressionAttributeNames={'#c': 'count'},
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Methods": "*",
                'Access-Control-Allow-Headers': '*'
            },
            'body': json.dumps({'message': 'Count updated'})
        }

    # Unsupported method
    return {
        'statusCode': 405,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps({'message': 'Method not allowed'})
    }
'''
'''
import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Common CORS headers
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*'
    }

    # Read the visitor count (GET method)
    if event['requestContext']['http']['method'] == 'GET':
        response = table.get_item(Key={'id': 'visitor'})
        count = response.get('Item', {}).get('count', 0)
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'count': count})
        }

    # Increment the visitor count (POST method)
    elif event['requestContext']['http']['method'] == 'POST':
        table.update_item(
            Key={'id': 'visitor'},
            UpdateExpression='ADD #c :inc',
            ExpressionAttributeNames={'#c': 'count'},
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'message': 'Count updated'})
        }

    # Unsupported method
    return {
        'statusCode': 405,
        'headers': cors_headers,
        'body': json.dumps({'message': 'Method not allowed'})
    }
'''
##working 
'''import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

# Custom JSON encoder to handle Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)  # or float(obj) if needed
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*'
    }

    method = event['requestContext']['http']['method']

    if method == 'GET':
        response = table.get_item(Key={'id': 'visitor'})
        count = response.get('Item', {}).get('count', 0)
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'count': count}, cls=DecimalEncoder)
        }

    elif method == 'POST':
        result = table.update_item(
            Key={'id': 'visitor'},
            UpdateExpression='ADD #c :inc',
            ExpressionAttributeNames={'#c': 'count'},
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )
        updated_count = result['Attributes']['count']
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'count': updated_count}, cls=DecimalEncoder)
        }

    return {
        'statusCode': 405,
        'headers': cors_headers,
        'body': json.dumps({'message': 'Method not allowed'})
    }'''
import json
import os
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = os.environ.get('TABLE_NAME', 'visitor_count_table')
    table = dynamodb.Table(table_name)

    method = event["requestContext"]["http"]["method"]

    if method == "GET":
        response = table.get_item(Key={'id': 'visitor'})
        count = response.get('Item', {}).get('count', 0)
        return {
            'statusCode': 200,
            'body': json.dumps({'count': int(count)})
        }

    elif method == "POST":
        response = table.update_item(
            Key={'id': 'visitor'},
            UpdateExpression='ADD #count :inc',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )
        count = response['Attributes']['count']
        return {
            'statusCode': 200,
            'body': json.dumps({'count': int(count)})
        }

    return {
        'statusCode': 405,
        'body': json.dumps({'message': 'Method not allowed'})
    }
