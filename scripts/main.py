# scripts/main.py

import subprocess

def run_script(script_path):
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {script_path} executed successfully.")
        print(result.stdout)
    else:
        print(f"❌ {script_path} failed.")
        print(result.stderr)

def main():
    print("Starting Cloud Cost Optimization Workflow...\n")
    
    # Step 1: Fetch AWS Data
    run_script('scripts/fetch_aws_data.py')
    
    # Step 2: Preprocess Data
    run_script('scripts/preprocess_data.py')
    
    # Step 3: Send Data to IBM Watsonx and Get Recommendations
    run_script('scripts/send_to_watsonx.py')
    
    # Step 4: Apply Recommendations to AWS
    run_script('scripts/apply_recommendations.py')
    
    print("\nCloud Cost Optimization Workflow Completed.")

if __name__ == "__main__":
    main()
