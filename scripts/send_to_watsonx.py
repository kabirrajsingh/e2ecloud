# scripts/send_to_watsonx.py

import yaml
import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def create_prompts(preprocessed_data):
    prompts = {}

    # EC2 Instances Prompt
    ec2_data = preprocessed_data['ec2_instances'].to_dict(orient='records')
    prompt_ec2 = f"Analyze the following EC2 instance usage data and provide optimization recommendations:\n{json.dumps(ec2_data, indent=2)}"
    prompts['ec2'] = prompt_ec2

    # S3 Storage Prompt
    s3_data = preprocessed_data['s3_storage'].to_dict(orient='records')
    prompt_s3 = f"Analyze the following S3 storage data and provide cost-saving recommendations:\n{json.dumps(s3_data, indent=2)}"
    prompts['s3'] = prompt_s3

    # Lambda Functions Prompt
    lambda_data = preprocessed_data['lambda_functions'].to_dict(orient='records')
    prompt_lambda = f"Review the following Lambda function data and suggest optimization strategies to reduce costs and improve performance:\n{json.dumps(lambda_data, indent=2)}"
    prompts['lambda'] = prompt_lambda

    # RDS Databases Prompt
    rds_data = preprocessed_data['rds_databases'].to_dict(orient='records')
    prompt_rds = f"Based on the following RDS database metrics, provide recommendations to optimize resource usage and reduce costs:\n{json.dumps(rds_data, indent=2)}"
    prompts['rds'] = prompt_rds

    # Auto Scaling Prompt
    auto_scaling_data = preprocessed_data['auto_scaling'].to_dict(orient='records')
    prompt_auto_scaling = f"Analyze the following auto-scaling group data and suggest strategies to optimize scaling policies and reduce costs:\n{json.dumps(auto_scaling_data, indent=2)}"
    prompts['auto_scaling'] = prompt_auto_scaling

    # CloudWatch Alarms Prompt
    alarms_data = preprocessed_data['cloudwatch_alarms'].to_dict(orient='records')
    prompt_alarms = f"Review the following CloudWatch alarm data and provide recommendations to tune alarm thresholds and actions for cost optimization:\n{json.dumps(alarms_data, indent=2)}"
    prompts['alarms'] = prompt_alarms

    # Cost Breakdown Prompt
    cost_breakdown = preprocessed_data['cost_breakdown']
    prompt_cost = f"Given the overall cost breakdown of AWS resources, identify areas for cost reduction and suggest a strategic plan to lower total cloud expenditure while maintaining performance:\n{json.dumps(cost_breakdown.to_dict(), indent=2)}"
    prompts['cost_breakdown'] = prompt_cost

    return prompts



# scripts/send_to_watsonx.py

import requests
import yaml

def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def send_prompt_to_watsonx(prompt):
    # Load the config to get the API key and service URL
    config = load_config()
    access_token = config['ibm_watsonx']['api_key']
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(access_token)
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
    service_url = config['ibm_watsonx']['service_url']
    
    # Prepare the request body
    body = {
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "repetition_penalty": 1
        },
        "model_id": "ibm/granite-13b-chat-v2",
        "project_id": "aac10742-d9eb-483e-9895-0505ac4e55b8",
        "input": prompt  # Sending the prompt to the model
    }
    
    # Set headers, including the authorization token
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"  # Bearer token for authentication
    }
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(headers)
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
    # Send the POST request to the IBM Watson ML API
    response = requests.post(service_url, headers=headers, json=body)
    
    # Check for non-200 responses and raise an exception if needed
    if response.status_code != 200:
        raise Exception(f"Non-200 response: {response.text}")
    
    # Return the response from the model
    return response.json()
