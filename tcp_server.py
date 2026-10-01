import asyncio
import sys
import shlex
import time


store = {}

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        while True:
            line = await reader.readline()
            if not line:
                break

            try:
                request = shlex.split(line.decode("utf-8"))
                response = (command_parser(request) + "\n").encode("utf-8")
            except (ValueError, UnicodeDecodeError):
                response = b"[ERROR] Invalid command.\n"
            

            writer.write(response)
            await writer.drain()
    finally:
        print(f"Disconnected: {addr}")
        writer.close()
        await writer.wait_closed()



def command_parser(request):
    if len(request) == 0:
        return "[ERROR] Empty request."

    match(request[0]):
        case "PING":
            return ping_handler()
        case "GET":
            if len(request) != 2:
                return "[ERROR] GET need a key."
            key = request[1]
            return get_handler(key)
        case "SET":
            if len(request) != 3:
                return "[ERROR] Invalid SET command."
            key = request[1]
            value = request[2]
            return set_handler(key, value)
        case "DEL":
            if len(request) != 2:
                return "[ERROR] DEL need a key."
            key = request[1]
            return del_handler(key)
        case "INCR":
            if len(request) != 2:
                return "[ERROR] INCR need a key."
            key = request[1]
            return incr_handler(key)
        case _:
            raise ValueError

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
        return f"Key [{key}] does not exist."
    try:
        store[key] = str(int(store[key]) + 1) 
    except ValueError:
        return f"Key [{key}] is not an integer."       
    return "OK"

async def main():
    try:
        server = await asyncio.start_server(handle_client, "127.0.0.1", 8000)
        addr = server.sockets[0].getsockname()
        print(f"Serving on {addr}")
    except OSError as e:
        print(f"[ERROR] Failed to start server: {e}")
        return

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())