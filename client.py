import socket

# Define server host and port
HOST = 'localhost'
PORT = 8000

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# TODO: move this somewhere appropriate

# Send a request to the server
request = 'list_books'
client_socket.sendall(request.encode())

# Receive and print the response from the server
response = client_socket.recv(1024).decode()
print(response)

# Close the client socket
client_socket.close()

