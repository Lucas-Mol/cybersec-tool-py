import socket
import ssl
import threading

clients = {}

def broadcast(msg, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(msg.encode())
            except:
                client_socket.close()
                del clients[client_socket]

def handle_client(client_socket, addr):
    print(f"[+] New connection from {addr}")

    client_socket.send("Enter your username: ".encode())
    username = client_socket.recv(1024).decode().strip()
    clients[client_socket] = username
    print(f"[+] {username} ({addr}) joined the chat.")
    broadcast(f"{username} has joined the chat!", client_socket)

    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print(f"[{username}] {msg}")
            broadcast(f"[{username}] {msg}", client_socket)
        except:
            break

    print(f"[-] {username} ({addr}) left the chat.")
    broadcast(f"{username} has left the chat.", client_socket)
    del clients[client_socket]
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(5)
    print("[*] Server is waiting for connections...")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="ssl/server.crt", keyfile="ssl/server.key")

    while True:
        client_socket, addr = server.accept()
        secure_socket = context.wrap_socket(client_socket, server_side=True)
        threading.Thread(target=handle_client, args=(secure_socket, addr)).start()

if __name__ == "__main__":
    start_server()
