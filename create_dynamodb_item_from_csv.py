import csv
import boto3
from botocore.exceptions import ClientError

def upload_csv_to_dynamodb(table_name, csv_file_path, number_attributes, delimiter=',', region='us-east-1'):
    """
    Read a CSV file and upload its content to a DynamoDB table, converting specified attributes to numbers.

    Parameters:
        table_name (str): Name of the DynamoDB table.
        csv_file_path (str): Path to the CSV file.
        number_attributes (list): List of attribute names to convert to numbers.
        delimiter (str): Delimiter of the CSV file.
        region (str): AWS region where the DynamoDB table is hosted.
    """
    # Initialize a session using your credentials
    session = boto3.Session(region_name=region)
    # Initialize the DynamoDB service
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Open the CSV file and read data
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            # Convert specified attributes from string to number
            for attribute in number_attributes:
                if attribute in row and row[attribute].isdigit():
                    row[attribute] = int(row[attribute])

            try:
                # Insert data into the table
                response = table.put_item(Item=row)
                print(f"Added item: {response}")
            except ClientError as e:
                print(f"Failed to add item: {e.response['Error']['Message']}")

# Example usage
number_attributes = ['UserId', 'CreatedBy', 'UpdatedBy']  # Specify the names of the columns to convert
upload_csv_to_dynamodb('dynamodb-table-name', 'path-to-.csv', number_attributes)


