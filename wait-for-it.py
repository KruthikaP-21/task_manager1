import time
import socket
import sys


def wait_for_service(host, port, timeout=60):
    start_time = time.time()
    while True:
        try:
            sock = socket.create_connection((host, port), timeout=5)
            sock.close()
            print(f"{host}:{port} is available.")
            break
        except (socket.timeout, socket.error):
            if time.time() - start_time > timeout:
                print(f"Timeout while waiting for {host}:{port}")
                sys.exit(1)
            print(f"Waiting for {host}:{port}...")
            time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: wait-for-it.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    wait_for_service(host, port)
