from cgi import print_directory
import hashlib
def hash_menu():
    while True: 
        print("Choose an option: ")
        print("1-Md5")
        print("2-SHA1")
        print("3-SHA256")
        print("4-Back")
        choice=int(input())

        if choice==1: 
            message=input("Enter the message you want to hash: ")
            print("The hashed message: ", hashlib.md5(message.encode()).hexdigest())
        elif choice==2:
            message=input("Enter the message you want to hash: ")
            print("The hashed message: ", hashlib.sha1(message.encode()).hexdigest())
        elif choice==3:
            message=input("Enter the message you want to hash: ")
            print("The hashed message: ", hashlib.sha256(message.encode()).hexdigest())
        elif choice==4: 
            break