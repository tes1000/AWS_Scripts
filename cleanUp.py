import boto3

regions = [
    "ap-south-1", "eu-north-1", "eu-west-3", "eu-west-2", "eu-west-1",
    "ap-northeast-3", "ap-northeast-2", "ap-northeast-1", "ca-central-1",
    "sa-east-1", "ap-southeast-1", "ap-southeast-2", "eu-central-1",
    "us-east-1", "us-east-2", "us-west-1", "us-west-2"
]

def delete_unused_volumes(region):
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])
    volumes = response.get("Volumes", [])
    for volume in volumes:
        volume_id = volume["VolumeId"]
        try:
            print(f"Deleting unused volume: {volume_id} in region {region}")
            ec2.delete_volume(VolumeId=volume_id)
        except Exception as e:
            print(f"Failed to delete volume {volume_id} in region {region}: {e}")

def delete_unused_network_interfaces(region):
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_network_interfaces(Filters=[{"Name": "status", "Values": ["available"]}])
    interfaces = response.get("NetworkInterfaces", [])
    for interface in interfaces:
        interface_id = interface["NetworkInterfaceId"]
        try:
            print(f"Deleting unused network interface: {interface_id} in region {region}")
            ec2.delete_network_interface(NetworkInterfaceId=interface_id)
        except Exception as e:
            print(f"Failed to delete network interface {interface_id} in region {region}: {e}")

def delete_unused_security_groups(region):
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_security_groups()
    security_groups = response.get("SecurityGroups", [])
    for sg in security_groups:
        group_id = sg["GroupId"]
        group_name = sg["GroupName"]
        if group_name == "default":  # Skip default security group
            continue
        try:
            if not sg.get("IpPermissions") and not sg.get("IpPermissionsEgress"):  # No rules
                print(f"Deleting unused security group: {group_id} ({group_name}) in region {region}")
                ec2.delete_security_group(GroupId=group_id)
        except Exception as e:
            print(f"Failed to delete security group {group_id} in region {region}: {e}")

def delete_unused_load_balancers(region):
    elb = boto3.client("elb", region_name=region)
    response = elb.describe_load_balancers()
    load_balancers = response.get("LoadBalancerDescriptions", [])
    for lb in load_balancers:
        lb_name = lb["LoadBalancerName"]
        try:
            print(f"Deleting unused load balancer: {lb_name} in region {region}")
            elb.delete_load_balancer(LoadBalancerName=lb_name)
        except Exception as e:
            print(f"Failed to delete load balancer {lb_name} in region {region}: {e}")

def delete_unused_target_groups(region):
    elbv2 = boto3.client("elbv2", region_name=region)
    response = elbv2.describe_target_groups()
    target_groups = response.get("TargetGroups", [])
    for tg in target_groups:
        tg_arn = tg["TargetGroupArn"]
        try:
            print(f"Deleting unused target group: {tg_arn} in region {region}")
            elbv2.delete_target_group(TargetGroupArn=tg_arn)
        except Exception as e:
            print(f"Failed to delete target group {tg_arn} in region {region}: {e}")

def aws_cleanup():
    for region in regions:
        print(f"Starting cleanup of {region}")
        delete_unused_volumes(region)
        delete_unused_network_interfaces(region)
        delete_unused_security_groups(region)
        delete_unused_load_balancers(region)
        delete_unused_target_groups(region)
        print(f"Cleanup {region} completed!")

if __name__ == "__main__":
    aws_cleanup()
