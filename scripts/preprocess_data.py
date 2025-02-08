# scripts/preprocess_data.py

import pandas as pd
import json

def preprocess_ec2(ec2_instances):
    df_ec2 = pd.DataFrame(ec2_instances)
    return df_ec2

def preprocess_s3(s3_storage):
    df_s3 = pd.DataFrame(s3_storage)
    return df_s3

def preprocess_lambda(lambda_functions):
    df_lambda = pd.DataFrame(lambda_functions)
    return df_lambda

def preprocess_rds(rds_databases):
    df_rds = pd.DataFrame(rds_databases)
    return df_rds

def preprocess_auto_scaling(auto_scaling):
    df_auto_scaling = pd.DataFrame(auto_scaling)
    return df_auto_scaling

def preprocess_cloudwatch_alarms(cloudwatch_alarms):
    df_alarms = pd.DataFrame(cloudwatch_alarms)
    return df_alarms

def preprocess_cost_breakdown(cost_breakdown):
    df_cost = pd.DataFrame(list(cost_breakdown.items()), columns=['Service', 'Cost_USD'])
    return df_cost

def preprocess_all(data):
    preprocessed_data = {
        'ec2_instances': preprocess_ec2(data['ec2_instances']),
        's3_storage': preprocess_s3(data['s3_storage']),
        'lambda_functions': preprocess_lambda(data['lambda_functions']),
        'rds_databases': preprocess_rds(data['rds_databases']),
        'auto_scaling': preprocess_auto_scaling(data['auto_scaling']),
        'cloudwatch_alarms': preprocess_cloudwatch_alarms(data['cloudwatch_alarms']),
        'cost_breakdown': preprocess_cost_breakdown(data['cost_breakdown'])
    }
    return preprocessed_data

if __name__ == "__main__":
    from fetch_aws_data import load_cloud_data
    data = load_cloud_data()
    preprocessed_data = preprocess_all(data)
    for key, df in preprocessed_data.items():
        print(f"{key} preprocessed with shape {df.shape}")
