import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# Initialize a session using Boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('table-name')

def fetch_all_items():
    response = table.scan()
    items = response['Items']
    
    # Handle pagination if the dataset is large
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    
    return items

def update_is_active(items):
    for item in items:
        # Convert 'IsActive' to a number
        is_active_value = item.get('IsActive')
        if isinstance(is_active_value, bool):
            is_active_number = 1 if is_active_value else 0
        elif isinstance(is_active_value, (int, Decimal)):  # Check if it's already a number
            is_active_number = int(is_active_value)  # Ensure it's an integer
        else:
            continue  # If it's not clear how to convert, skip it

        # Update the item in the table
        table.update_item(
            Key={
                'UserId': item['UserId'],  # Adjust this to your table's primary key attribute
                # Add your sort key here if you have one, e.g., 'YourSortKey': item['YourSortKey']
            },
            UpdateExpression='SET IsActive = :val',
            ExpressionAttributeValues={
                ':val': is_active_number
            }
        )

# Main execution logic
items = fetch_all_items()
update_is_active(items)
print("All items have been updated.")
