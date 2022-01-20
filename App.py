import re
import sqlite3
import hashlib
from getpass import getpass
import re
from MenuManager import menu


class App: 
    def __init__(self):
        self.connection=sqlite3.connect("project.db")
        self.cursor=self.connection.cursor()

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def sign_in(self):
        email=""
        while not(re.fullmatch(self.regex, email)):
            email=input("Enter your email: ")
        password=getpass("Enter your password: ")
        user=self.cursor.execute('''SELECT * FROM user
            where email=? and pwd=?
            ''',(email,hashlib.sha256(password.encode()).hexdigest())).fetchall()
        if len(user)<1 : 
            print("Sign in failed! try again or sign up if you don't have an account")
            self.launch()
        else: 
            print("Welcome ", user[0][0],user[0][1])
            menu()

    def sign_up(self): 
        email=""
        print("Please enter your information.")
        first_name=input("Enter your first name: ")
        last_name=input("Enter your last name: ")
        while not(re.fullmatch(self.regex, email)):
            email=input("Enter your email: ")
        password=input("Enter your password: ")
        hashed_password=hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("INSERT INTO user VALUES (?,?,?,?)",(first_name,last_name,email,hashed_password))
        self.connection.commit()

        

    def launch(self):
        while True:  
            print("Choose an option : ")
            print("1-Sign in")
            print("2-Sign up")
            choice=int(input())

            if choice==1: 
                self.sign_in()
                break
            elif choice==2: 
                self.sign_up()

        

if __name__ == '__main__':
    App().launch()
        
