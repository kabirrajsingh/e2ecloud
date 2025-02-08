# scripts/apply_recommendations.py

import json
import yaml
import boto3

def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_recommendations(file_path='data/recommendations.json'):
    with open(file_path, 'r') as file:
        recommendations = json.load(file)
    return recommendations

def resize_ec2_instance(ec2_client, instance_id, new_instance_type):
    try:
        ec2_client.stop_instances(InstanceIds=[instance_id])
        ec2_client.modify_instance_attribute(InstanceId=instance_id, Attribute='instanceType', Value=new_instance_type)
        ec2_client.start_instances(InstanceIds=[instance_id])
        print(f"EC2 Instance {instance_id} resized to {new_instance_type}.")
    except Exception as e:
        print(f"Error resizing EC2 Instance {instance_id}: {e}")

def terminate_ec2_instance(ec2_client, instance_id):
    try:
        ec2_client.terminate_instances(InstanceIds=[instance_id])
        print(f"EC2 Instance {instance_id} terminated.")
    except Exception as e:
        print(f"Error terminating EC2 Instance {instance_id}: {e}")

def apply_s3_optimization(s3_client, bucket_name, action, storage_class=None):
    try:
        if action == 'move_to_glacier':
            # Transition objects to Glacier
            s3_client.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration={
                    'Rules': [{
                        'ID': 'Move to Glacier',
                        'Filter': {'Prefix': ''},
                        'Status': 'Enabled',
                        'Transitions': [{
                            'Days': 30,
                            'StorageClass': 'GLACIER'
                        }]
                    }]
                }
            )
            print(f"S3 Bucket {bucket_name} lifecycle policy updated to move objects to Glacier.")
        elif action == 'update_storage_class' and storage_class:
            # Update storage class for all objects
            response = s3_client.list_objects_v2(Bucket=bucket_name)
            for obj in response.get('Contents', []):
                s3_client.copy_object(
                    Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': obj['Key']},
                    Key=obj['Key'],
                    StorageClass=storage_class,
                    MetadataDirective='COPY'
                )
            print(f"S3 Bucket {bucket_name} objects updated to {storage_class} storage class.")
    except Exception as e:
        print(f"Error optimizing S3 Bucket {bucket_name}: {e}")

def adjust_auto_scaling(asg_client, group_name, desired_capacity):
    try:
        asg_client.update_auto_scaling_group(
            AutoScalingGroupName=group_name,
            DesiredCapacity=desired_capacity
        )
        print(f"Auto Scaling Group {group_name} desired capacity updated to {desired_capacity}.")
    except Exception as e:
        print(f"Error updating Auto Scaling Group {group_name}: {e}")

def main():
    config = load_config()
    recommendations = load_recommendations()

    # Initialize AWS clients
    ec2_client = boto3.client(
        'ec2',
        aws_access_key_id=config['aws']['access_key_id'],
        aws_secret_access_key=config['aws']['secret_access_key'],
        region_name=config['aws']['region_name']
    )

    s3_client = boto3.client(
        's3',
        aws_access_key_id=config['aws']['access_key_id'],
        aws_secret_access_key=config['aws']['secret_access_key'],
        region_name=config['aws']['region_name']
    )

    asg_client = boto3.client(
        'autoscaling',
        aws_access_key_id=config['aws']['access_key_id'],
        aws_secret_access_key=config['aws']['secret_access_key'],
        region_name=config['aws']['region_name']
    )

    # Apply EC2 Recommendations
    ec2_recommendations = recommendations.get('ec2_instances', [])
    for rec in ec2_recommendations:
        instance_id = rec.get('instance_id')
        action = rec.get('action')  # e.g., 'resize', 'terminate'
        new_type = rec.get('new_instance_type', None)
        if action == 'resize' and new_type:
            resize_ec2_instance(ec2_client, instance_id, new_type)
        elif action == 'terminate':
            terminate_ec2_instance(ec2_client, instance_id)

    # Apply S3 Recommendations
    s3_recommendations = recommendations.get('s3_storage', [])
    for rec in s3_recommendations:
        bucket_name = rec.get('bucket_name')
        action = rec.get('action')  # e.g., 'move_to_glacier', 'update_storage_class'
        storage_class = rec.get('storage_class', None)
        apply_s3_optimization(s3_client, bucket_name, action, storage_class)

    # Apply Auto Scaling Recommendations
    auto_scaling_recommendations = recommendations.get('auto_scaling', [])
    for rec in auto_scaling_recommendations:
        group_name = rec.get('auto_scaling_group')
        desired_capacity = rec.get('recommended_desired_capacity')
        adjust_auto_scaling(asg_client, group_name, desired_capacity)

    print("All recommendations applied successfully.")

if __name__ == "__main__":
    main()
