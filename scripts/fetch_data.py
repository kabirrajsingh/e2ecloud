import boto3

# Initialize AWS clients
ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')
rds_client = boto3.client('rds')
autoscaling_client = boto3.client('autoscaling')
cloudwatch_client = boto3.client('cloudwatch')

# Fetch EC2 instances
def fetch_ec2_instances():
    response = ec2_client.describe_instances()
    ec2_data = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            ec2_data.append({
                'instance_id': instance['InstanceId'],
                'instance_type': instance['InstanceType'],
                'region': instance['Placement']['AvailabilityZone'],
                'state': instance['State']['Name']
            })
    return ec2_data

# Fetch S3 buckets
def fetch_s3_buckets():
    response = s3_client.list_buckets()
    s3_data = []
    for bucket in response['Buckets']:
        s3_data.append({
            'bucket_name': bucket['Name'],
            'creation_date': bucket['CreationDate'].strftime("%Y-%m-%d")
        })
    return s3_data

# Fetch Lambda functions
def fetch_lambda_functions():
    response = lambda_client.list_functions()
    lambda_data = []
    for function in response['Functions']:
        lambda_data.append({
            'function_name': function['FunctionName'],
            'runtime': function['Runtime'],
            'handler': function['Handler'],
            'code_size': function['CodeSize'],
            'last_modified': function['LastModified']
        })
    return lambda_data

# Fetch RDS databases
def fetch_rds_databases():
    response = rds_client.describe_db_instances()
    rds_data = []
    for db_instance in response['DBInstances']:
        rds_data.append({
            'db_instance_id': db_instance['DBInstanceIdentifier'],
            'db_instance_class': db_instance['DBInstanceClass'],
            'engine': db_instance['Engine'],
            'storage': db_instance['AllocatedStorage'],
            'status': db_instance['DBInstanceStatus'],
        })
    return rds_data

# Fetch Auto Scaling groups
def fetch_auto_scaling_groups():
    response = autoscaling_client.describe_auto_scaling_groups()
    asg_data = []
    for asg in response['AutoScalingGroups']:
        asg_data.append({
            'asg_name': asg['AutoScalingGroupName'],
            'desired_capacity': asg['DesiredCapacity'],
            'min_size': asg['MinSize'],
            'max_size': asg['MaxSize'],
            'instances': len(asg['Instances']),
        })
    return asg_data

# Fetch CloudWatch alarms
def fetch_cloudwatch_alarms():
    response = cloudwatch_client.describe_alarms()
    alarms_data = []
    for alarm in response['MetricAlarms']:
        alarms_data.append({
            'alarm_name': alarm['AlarmName'],
            'state': alarm['StateValue'],
            'metric_name': alarm['MetricName'],
            'namespace': alarm['Namespace'],
            'evaluation_periods': alarm['EvaluationPeriods'],
        })
    return alarms_data

# Example of how to use the functions
ec2_data = fetch_ec2_instances()
s3_data = fetch_s3_buckets()
lambda_data = fetch_lambda_functions()
rds_data = fetch_rds_databases()
asg_data = fetch_auto_scaling_groups()
alarms_data = fetch_cloudwatch_alarms()

export
