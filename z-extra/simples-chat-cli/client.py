import socket
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
    server_ip = input("Enter the server IP: ")
    client.connect((server_ip, 5555))

    print(client.recv(1024).decode(), end="")
    username = input()
    client.send(username.encode())

    print("[*] Connected to the server. Type your messages below.")

    threading.Thread(target=receive_messages, args=(client,username,), daemon=True).start()

    while True:
        msg = input(f"[{username}] ")
        if msg.lower() == "exit()":
            break
        client.send(msg.encode())

    client.close()
    print("[-] Connection closed.")

if __name__ == "__main__":
    start_client()
