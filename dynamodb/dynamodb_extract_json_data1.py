import boto3
import json
from decimal import Decimal

# Helper function to convert DynamoDB item to JSON with data types
def convert_dynamodb_item(item):
    converted_item = {}
    for key, value in item.items():
        if 'S' in value:
            converted_item[key] = {'S': value['S']}
        elif 'N' in value:
            converted_item[key] = {'N': str(value['N'])}  # Ensure numbers are strings in DynamoDB JSON
        elif 'BOOL' in value:
            converted_item[key] = {'BOOL': value['BOOL']}
        elif 'SS' in value:
            converted_item[key] = {'SS': value['SS']}
        elif 'NS' in value:
            converted_item[key] = {'NS': [str(num) for num in value['NS']]}  # Ensure numbers are strings in DynamoDB JSON
        elif 'M' in value:
            converted_item[key] = {'M': convert_dynamodb_item(value['M'])}
        elif 'L' in value:
            converted_item[key] = {'L': [convert_dynamodb_item(sub_item) if isinstance(sub_item, dict) else sub_item for sub_item in value['L']]}
        # Add more cases as needed for other DynamoDB data types
    return converted_item

# Initialize a session using Amazon DynamoDB (credentials taken from environment variables)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Select your table
table = dynamodb.Table('table-name')

# Scan the table
response = table.scan()
items = response['Items']

# Convert each item to the desired format
converted_items = [convert_dynamodb_item(item) for item in items]

# Write the converted items to a JSON file
with open('output.json', 'w') as f:
    json.dump(converted_items, f, indent=4)

print("Data has been written to output.json")
