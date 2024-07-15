from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

#URLs for Gilhari microservices as running on EC2
SOURCE_URL = "http://65.2.121.67:8082/gilhari/v1"
TARGET_URL = "http://65.2.121.67:8083/gilhari/v1"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view_table/<table_name>', methods=['GET'])
def view_table(table_name):
    try:
        response = requests.get(f"{SOURCE_URL}/{table_name}")
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)})

@app.route('/transfer_data', methods=['POST'])
def transfer_data():
    source_url = f"{SOURCE_URL}/Loan"
    target_url = f"{TARGET_URL}/LoanH"
    
    try:
        response = requests.get(source_url)
        response.raise_for_status()
        loans = response.json()
        sorted_loans = sorted(loans, key=lambda x: x['loan_date'])
        
        
        requests.delete(target_url)
        
        data = {"entity": sorted_loans}
        response = requests.post(target_url, json=data)
        response.raise_for_status()
        
        response = requests.get(target_url)
        response.raise_for_status()
        transferred_data = response.json()
        
        return jsonify({"success": True, "message": "Data transferred successfully", "data": transferred_data})
    except requests.RequestException as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/view_postgres_data', methods=['GET'])
def view_postgres_data():
    try:
        response = requests.get(f"{TARGET_URL}/LoanH")
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
