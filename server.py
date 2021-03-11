'''https://www.youtube.com/watch?v=3QiPPX-KeSc'''

import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
# automatically gets the server IP addr equi to SERVER = "192.168.20.7"
# print("Server ip address is: ", SERVER)
# print("Server name is: ", socket.gethostname())
# To connect from outside your network >> SERVER = "public ip address"
HEADER = 64 
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSSAGE = "DISCONNECT!"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IPV4, TCP)
server.bind(ADDR)

def handle_client(conn, addr):
    # this will run concurrently for each client
    print(f"[NEW CONNECTION] {addr} connected!")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # blocking code
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSSAGE:
                connected = False
            
            print(f"[{addr}] {msg}")
            conn.send("Message received".encode(FORMAT))

    conn.close()

def start():
    #start listening for connection
    print(f"[LISTENING] Server is listening on {SERVER}")
    server.listen()
    while True:
        conn, addr = server.accept() # blocking code
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        # amount of clients connected, subtract 1 
        # which represents the start thread

print("[STARTING] server is starting...")
start()