import socket
import sys

SERVER_IP = 'localhost'
SERVER_PORT = 8080

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"Client connected to server running at {SERVER_IP}:{SERVER_PORT}")
    print("Type your message and press Enter (Type 'exit' to quit).\n")

    while True:
        msg = input("You: ")
        if msg.lower() == 'exit':
            break
        if not msg:
            continue

        client_socket.sendall(msg.encode('utf-8'))

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