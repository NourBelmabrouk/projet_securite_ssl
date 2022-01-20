from Crypto import Random
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.Util.number import GCD
from Crypto.Hash import SHA



import rsa
import random
from math import pow
import pickle

def asym_menu():
    while True: 
        print("Choose an option: ")
        print("1-RSA")
        print("2-ElGamal")
        print("3-Back")
        choice=int(input())

        if choice==1: 
            rsa_function()
        elif choice==2:
            elgamal_function()
        elif choice==3: 
            break

def rsa_function():   
    while True: 
        print("Choose an option: ")
        print("1-Encrypt")
        print("2-Decrypt")
        print("3-Generate keys")
        print("4-Back")
        choice=int(input())

        if choice==1:
            key_path = input("Enter public key path: ")
            try:
                with open(key_path, 'rb') as f:
                    public_key = rsa.PublicKey.load_pkcs1(f.read())
            except:
                print("Key not found.")
            if(public_key):
                message=input("Enter your message: ")
                message=message.encode('utf8')
                encrypted_message=rsa.encrypt(message,public_key)
                print("The encrypted message is: ",encrypted_message)
                with open("encrypted_message.txt",'wb') as f:
                    f.write(encrypted_message)
            else:
                print("public key not found")
        elif choice==2:
            key_path = input("Enter private key path: ")
            try:
                with open(key_path, 'rb') as f:
                    private_key = rsa.PrivateKey.load_pkcs1(f.read())
            except:
                print("Key not found.")
            if(private_key):           
                with open("encrypted_message.txt",'rb') as f:
                    encrypted_message=f.read()
                message=rsa.decrypt(encrypted_message,private_key)
                print("The message is: ",message.decode('utf8'))
        elif choice==3:
            (pubkey, privkey) = rsa.newkeys(512)    
            with open('keys/pubkey.pem', 'wb') as f:
                f.write(pubkey.save_pkcs1('PEM'))

            with open('keys/privkey.pem', 'wb') as f:
                f.write(privkey.save_pkcs1('PEM'))
        elif choice==4:
            exit()

def elgamal_function():    
    while True: 
        print("Choose an option: ")
        print("1-Encrypt")
        print("2-Decrypt")
        print("3-Generate keys")
        print("4-Back")
        choice=int(input())

        if choice==1:
            message = input("Enter message to encrypt: ")
            filename = input("Enter public key path: ")
            with open(filename, 'rb') as f:
                pubKey, q, g = pickle.load(f)
            enc_message, u = encryption(message, q, pubKey, g)
            print("The encrypted message is: ",enc_message)
            with open("encrypted_message_gamal.txt", 'wb') as f:
                pickle.dump((enc_message, u, q), f)
        elif choice==2:
            filename = input("Enter private key path: ")
            with open(filename, 'rb') as f:
                privKey, q, g = pickle.load(f)
            with open("encrypted_message_gamal.txt", 'rb') as f:
                enc_message, u, o = pickle.load(f)
                dr_message = decryption(enc_message, u, privKey, o)
            print("The decrypted message is: " + ''.join(dr_message))
        elif choice==3:
            q = random.randint(pow(10, 20), pow(10, 50)) 
            g = random.randint(2, q) 
            privKey_path = input("Enter private key filename: ")
            privKey = gen_key(q)
            with open(privKey_path, 'wb') as f:
                pickle.dump((privKey, q, g),f)
            pubKey_path = input("Enter public key filename: ")
            pubKey = power(g, privKey, q)
            with open(pubKey_path, 'wb') as f:
                pickle.dump((pubKey, q, g),f)
        elif choice==4:
            break



def pgcd(a,b):
    if a<b:
        return pgcd(b,a)
    elif a%b==0:
        return b
    else:
        return pgcd(b,a%b)

def gen_key(q):
    key= random.randint(pow(10,20),q)
    while pgcd(q,key)!=1:
        key=random.randint(pow(10,20),q)
    return key

def power(a,b,c):
    x=1
    y=a
    while b>0:
        if b%2==0:
            x=(x*y)%c
        y=(y*y)%c
        b=int(b/2)
    return x%c

def encryption(msg,q,h,g):
    ct=[]
    k=gen_key(q)
    s=power(h,k,q)
    p=power(g,k,q)
    for i in range(0,len(msg)):
        ct.append(msg[i])
    for i in range(0,len(ct)):
        ct[i]=s*ord(ct[i])        
    return ct,p

def decryption(ct,p,key,q):
    pt=[]
    h=power(p,key,q)
    for i in range(0,len(ct)):
        pt.append(chr(int(ct[i]/h)))
    return pt