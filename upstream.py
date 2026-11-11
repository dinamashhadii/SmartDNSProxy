import socket
HOST = "127.0.0.1"
PORT = 5354
request_count = 0
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((HOST, PORT))
    print("Upstream server is running.")
    while True:
        data, client_address = server.recvfrom(1024)
        message = data.decode("utf-8").strip()
        parts = message.split()
        request_count += 1
        if len(parts) == 2 and parts[0] == "QUERY":
            domain = parts[1]
            if domain == "missing.example.net":
                response = "NOT_FOUND"
            else:
                response = "OK 198.51.100.7 5"
            print(f"Request #{request_count}: {domain} -> {response}")
        else:
            response = "ERROR"
        server.sendto(response.encode("utf-8"), client_address)