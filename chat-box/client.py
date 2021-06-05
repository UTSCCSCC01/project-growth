import socket
from threading import Thread

# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002  # server's port

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# prompt the client for a name
name = input("Enter your name: ")


def listen_for_messages():
    while True:
        recv_msg = s.recv(1024).decode()
        print("\n" + recv_msg)


# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    msg = input(f"{name} > ")

    # format the string
    msg = f"{name}:{msg}"

    # finally, send the message
    s.send(msg.encode())

# close the socket
s.close()
