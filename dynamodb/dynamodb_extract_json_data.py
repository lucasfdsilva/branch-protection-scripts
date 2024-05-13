import boto3
import json
from decimal import Decimal

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('quantsal-dev-usermaster')

# Helper function to convert Decimals from DynamoDB to float
def convert_decimals(obj):
    if isinstance(obj, Decimal):
        # Convert decimal instances to float. Adjust based on your precision requirements.
        return float(obj)
    elif isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    else:
        return obj

# Scan the table
response = table.scan()

# List to hold all items, converting Decimals to floats
all_items = [convert_decimals(item) for item in response['Items']]

# Handle pagination
while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    all_items.extend([convert_decimals(item) for item in response['Items']])

# Save to a JSON file
with open('dynamodb_data.json', 'w') as file:
    json.dump(all_items, file)

print("Data extraction complete.")
