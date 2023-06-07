from jsonrpcclient import request 
import requests

# Define the RPC endpoint
url = "http://localhost:5001"

# Send a request to the server
response = requests.post(url=url, json=request("process_request", ["list_books"]))
print(response.json())  # Print the response from the server

