import boto3
from datetime import datetime, timedelta, timezone

DRY_RUN = True

def delete_old_amis():
    # Create a session using default AWS credentials
    ec2_client = boto3.client('ec2', region_name='us-east-1')

    # Get the current date in UTC
    current_date = datetime.now(timezone.utc)

    # Calculate the date 3 months ago
    cutoff_date = current_date - timedelta(days=90)

    # Retrieve all AMIs owned by the user
    images_response = ec2_client.describe_images(Owners=['self'])
    images = images_response['Images']

    for image in images:
        image_id = image['ImageId']
        creation_date_str = image['CreationDate']
        creation_date = datetime.strptime(creation_date_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)

        if creation_date < cutoff_date:
            print(f"Deregistering AMI: {image_id}, Created on: {creation_date_str}")

            # Deregister the AMI
            ec2_client.deregister_image(ImageId=image_id, DryRun=DRY_RUN)

            # Delete associated snapshots
            block_mappings = image.get('BlockDeviceMappings', [])
            for block in block_mappings:
                if 'Ebs' in block and 'SnapshotId' in block['Ebs']:
                    snapshot_id = block['Ebs']['SnapshotId']
                    print(f"Deleting snapshot: {snapshot_id}")
                    ec2_client.delete_snapshot(SnapshotId=snapshot_id, DryRun=DRY_RUN)

if __name__ == "__main__":
    delete_old_amis()
