import socket
import threading
import sys


def handle_client(connection, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    try:
        while True:
            data = connection.recv(1024)
            if data:
                message = data.decode('utf-8', errors='ignore')
                

                print(f"[{client_address}] Received: {message}")
                
                # Echo the message back to this specific client
                connection.sendall(data)
            else:
                # No data means the client closed the connection gracefully
                break
    except ConnectionResetError:
        print(f"[DISCONNECT] Client {client_address} abruptly disconnected.")
    except socket.error as e:
        print(f"[ERROR] Network error with client {client_address}: {e}")
    finally:
        connection.close()
        print(f"[CLOSE] Connection with {client_address} closed.")


def start_server():
    server_address = ('localhost', 8000)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind(server_address)
        server_socket.listen()
        print(f"[STARTING] Server is listening on {server_address}...")
    except socket.error as e:
        print(f"[ERROR] Failed to bind/listen: {e}")
        sys.exit(1)

    try:
        while True:
            connection, client_address = server_socket.accept()

            client_thread = threading.Thread(
                target=handle_client,
                args=(connection, client_address)
            )

            client_thread.daemon = True
            client_thread.start()

            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server shutting down via Ctrl+C...")
    finally:
        server_socket.close()
        print("Server shut down successfully.")


if __name__ == "__main__":
    start_server()