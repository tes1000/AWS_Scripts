import boto3

regions = [
    "ap-south-1", "eu-north-1", "eu-west-3", "eu-west-2", "eu-west-1",
    "ap-northeast-3", "ap-northeast-2", "ap-northeast-1", "ca-central-1",
    "sa-east-1", "ap-southeast-1", "ap-southeast-2", "eu-central-1",
    "us-east-1", "us-east-2", "us-west-1", "us-west-2"
]

# Iterate through regions and list AMIs
for region in regions:
    print(f"Listing AMIs in region: {region}")
    try:
        # Initialize boto3 EC2 client for the specific region
        ec2_client = boto3.client("ec2", region_name=region)
        
        # Describe images owned by the account
        response = ec2_client.describe_images(Owners=["self"])
        
        # Extract and print relevant details
        images = response.get("Images", [])
        for image in images:
            print(f"AMI ID: {image['ImageId']}, Name: {image.get('Name', 'N/A')}, Creation Date: {image['CreationDate']}")
    except Exception as e:
        print(f"Error listing AMIs in region {region}: {e}")
