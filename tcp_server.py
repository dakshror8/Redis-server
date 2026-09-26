import socket
import sys

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print(f"Server is listening on {server_address[0]}:{server_address[1]}.")
except socket.error as e:
    print(f"Failed to bind/listen on socket: {e}")
    sys.exit(1)

try:
    while True:
        
        connection, client_address = server_socket.accept()    

        try:
            print(f"Connected to {client_address}")

            while True:
                data = connection.recv(1024)
                if data:
                    print(f"Received data: {data.decode('utf-8')}")
                    connection.sendall(data)
                else:
                    break
        except ConnectionResetError:
            print(f"Client {client_address} abruptly disconnected.")
        except socket.error as e:
            print(f"Network error with client {client_address}:{e}")
        finally:
            connection.close()
            print(f"Connection with {client_address} closed.")

except KeyboardInterrupt:
    print("\nServer is shutting down from Keyboard Interrupt.")
    sys.exit(1)
finally:
    server_socket.close()
    print("Server socket closed successfully.")
