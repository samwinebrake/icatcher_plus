import json
import socket

import paramiko
# from icp_api import PipelineHandler
from flask import Flask, request,jsonify
from flask_socketio import SocketIO,emit, send
from flask_cors import CORS

HOST = "localhost"
PORT = 5001

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gaze_coding'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")

def handle_client(
    client_socket,
):
    # pipeline_handler = PipelineHandler()
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
            # response_data = handler(json_data)
            # response_json = json.dumps(response_data)
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


def start_server(app, host, port):
    socketio = SocketIO(app,cors_allowed_origins="*")


    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connected from {client_address[0]}:{client_address[1]}")
        handle_client(client_socket)

    # Close the server socket
    server_socket.close()

def check_connection(ssh_client):
    """
    This will check if the connection is still availlable. is_active can sometimes return false posivies, 
    so seeing if the connection fails is the safest way to get a true positive one way or the other.

    Return (bool) : True if it's still alive, False otherwise.
    """
    try:
        ssh_client.exec_command('ls', timeout=5)
        return True
    except Exception as e:
        return False

def run_icatcher_remote(host, username, password, ic_path, data_path, use_key=False):
    #Here we ssh into the openmind cluster and can run our sbatch command
    #The final configuration of this will depend on how we specifically deliver iCatcher.
    
    #This will check to see if the client is still connected to the ssh instance, if it is, it will return
    if check_connection == True:
        client.exec_command("")
    else:
        client.connect(host, username=username, password=password)
    
    #Actual logic goes here
    # if conda_module == None:
        # _stdin, _stdout,_stderr = client.exec_command("sbatch --wrap "")
    #     _stdin, _stdout,_stderr = client.exec_command(f"sbatch {ic_path} ")
    # else:
    #     _stdin, _stdout,_stderr = client.exec_command(f"conda activate {conda_module}")

    
    #Test command to ensure that it can connect
    _stdin, _stdout,_stderr = client.exec_command("touch test_ssh.txt")
    client.close()


@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data':'This text was fetched using an HTTP call to server on render'}
    print("HTTP Call")
    return jsonify(data)

@socketio.on("connect")
def connected(data):
    """event listener when client connects to the server"""
    # print(request.sid)
    print("client has connected")
    print(data)
    emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on('data')
def handle_message(data):
    """
    Event listener when client types a message
    TODO: Could be nice to put logic for "remote or local" here
    """
    print("data from the front end: ",str(data))
    try:
        print(data)
        response_data = data
        # data = json.loads(data)
        # host = data['host']
        # username = data['username']
        # password = data['password']
        # ic_path = data['ic_path']
        # data_path = data['data_path']
    except:
        response_data = ""
    emit('Test')
    emit("data",{'data':response_data,'id':request.sid},broadcast=True)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)

if __name__ == "__main__":
    #Vars for testing
    host = "openmind7.mit.edu"
    username = "*"
    password = "*"
    ic_path = ""
    data_path = ""

    # Start the server
    # start_server(app, HOST, PORT)
    socketio.run(app, debug=True,port=PORT)