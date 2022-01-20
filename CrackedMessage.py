
import hashlib


def cracked_message_menu():
    while True: 
        print("Choose an option: ")
        print("1-Md5")
        print("2-SHA1")
        print("3-SHA256")
        print("4-Back")
        choice=int(input())

        if choice==1: 
            message=input("Enter the message you want to hash and then crack: ")
            hashed_message=hashlib.md5(message.encode()).hexdigest()
            print("The hashed message is: ",hashed_message)
            with open('insat.dic', 'r') as f:
                for line in f: 
                    if(hashlib.md5(line.strip().encode()).hexdigest()==hashed_message):
                        print("We cracked the email")
                        print("The email is: ",line)
                        break
        elif choice==2:
            message=input("Enter the message you want to hash and then crack: ")
            hashed_message=hashlib.sha1(message.encode()).hexdigest()
            print("The hashed message is: ",hashed_message)
            with open('insat.dic', 'r') as f:
                for line in f: 
                    if(hashlib.sha1(line.strip().encode()).hexdigest()==hashed_message):
                        print("We cracked the email")
                        print("The email is: ",line)
                        break
        elif choice==3:
            message=input("Enter the message you want to hash and then crack: ")
            hashed_message=hashlib.sha256(message.encode()).hexdigest()
            print("The hashed message is: ",hashed_message)
            with open('insat.dic', 'r') as f:
                for line in f: 
                    if(hashlib.sha256(line.strip().encode()).hexdigest()==hashed_message):
                        print("We cracked the email")
                        print("The email is: ",line)
                        break
        elif choice==4: 
            break