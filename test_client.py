import socket
import threading

def client(x):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost',8000))

    client_socket.sendall(f"INCR {x}\n".encode())
    
    response = client_socket.recv(1024)

    print(response.decode())

    client_socket.close()

threads = []
for i in range(9000):
    t = threading.Thread(target=client, args=('x',))
    threads.append(t)
    t.start()

for t in threads:
    t.join()