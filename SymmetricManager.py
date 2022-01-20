import base64
import hashlib
from Crypto.Cipher import DES
from Crypto.Cipher import AES
from Crypto import Random

def sym_menu():
    while True: 
        print("Choose an option: ")
        print("1-DES")
        print("2-AES256")
        print("3-Back")
        choice=int(input())

        
        if choice==1: 
            des()
        elif choice==2:
            aes()
        elif choice==3: 
            break

    
def des():
    while True: 
        print("Choose an option: ")
        print("1-Encrypt")
        print("2-Decrypt")
        print("3-Back")
        choice=int(input())

        
        if choice==1: 
            key=input("Enter key: ")
            message=input("Enter the message you want to encrypt: ")
            message=bytes(message.encode())
            crypter =DES.new(bytes(key.encode()), DES.MODE_ECB)
            while (len(message) % 8 != 0):
                message += b'\x00'
            encrypted_message=crypter.encrypt(message)
            print("The encrypted message is: ",str(encrypted_message))
            with open("encrypted_message.txt",'wb') as f:
                f.write(encrypted_message)
        elif choice==2:
            key=input("Enter key: ")
            with open("encrypted_message.txt",'rb') as f:
                encrypted_message=f.read()
            crypter =DES.new(bytes(key.encode()), DES.MODE_ECB)
            message=crypter.decrypt(encrypted_message)
            print("The message is: ",message)
        elif choice==3:
            break


bs = AES.block_size

def aes():
    while True: 
        print("Choose an option: ")
        print("1-Encrypt")
        print("2-Decrypt")
        print("3-Back")
        choice=int(input())

        
        if choice==1: 
            key=input("Enter key: ")
            message=input("Enter the message you want to encrypt: ")
            key = hashlib.sha256(key.encode()).digest()
            raw = _pad(message)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            encrypted_message=base64.b64encode(iv + cipher.encrypt(raw.encode()))
            print("The encrypted message is: ",encrypted_message.decode())

        elif choice==2:
            key=input("Enter key: ")
            encrypted_message=input("Enter the encrypted message you want to encrypt: ")
            key = hashlib.sha256(key.encode()).digest()
            encrypted_message = base64.b64decode(encrypted_message)
            iv = encrypted_message[:AES.block_size]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            print("The message is: ", _unpad(cipher.decrypt(encrypted_message[AES.block_size:])).decode('utf-8'))
        elif choice==3:
            break

def _pad( s):
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]
