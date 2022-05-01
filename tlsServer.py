# from email import message
# from http import client
import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl
import threading
import sys
# import urllib

# urllib.request.http.client

listen_addr = '127.0.0.1'
listen_port = 44567
server_cert = 'server.crt'
client_cert = 'client.crt'
server_key = 'server.key'

# context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# context.options &= ~ssl.OP_NO_SSLv3
# context.verify_mode = ssl.CERT_REQUIRED
# context.load_cert_chain(certfile=server_cert, keyfile=server_key)
# context.load_verify_locations(cafile=client_cert)

bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
bindsocket.bind((listen_addr, listen_port))
bindsocket.listen()

clientlist = []


def deal_with_client(connstream):
    data = connstream.recv(1024)

    while data:
        print(data)
        data = connstream.recv(1024)


def broadcast(message):
    for tup in clientlist:
        tup[0].send(message)


def endClientConnection(client):
    nickname = ' '
    for tup in clientlist:
        if tup[0] == client:
            nickname = tup[1]
            clientlist.remove(tup)
            print(nickname + " disconnected")

    broadcast(f'{nickname} left the chat!'.encode('ascii'))

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
            print(message.decode('asscii'))
            if message.decode('ascii').split(":")[1] == " .exit":
                endClientConnection(client)
        except:
                e = sys.exc_info()[0]
                print(e)

def receive():
    while True:
        print("Waiting for client")
        newsocket, fromaddr = bindsocket.accept()
        print(f"connected with {str(fromaddr)}")
        # print("Client connected: {}:{}".format(fromaddr[0], fromaddr[1]))

        newsocket.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        clientlist.append((newsocket, nickname))

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send("connected to the server!".encode('ascii'))
        msg = ""
        for tup in clientlist:
            msg = msg + " ," + tup[1]
        msg = msg + " are connected to the chat!"
        client.send(msg.encode('ascii'))
        threading = threading.Thread(target=handle, args=(client,))
        threading.start()

'''
        conn = context.wrap_socket(newsocket, server_side=True)
        print("SSL established. Peer: {}".format(conn.getpeercert()))
        buf = b''  #Buffer to hold received client data
        try:
            while True:
                data = conn.recv(1024)
                if data:
                # Client sent us data. Append to buffer
                    buf += data
                else:
                    # No more data from client. Show buffer and close connection.
                    print("Received:", buf)
                    break
        finally:
            print("Closing connection")
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
'''
        # threading = threading.Thread(target=handle, args=(client,))
        # threading.start()

receive()