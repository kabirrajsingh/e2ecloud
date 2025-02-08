# scripts/fetch_aws_data.py

import json

def load_cloud_data(file_path='data/cloud_data.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    data = load_cloud_data()
    print("Cloud data loaded successfully.")
