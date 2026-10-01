import asyncio

async def main():
    reader, writer = await asyncio.open_connection("127.0.0.1", 8000)

    try:
        while True:
            req = input(">>>")
            
            writer.write((req+"\n").encode("utf-8"))
            await writer.drain()

            line = await reader.readline()
            if not line:
                break
            response = line.decode("utf-8")

            print(response, end="")
    finally:
        writer.close()
        await writer.wait_closed()



if __name__ == "__main__":
    asyncio.run(main())