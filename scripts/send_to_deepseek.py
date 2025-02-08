# scripts/send_to_watsonx.py

import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def create_prompts(preprocessed_data):
    prompts = {}  # Changed to a dictionary to store prompts with keys

    # EC2 Instances Prompt
    ec2_data = preprocessed_data['ec2_instances'].to_dict(orient='records')

    prompt_ec2 = f"""
    You are a cloud optimization expert. Below is detailed usage data for multiple EC2 instances, including resource consumption, uptime, instance types, and region.

    Analyze this data with a focus on identifying underutilized or overprovisioned instances. Provide a strategic plan that includes actions such as right-sizing,
    terminating idle instances, and changing pricing models (e.g., reserved or spot instances) to optimize cost efficiency. Additionally, offer insights into
    region-specific optimization and potential use of auto-scaling based on instance utilization patterns. Provide both technical and financial recommendations for
    optimizing EC2 usage.\n

    {json.dumps(ec2_data, indent=2)} 
    """

    prompts['ec2'] = prompt_ec2

    # S3 Storage Prompt
    s3_data = preprocessed_data['s3_storage'].to_dict(orient='records')

    prompt_s3 = f"""
    As a cloud storage expert, review the following data on S3 storage usage, including object size distribution, access frequency, and storage class.

    Focus on identifying opportunities to reduce storage costs by transitioning objects to more cost-effective storage classes such as Glacier or Intelligent-Tiering
    based on access patterns. Highlight any redundant or outdated objects that could be archived or deleted. Provide both a detailed cost-saving analysis and specific
    steps to manage storage lifecycle policies more effectively, taking into account long-term data retention and retrieval requirements.\n

    {json.dumps(s3_data, indent=2)}
    """

    prompts['s3'] = prompt_s3

    # Lambda Functions Prompt
    lambda_data = preprocessed_data['lambda_functions'].to_dict(orient='records')

    prompt_lambda = f"""
    The following is a detailed report on the usage of Lambda functions, including execution times, memory consumption, invocation frequency, and error rates.
    Analyze this data to recommend optimizations that will improve both cost efficiency and performance. Identify opportunities to adjust memory allocations,
    reduce cold start times, and improve overall function performance. Additionally, suggest any code refactoring, architectural improvements, or caching strategies
    that could further enhance cost-effectiveness and performance at scale. Provide a clear cost-performance trade-off analysis for implementing these recommendations.\n
    {json.dumps(lambda_data, indent=2)}
    """

    prompts['lambda'] = prompt_lambda  # Corrected key to 'lambda'

    # RDS Databases Prompt
    rds_data = preprocessed_data['rds_databases'].to_dict(orient='records')

    prompt_rds = f"""
    You are presented with detailed performance and cost data for various RDS instances, including resource utilization, query performance, and instance types.

    Analyze this data to recommend optimizations that will reduce operational costs while maintaining or improving database performance. Specifically, suggest
    opportunities for right-sizing database instances, leveraging reserved instances, or implementing read replicas for better query distribution. Provide strategies
    for optimizing backup and snapshot costs, and consider region-specific optimizations as well. Present a holistic cost-saving plan along with database performance improvements.\n
    {json.dumps(rds_data, indent=2)}
    """

    prompts['rds'] = prompt_rds

    # Auto Scaling Prompt
    auto_scaling_data = preprocessed_data['auto_scaling'].to_dict(orient='records')

    prompt_auto_scaling = f"""
    The following is data from several auto-scaling groups, detailing scaling events, resource consumption patterns, and trigger thresholds. Review this data and provide
    recommendations to optimize scaling policies, reduce over-provisioning, and avoid unnecessary scaling events. Analyze whether the current scaling triggers are aligned
    with real-time usage patterns and suggest more efficient strategies, such as predictive scaling or scheduled scaling based on usage forecasts. Additionally, provide
    insights into adjusting thresholds to better balance performance and cost, reducing both scaling lag and over-commitment of resources.\n
    {json.dumps(auto_scaling_data, indent=2)}
    """

    prompts['auto_scaling'] = prompt_auto_scaling

    # CloudWatch Alarms Prompt
    alarms_data = preprocessed_data['cloudwatch_alarms'].to_dict(orient='records')

    prompt_alarms = f"""
    You are tasked with analyzing CloudWatch alarm configurations and metrics, including thresholds, actions, and alarm frequency. Review this data and provide recommendations

    for tuning alarm settings to minimize false positives while maintaining the responsiveness necessary for mission-critical services. Suggest ways to optimize alarm thresholds,
    reduce unnecessary alerts, and automate actions such as scaling or instance rebooting in response to certain alarms. Provide a cost-benefit analysis of optimizing these alarms
    to ensure that cloud costs remain low without compromising system availability or performance.\n
    {json.dumps(alarms_data, indent=2)}
    """

    prompts['alarms'] = prompt_alarms

    # Cost Breakdown Prompt
    cost_breakdown = preprocessed_data['cost_breakdown']  # Removed .to_dict() here
    prompt_cost = f"""
    You are given a comprehensive cost breakdown of AWS resources, including compute, storage, networking, and miscellaneous services. Based on this breakdown, identify areas with
    the highest potential for cost reduction. Suggest optimization strategies such as rightsizing, moving to more cost-effective services, or eliminating unnecessary resources.
    Present a strategic plan for minimizing cloud expenditure, including the trade-offs between performance and cost. Additionally, propose long-term measures such as implementing
    cost governance policies and using predictive analytics to forecast future cloud spending trends.\n
    {json.dumps(cost_breakdown.to_dict(), indent=2)} # Added .to_dict() here
    """

    prompts['cost_breakdown'] = prompt_cost  # Assuming 'prompts' is defined elsewhere

    return prompts  # Assuming 'prompts' is defined and this is part of a function

def send_prompt_to_watsonx(prompt):
    client = OpenAI(
        base_url = "https://infer.e2enetworks.net/project/p-4817/genai/deepseek_r1/v1"
    )

    completion = client.chat.completions.create(
        model='deepseek_v3',
        messages=[{"role":"system","content":prompt}, {"role":"user","content":"What are your recommendations for this scenario?"}],
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=1,
        stream=True
    )
        
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    return response