import socket
import sys
import time

SERVER_IP = 'localhost'
SERVER_PORT = 8000

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"Client connected to server running at {SERVER_IP}:{SERVER_PORT}")
    print("Type your message and press Enter (Type 'exit' to quit).\n")

    '''
    client_socket.sendall(b"SET na")

    time.sleep(2)

    client_socket.sendall(b"me thor\n")
    response = client_socket.recv(1024).decode("utf-8")
    print(response)
    client_socket.sendall(b"GET")
    time.sleep(1)
    client_socket.sendall(b" name\n")
    response = client_socket.recv(1024).decode("utf-8")
    print(response)
    ''''

    while True:
        msg = input()
        if msg.lower() == 'exit':
            break
        if not msg:
            continue

        client_socket.sendall((msg + "\n").encode('utf-8'))

        response = client_socket.recv(1024)
        print(f"Server echo: {response.decode('utf-8')}")

except ConnectionRefusedError:
    print(f"Connection to server {SERVER_IP}:{SERVER_PORT} failed.")
    sys.exit(1)
except Exception as e:
    print(e)
    sys.exit(1)
finally:
    client_socket.close()
    print("client socket closed.")