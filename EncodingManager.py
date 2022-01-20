
import base64


def encoding_menu():
    while True: 
        print("Choose an option: ")
        print("1-Encoding")
        print("2-Decoding")
        print("3-Back")
        choice=int(input())

        if choice==1: 
            message=input("Enter the message you want to encode: ")
            encode(message)
        elif choice==2:
            encoded_message=input("Enter the encoded  message you want to decode: ")
            decode(encoded_message)
        elif choice==3: 
            break


def encode(message):
    print("The encoded message is:",str(base64.b64encode(message.encode('utf-8'))))

def decode(encoded_message):
    print("The message is: ",base64.b64decode(encoded_message.encode('utf-8')).decode('utf-8'))
