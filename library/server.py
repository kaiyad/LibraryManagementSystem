import socket
import logging

logger = logging.getLogger(__name__)
# TODO: Move the host details to somewhere else
HOST = "localhost"
PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

logger.info(f"Server listening at {HOST}: {PORT}")


def handle_request(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break

        response = process_request(data)
        client_socket.sendall(response.encode())
    client_socket.close()

def process_request(request):
    if request == 'list_books':
        return "List of Books"

    return f"Invalid Request {request}"

while True:
    client_socket, address = server_socket.accept()
    logger.info(f"Connection from {address[0]}: {address[1]}")

    handle_request(client_socket)
    
