import json
import socket
from icp_api import PipelineHandler

HOST = "localhost"
PORT = 60371


def handle_client(
    client_socket,
):
    pipeline_handler = PipelineHandler()
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break

        # Parse the received JSON data
        try:
            json_data = json.loads(data)
        except ValueError:
            print(f"Invalid JSON data received: '{data}'")
            continue

        try:
            handler = getattr(pipeline_handler, f"handle_{json_data['method']}")
            response_data = handler(json_data)
            response_json = json.dumps(response_data)
        except Exception as e:
            response_data = {
                "success": False,
                "error": str(e),
            }
            response_json = json.dumps(response_data)

        # Convert the response JSON to a string

        # Send the response back to the client
        client_socket.send(response_json.encode("utf-8"))

    # Close the client socket
    client_socket.close()


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connected from {client_address[0]}:{client_address[1]}")
        handle_client(client_socket)

    # Close the server socket
    server_socket.close()


if __name__ == "__main__":
    # Start the server
    start_server(HOST, PORT)
