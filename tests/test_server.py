import sys

sys.path.append("./reproduce")

from reproduce.server import start_server

import socket
import json
import threading


HOST = "localhost"  # The server's hostname or IP address
PORT = 60371  # The port used by the server


def start_server_thread():
    server_thread = threading.Thread(target=start_server, args=(HOST, PORT))
    server_thread.daemon = True
    server_thread.start()

    while True:
        try:
            # Try connecting to the server
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_socket.connect((HOST, PORT))
            temp_socket.close()
            break
        except ConnectionRefusedError:
            # Server is not yet listening, wait and try again
            continue


def create_and_communicate_client(input_json):
    # Prepare a JSON message
    message_json = json.dumps(input_json)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(message_json.encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")

    # Parse the response JSON
    response_json = json.loads(response)
    return response_json


def test_handle_register():
    start_server_thread()

    in_message = {
        "method": "register",
        "video_paths": [
            "video_path_1",
            "video_path_2",
        ],
    }
    out_message = create_and_communicate_client(in_message)
    print(out_message)

    assert out_message["success"]
    assert out_message["error"] is None
    assert len(out_message["video_guids"]) == 2
