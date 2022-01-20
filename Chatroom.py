

from random import choice
from Server import start
from Client import start_client


def chatroom_menu():
    print("Choose an option")
    print("1-Be the server")
    print("2-Be the client")
    choice=int(input())
    
    if choice==1 : 
        start()
    elif choice==2:
        start_client()