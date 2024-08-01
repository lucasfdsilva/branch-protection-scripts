import boto3
import json

# Load JSON data
with open('dynamodb_data.json', 'r') as file:
    items_to_load = json.load(file)

# Initialize a session using Boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
destination_table = dynamodb.Table('table-name')

# Write items to the new table
with destination_table.batch_writer() as batch:
    for item in items_to_load:
        # Convert numerical values if necessary (DynamoDB stores all numbers as Decimal)
        item['UserId'] = int(item['UserId'])
        item['IsActive'] = bool(item['IsActive'])
        item['CreatedBy'] = int(item['CreatedBy'])
        if 'UpdatedBy' in item:
            item['UpdatedBy'] = int(item['UpdatedBy'])

        # Send the item to DynamoDB
        batch.put_item(Item=item)

print("Data loading complete.")
