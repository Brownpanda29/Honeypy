import socket
import paramiko
import threading
import logging

# Set up logging
logging.basicConfig(filename='honeypot_logs.log', level=logging.INFO, format='%(asctime)s %(message)s')

# The banner to display upon connection
BANNER = "Welcome to Ubuntu 20.04 LTS (GNU/Linux 5.4.0-42-generic x86_64)\n"

# Simulated file system
FILE_SYSTEM = {
    "/": {"bin", "etc", "home", "usr"},
    "/home": {"user"},
    "/home/user": {"documents", "images"}
}

# Simulated commands
def ls(path="/"):
    return FILE_SYSTEM.get(path, {"No such file or directory"})

def pwd():
    return "/home/user"  # Simulated current directory

# Command handler
def handle_command(cmd):
    if cmd.startswith("ls"):
        path = cmd.split(" ")[-1] if len(cmd.split(" ")) > 1 else "/"
        return "\n".join(ls(path))
    elif cmd == "pwd":
        return pwd()
    else:
        return "bash: command not found"

# Client handler
def handle_client(client_socket):
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(paramiko.RSAKey.generate(bits=2048))
        server = paramiko.ServerInterface()
        transport.start_server(server=server)

        channel = transport.accept(20)
        if channel:
            channel.send(BANNER)
            while True:
                channel.send("$ ")
                command = ""
                while not command.endswith("\r"):
                    transport = channel.recv(1024)
                    channel.send(transport.decode("utf-8"), end='')
                    command += transport.decode("utf-8")
                channel.send("\n")
                command = command.strip()
                if command == "exit":
                    channel.send("logout\n")
                    channel.close()
                    break
                logging.info(f"Command: {command}")
                channel.send(handle_command(command) + "\n")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        client_socket.close()

# Server setup
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", 2222))  # Listen on port 2222
    server_socket.listen(100)

    print("[+] Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] New connection from {addr}")
        logging.info(f"New connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
