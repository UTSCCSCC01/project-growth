import socket
from threading import Thread

# server's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # port we want to use

# initialize list/set of all connected client's sockets
client_sockets = set()

# create a TCP socket
s = socket.socket()

# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))

# listen for upcoming connections
s.listen(100)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(client, contact_info):
    """
    This function keeps listening for a message from "client" socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            flag = 0
            # keep listening for a message from "client" socket
            msg = client.recv(1024).decode()

            client_info = msg.split(':')
            contact_info[client] = client_info[0] # making a dictionary where key: client_socket,
            # value: client_name

            if client_info[1][0] == '@':
                target_name = client_info[1].split(' ')[0][1:] # getting the name of the referenced
                # client
                print("this is the target " + target_name)
                for client_socket in client_sockets:
                    if contact_info[client_socket] == target_name:
                        client_socket.send(msg.encode)
                        flag = 1
                        break
                    elif target_name == "everyone":
                        client_socket.send(msg.encode)
            else:
                # iterate over all connected sockets
                for client_socket in client_sockets:
                    # and send the message
                    client_socket.send(msg.encode())
                    flag = 1

            if flag != 1:
                print("User not found!")


        except Exception as e:
            # if client is no longer connected, remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(client)


while True:

    contact_info = {}

    # we keep listening for new connections all the time

    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")

    # add the new connected client to connected sockets
    client_sockets.add(client_socket)

    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket, contact_info))

    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True

    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()