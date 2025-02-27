import socket
import ssl
import threading

def receive_messages(client_socket, username):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print(f"\r{msg}\n[{username}] ", end="", flush=True)
        except:
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    context.check_hostname = False  
    context.verify_mode = ssl.CERT_NONE  
    server_ip = input("Enter the server IP: ")

    secure_client = context.wrap_socket(client, server_hostname=server_ip)
    secure_client.connect((server_ip, 5555))

    print(secure_client.recv(1024).decode(), end="")
    username = input()
    secure_client.send(username.encode())

    print("[*] Connected to the secure server. Type your messages below.")

    threading.Thread(target=receive_messages, args=(secure_client,username,), daemon=True).start()

    while True:
        msg = input(f"[{username}] ")
        if msg.lower() == "exit()":
            break
        secure_client.send(msg.encode())

    secure_client.close()
    print("[-] Connection closed.")

if __name__ == "__main__":
    start_client()
