'''import json
 
import os
os.environ["AWS_REGION"] = "us-east-1"

from hello_world.app import lambda_handler 
# Test for GET request
def test_get_count():
    # Fake event for GET method
    event = {
        "requestContext": {
            "http": {
                "method": "GET"
            }
        }
    }
    

    context = {}

    # Call the Lambda function
    response = lambda_handler(event, context)

    # Check that status code is 200
    assert response["statusCode"] == 200

    # Check that response contains a count
    body = json.loads(response["body"])
    assert "count" in body

# Test for POST request
def test_increment_count():
    # Fake event for POST method
    event = {
        "requestContext": {
            "http": {
                "method": "POST"
            }
        }
    }

    context = {}

    response = lambda_handler(event, context)

    assert response["statusCode"] == 200

    body = json.loads(response["body"])
    assert "count" in body  # Because your Lambda returns updated count'''

###########WORKS 
'''
# tests/test_lambda_function.py
import os
import boto3
import json
import pytest
from moto import mock_dynamodb
from hello_world import app

@mock_dynamodb
def test_lambda_handler_get():
    os.environ['TABLE_NAME'] = 'visitor_count_table'

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # Create the DynamoDB table mock
    table = dynamodb.create_table(
        TableName='visitor_count_table',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    # Add a mock item to the table
    table.put_item(Item={'id': 'visitor', 'count': 0})

    # Mock the event for a GET request
    event = {
        "requestContext": {
            "http": {
                "method": "GET"
            }
        }
    }

    # Call the Lambda handler function
    response = app.lambda_handler(event, None)
    body = json.loads(response['body'])

    # Assert the expected response
    assert response['statusCode'] == 200
    assert 'count' in body
    assert body['count'] == 0

@mock_dynamodb
def test_lambda_handler_post():
    os.environ['TABLE_NAME'] = 'visitor_count_table'

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # Create the DynamoDB table mock
    table = dynamodb.create_table(
        TableName='visitor_count_table',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    # Add a mock item to the table
    table.put_item(Item={'id': 'visitor', 'count': 0})

    # Mock the event for a POST request
    event = {
        "requestContext": {
            "http": {
                "method": "POST"
            }
        }
    }

    # Call the Lambda handler function
    response = app.lambda_handler(event, None)
    body = json.loads(response['body'])

    # Assert the expected response
    assert response['statusCode'] == 200
    assert 'count' in body
    assert body['count'] == 1
'''
######################

import json
import boto3
import os
from moto import mock_dynamodb
from hello_world import app  # Import your app with lambda_handler

# Test for GET request (retrieve current visitor count)
@mock_dynamodb
def test_lambda_handler_get():
    os.environ['TABLE_NAME'] = 'visitor_count_table'  # Set table name

    # Set up mock DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(
        TableName='visitor_count_table',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    table.put_item(Item={'id': 'visitor', 'count': 0})  # Add a visitor item

    # Simulate GET request
    event = {"requestContext": {"http": {"method": "GET"}}}
    response = app.lambda_handler(event, None)

    # Check if status code is 200
    assert response['statusCode'] == 200, "GET request failed"  # Fail if not 200

    # Check if the visitor count is 0
    response_body = json.loads(response['body'])
    assert response_body['count'] == 0, "Visitor count is not 0"  # Fail if count is not 0

    print("GET request test passed!")

# Test for POST request (increment visitor count)
@mock_dynamodb
def test_lambda_handler_post():
    os.environ['TABLE_NAME'] = 'visitor_count_table'  # Set table name

    # Set up mock DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(
        TableName='visitor_count_table',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    table.put_item(Item={'id': 'visitor', 'count': 0})  # Add a visitor item

    # Simulate POST request
    event = {"requestContext": {"http": {"method": "POST"}}}
    response = app.lambda_handler(event, None)

    # Check if status code is 200
    assert response['statusCode'] == 200, "POST request failed"  # Fail if not 200

    # Check if the visitor count was incremented to 1
    response_body = json.loads(response['body'])
    assert response_body['count'] == 1, "Visitor count not incremented"  # Fail if count is not 1

    print("POST request test passed!")

# Run the tests
if __name__ == '__main__':
    test_lambda_handler_get()  # Run GET test
    test_lambda_handler_post()  # Run POST test

