import socket
import threading
import sys
import shlex
import time


store = {}
lock = threading.Lock()

def handle_client(connection, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    buffer = b""
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break

            buffer += data

            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)

                request = shlex.split(line.decode("utf-8"))
                
                response = command_parser(request)

                connection.sendall(response.encode("utf-8"))


    except ConnectionResetError:
        print(f"[DISCONNECT] Client {client_address} abruptly disconnected.")
    except socket.error as e:
        print(f"[ERROR] Network error with client {client_address}: {e}")
    finally:
        connection.close()
        print(f"[CLOSE] Connection with {client_address} closed.")



def command_parser(request):
    if len(request) == 0:
        return "ERROR Empty request."

    if request[0] == 'PING':
        return ping_handler()

    match(request[0]):
        case "GET":
            if len(request) != 2:
                return "ERROR GET need a key."
            key = request[1]
            return get_handler(key)
        case "SET":
            if len(request) != 3:
                return "Invalid [SET] command."
            key = request[1]
            value = request[2]
            return set_handler(key, value)
        case "DEL":
            if len(request) != 2:
                return "ERROR DEL need a key."
            key = request[1]
            return del_handler(key)
        case "INCR":
            if len(request) != 2:
                return "ERROR INCR need a key."
            key = request[1]
            return incr_handler(key)
        case _:
            return "Invalid request."

def ping_handler():
    return "PONG"

def get_handler(key):
    if key not in store:
        return f"Key [{key}] does not exist."
    return store[key]

def set_handler(key, value):
    store[key] = value
    return "SET"

def del_handler(key):
    if key not in store:
        return f"Key [{key}] does not exist."
    del store[key]
    return "DEL"

def incr_handler(key):
    if key not in store:
        return f"ERROR [{key}] does not exist."
    with lock:
        '''
        try:
            tmp = int(store[key])
        except ValueError:
            print(f"ERROR [{key}] is not an integer.")
            
        
        time.sleep(1)
        tmp += 1
        time.sleep(1)
        
        store[key] = str(tmp)
        '''
        store[key] = str(int(store[key]) + 1)
        
        return "OK"

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