

from AsymmetricManager import asym_menu
from EncodingManager import encoding_menu
from SymmetricManager import sym_menu
from hashManager import hash_menu
from Chatroom import chatroom_menu
from CrackedMessage import cracked_message_menu


def menu():
    while True: 
        print("Choose an option: ")
        print("1-Encoding and Decoding")
        print("2-hash of a message")
        print("3-Cracking a hashed message")
        print("4-Symmetric encryption and decryption of a message")
        print("5-Asymmetric encryption and decryption of a message")
        print("6-Secure communication between two clients (ChatRoom)")
        print("7-Leave")
        choice=int(input())

        
        if choice==1: 
            encoding_menu()
        elif choice==2: 
            hash_menu()
        elif choice==3: 
            cracked_message_menu()
        elif choice==4: 
            sym_menu()
        elif choice==5: 
            asym_menu()
        elif choice==6: 
            chatroom_menu()
            break
        elif choice==7: 
            exit()
