from email import message

# import imp
import socket
import ssl
import threading
import random
import string

nickname = (''.join(random.choice(string.ascii_letters) for i in range(10))) + str(random.randint(0, 10000))

# host_addr = '127.0.0.1'
# host_port = 8082
server_sni_hostname = 'example.com'
server_cert = 'server.crt'
client_cert = 'client.crt'
client_key = 'client.key'

# nickname = (''.join(random.choice(string.ascii_letters) for i in range(10))) + str(random.randint(0, 10000))

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)


# def receive():
#     while True:
#         try:
#             message = client.re
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
# conn.connect(('127.0.0.1', 8082))
#  print("SSL established. Peer: {}".format(conn.getpeercert()))

def receive():
    while True:
        try:
            message = conn.recv(1024).decode('ascii')
            # if message == '.exit':
            #     client.close()
            if message == 'NICK':
                conn.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('An error occurred!')
            conn.close()
            break

def write():
    while True:
        print("SSL established. Peer: {}".format(conn.getpeercert()))
        message = f'{nickname}: {input("")})'
        conn.send(message.encode('ascii'))
# print("Sending: 'Hello, world!'")
# conn.send(b"Hello, world!")
# print("closing connection")
# conn.close()

receive_threaing = threading.Thread(target=receive)
receive_threaing.start()

write_threading = threading.Thread(target=write)
write_threading.start()