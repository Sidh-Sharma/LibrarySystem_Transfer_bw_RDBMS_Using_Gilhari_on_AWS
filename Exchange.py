import requests
import json
from concurrent.futures import ThreadPoolExecutor
from functools import partial

def fetch_sorted_loans(source_url):
    """Fetch loan data from the source database and sort it by loan_date."""#GET request
    response = requests.get(source_url)
    response.raise_for_status()
    loans = response.json()
    return sorted(loans, key=lambda x: x['loan_date'])#note the use of key to use the relevant field in the json data. sorted is a built-in function. use flag reverse = True to sort in descending order

def clear_existing_loans(target_url): #for clarity
    """Clear all pre-existing Loan History objects in the target database."""
    response = requests.delete(target_url)
    response.raise_for_status()

def post_loans(target_url, sorted_loans):
    """Post sorted loan data to the target database."""#POST request
    data = {"entity": sorted_loans}
    response = requests.post(target_url, json=data)
    response.raise_for_status()

def confirm_transfer(target_url):
    """Confirm data transfer and print results."""
    response = requests.get(target_url)
    response.raise_for_status()
    print("Data transfer confirmed. Here are the posted records:")
    print(json.dumps(response.json(), indent=4))

def handle_request(func, *args):
    """Execute a function and handle potential request exceptions."""
    try:
        func(*args)
        print(f"Successfully executed: {func.__name__}")
    except requests.RequestException as e:
        print(f"Error in {func.__name__}: {e}")
        raise

def main():
    source_url = "http://localhost:8082/gilhari/v1/Loan" #first gilhari instance
    target_url = "http://localhost:8080/gilhari/v1/LoanH" #second gilhari instance
    
    try:
        sorted_loans = fetch_sorted_loans(source_url)
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(handle_request, clear_existing_loans, target_url),
                executor.submit(handle_request, post_loans, target_url, sorted_loans)
            ]
            for future in futures:
                future.result()
        
        confirm_transfer(target_url)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()