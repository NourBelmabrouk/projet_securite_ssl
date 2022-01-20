import socket, threading
import os, datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes


class Server:
    def __init__(self, port):

        self.host = '127.0.0.1'
        self.port = port

    def start_server(self):
        
        self.generate_keys()
        secret_key = get_random_bytes(16)

        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.clients = []

        self.s.bind((self.host, self.port))
        self.s.listen(100)
    
        print("Running on host and waiting for clients")

        self.username_lookup = {}
        
        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print("New connection. Username: " + str(username))           
            self.broadcast("New person joined the room. Username: " + username)
            self.username_lookup[c] = username
            self.clients.append(c)
            client_pub_key = self.send_pub_key(c)
            encrypted_secret = self.encrypt_secret(client_pub_key, secret_key)
            self.send_secret(c, encrypted_secret) 
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self,msg):
        for connection in self.clients:
            print("Broadcast message: "+ msg)

    def generate_keys(self):
        try:
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            private_key_pem = private_key.exportKey().decode()
            public_key_pem = public_key.exportKey().decode()
            with open('server_keys/server_private_key.pem', 'w') as priv:
                priv.write(private_key_pem)
            with open('server_keys/server_public_key.pem', 'w') as pub:
                pub.write(public_key_pem)
            return public_key

        except Exception as e:
            print(e)
    
    def encrypt_secret(self, client_pub_key, secret_key):
        try:
            cpKey = RSA.importKey(client_pub_key)
            cipher = PKCS1_OAEP.new(cpKey)
            encrypted_secret = cipher.encrypt(secret_key)
            return encrypted_secret

        except Exception as e:
            print(e)
    
    def send_secret(self,c,secret_key):
        try:
            c.send(secret_key)
            print("Secret key had been sent to the client")
        
        except Exception as e:
            print(e)
   
    def send_pub_key(self, c):
        try:
            public_key = RSA.importKey(open('server_keys/server_public_key.pem', 'r').read())
            c.send(public_key.exportKey())
            client_pub_key = c.recv(1024)
            print("Client public key had been received")
            return client_pub_key

        except Exception as e:
            print(e)

    def handle_client(self,c,addr):
        
        while True:
            try:
                msg = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)
                self.broadcast(str(self.username_lookup[c])+' has left.')
                break

            if msg.decode() != '':
                print("Message exchanged")
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)
            else:
                print( self.username_lookup[c] +" left the server.")
                for conn in self.clients:
                    if conn == c:
                        self.clients.remove(c)
                break

def terminate(Server):
    while True:
        command = input('')
        if (command == 'exit'):
            for conn in Server.clients:
                conn.shutdown(socket.SHUT_RDWR)
            print("All connections had been terminated")
        break
    print("Server is shut down")
    os._exit(0)
       
def start():
    server = Server(2005)
    t_terminate = threading.Thread(target = terminate, args=(server,))
    t_terminate.start()
    server.start_server()