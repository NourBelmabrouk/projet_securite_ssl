import os, datetime
import json, socket, threading

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode

class Client:
    def __init__(self, server, port, username):
        self.server = server
        self.port = port
        self.username = username

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.s.connect((self.server, self.port))
        except Exception as e:
            print( e)
        
        self.s.send(self.username.encode())
        print(" Connected successfully!")
        
        self.create_key_pairs()
        self.exchange_public_keys()
        global secret_key
        secret_key = self.handle_secret()
        

        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.input_handler,args=())
        input_handler.start()

    def handle_messages(self):
        while True:
            message = self.s.recv(1024).decode()
            if message:
                key = secret_key
                decrypt_message = json.loads(message)
                iv = b64decode(decrypt_message['iv'])
                cipherText = b64decode(decrypt_message['ciphertext'])
                cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                msg = cipher.decrypt(cipherText)
                current_time = datetime.datetime.now()
                print(msg.decode())
            else:
                print("Lost the connection to the server")
                print(" Closing down the connection")
                self.s.shutdown(socket.SHUT_RDWR)
                os._exit(0)

    def input_handler(self):
        while True:
            message = input()
            if message == "bye":
                break
            else:
                key = secret_key
                cipher = AES.new(key, AES.MODE_CFB)
                message_to_encrypt = self.username + ": " + message
                msgBytes = message_to_encrypt.encode()
                encrypted_message = cipher.encrypt(msgBytes)
                iv = b64encode(cipher.iv).decode('utf-8')
                message = b64encode(encrypted_message).decode('utf-8')
                result = json.dumps({'iv':iv, 'ciphertext':message})
                self.s.send(result.encode())
        
        self.s.shutdown(socket.SHUT_RDWR)
        os._exit(0)

    def handle_secret(self):
            secret_key = self.s.recv(1024)          
            private_key = RSA.importKey(open(f'server_keys/{self.username}_private_key.pem', 'r').read())
            cipher = PKCS1_OAEP.new(private_key) 
            return cipher.decrypt(secret_key)

    def exchange_public_keys(self):
        try:
            print(" Getting public key from the server")
            server_public_key = self.s.recv(1024).decode()
            server_public_key = RSA.importKey(server_public_key)    

            print("Sending public key to server")
            public_pem_key = RSA.importKey(open(f'server_keys/{self.username}_public_key.pem', 'r').read())
            self.s.send(public_pem_key.exportKey())
            print("Exchange completed!")

        except Exception as e:
            print("ERROR")

    def create_key_pairs(self):
        try:    
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            private_pem = private_key.exportKey().decode()
            public_pem = public_key.exportKey().decode()
            with open(f'server_keys/{self.username}_private_key.pem', 'w') as priv:
                priv.write(private_pem)
            with open(f'server_keys/{self.username}_public_key.pem', 'w') as pub:
                pub.write(public_pem)

        except Exception as e:
            print(" ERROR, you messed up something.... ")


def start_client():
    username = input("Enter Username: ")
    client = Client("127.0.0.1", 2005, username)
    client.create_connection()