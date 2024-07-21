from flask import Flask, render_template, request, jsonify
import requests
from functools import wraps

app = Flask(__name__)

# URLs for Gilhari microservices as running on EC2
SOURCE_URL = "http://13.127.81.92:8082/gilhari/v1"
TARGET_URL = "http://13.127.81.92:8083/gilhari/v1"

def handle_request_exception(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.RequestException as e:
            return jsonify({"error": str(e)}), 500
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view_table/<table_name>', methods=['GET'])
@handle_request_exception
def view_table(table_name):
    response = requests.get(f"{SOURCE_URL}/{table_name}")
    response.raise_for_status()
    return jsonify(response.json())

@app.route('/transfer_data', methods=['POST'])
@handle_request_exception
def transfer_data():
    source_url = f"{SOURCE_URL}/Loan"
    target_url = f"{TARGET_URL}/LoanH"
    
    response = requests.get(source_url)
    response.raise_for_status()
    loans = response.json()
    
    response=requests.delete(target_url)
    response.raise_for_status()
    
    data = {"entity": loans}
    response = requests.post(target_url, json=data)
    response.raise_for_status()
    
    response = requests.get(target_url)
    response.raise_for_status()
    transferred_data = response.json()
    
    return jsonify({
        "success": True,
        "message": "Data transferred successfully",
        "data": transferred_data
    })

@app.route('/view_postgres_data', methods=['GET'])
@handle_request_exception
def view_postgres_data():
    response = requests.get(f"{TARGET_URL}/LoanH")
    response.raise_for_status()
    return jsonify(response.json())

@app.route('/filter_data/<table_name>', methods=['GET'])
@handle_request_exception
def filter_data(table_name):
    filter_param = request.args.get('filter')
    value = request.args.get('value')
    response = requests.get(f"{SOURCE_URL}/{table_name}?filter={filter_param}={value}")
    response.raise_for_status()
    return jsonify(response.json())

@app.route('/sort_data/<table_name>', methods=['GET'])
@handle_request_exception
def sort_data(table_name):
    sort_by = request.args.get('sort_by')
    response = requests.get(f"{SOURCE_URL}/{table_name}?filter=ORDER+BY+{sort_by}")
    response.raise_for_status()
    return jsonify(response.json())
@app.route('/view_authors', methods=['GET'])
def view_authors():
    try:
        response = requests.get(f"{SOURCE_URL}/Author")
        response.raise_for_status()
        authors = response.json()
        
        for author in authors:
            if 'listBook' in author:
                author['books'] = json.loads(author['listBook'])
                del author['listBook']
        
        return jsonify(authors)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/end_application')
@handle_request_exception
def end_application():
    requests.get(f"{SOURCE_URL}/quit/now")
    requests.get(f"{TARGET_URL}/quit/now")
    return jsonify({"message": "Application is closed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='80',debug=True)