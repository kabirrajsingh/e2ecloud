from flask import Flask, jsonify, request
from flask_cors import CORS
from scripts.fetch_aws_data import load_cloud_data
from scripts.send_to_watsonx import create_prompts, send_prompt_to_watsonx
from scripts.preprocess_data import preprocess_all
from scripts.apply_recommendations import main as apply_recommendations_main

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests for the React frontend

# Load cloud data on server start
cloud_data = load_cloud_data()
preprocessed_data = preprocess_all(cloud_data)
prompts = create_prompts(preprocessed_data)

# Endpoint 1: Get filtered data
@app.route('/api/get-data', methods=['GET'])
def get_data():
    return jsonify(cloud_data)

# Endpoint 2: Send prompt to the model (support for multiple keys)
@app.route('/api/get-analytics', methods=['POST'])
def send_prompt():
    data = request.json
    prompt_keys = data.get('prompt_keys', ['ec2'])  # Default to 'ec2' if no key is provided

    # Ensure prompt_keys is a list, convert if a single key is provided
    if isinstance(prompt_keys, str):
        prompt_keys = [prompt_keys]

    combined_prompt = ""
    
    # Loop through provided prompt_keys and append corresponding prompts
    for prompt_key in prompt_keys:
        if prompt_key in prompts:
            combined_prompt += prompts[prompt_key] + "\n\n"
        else:
            return jsonify({"error": f"Invalid prompt key: {prompt_key}"}), 400
    
    # Send the combined prompt to IBM Watsonx
    print("Combined prompt:\n", combined_prompt)
    recommendations = send_prompt_to_watsonx(combined_prompt)

    return jsonify({"recommendations": recommendations})

# Endpoint 3: Apply recommendations
@app.route('/api/apply-recommendations', methods=['POST'])
def apply_recommendations():
    apply_recommendations_main()  # Calling the apply_recommendations script
    return jsonify({"response": "Recommendations applied successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
