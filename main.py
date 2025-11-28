import json #using json file
import random #for unique id's
import string #for string operations
from pathlib import Path #for accesing the json file
from datetime import datetime #for managing date and time

class Library:

    database = "library.json"
    data = {"books": [] , "members": []} 

    #load existing data to json
    if Path(database).exists():
        with open(database,"r") as fs:
            content = fs.read().strip()
            if content: #someting exists as the content
                data = json.loads(content) #load json file to temporay location data
    else:
        with open(database,"w") as fs:
            json.dump(data,fs,indent = 4) #if json file does not exists than create one and dump the content of temporary storage inside it 


    @classmethod #only accessable inside the class
    def save_data(cls): #saving the content of data to library.json 

        with open(cls.database,'w') as  fs : 
            json.dump(cls.data,fs,indent = 4,default = str) #dumping the data of temporary data inside json file

    @staticmethod
    def gen_id(Prefix = "B"):

        random_id = ""
        for i in range(5):
            random_id += random.choice(string.ascii_uppercase + string.digits)#choices returns list

        return Prefix + "-" + random_id 

    def add_book(self):

        title = input("Enter the book title : ")
        author = input("Enter the name of book author : ")
        copies = int(input("how many copies you want to store : "))

        book = {
            "id" : Library.gen_id(),
            "title" : title,
            "author" : author,
            "total_copies" : copies,
            "available_copies" : copies,
            "added_on" : (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        }

        Library.data["books"].append(book)
        Library.save_data()

    def list_books(self):

        if not Library.data["books"] : 
            print("sorry no books found")
            return
        
        for b in Library.data["books"]:
            print(f"{b["id"]:12} {b["title"][:24]:25} {b["author"][:19]:20} {b["total_copies"]}/{b["available_copies"]:>3}")
        print()   
        
    def add_member(self): 

        name = input("enter your name : ")
        email = input("enter your email : ")   

        member = {
            "id" : Library.gen_id("M"),
            "name" : name,
            "email" : email,
            "borrowed" : []

        }
        Library.data["members"].append(member)
        Library.save_data()
        print("member added succesfully")

    def list_members(self):  

        if not Library.data["members"]:
            print("there are no members") 
        else :
            for m in Library.data["members"]:
                print(f"{m["id"]:12} {m["name"][:24]:25} {m["email"][:29]:30}")
                print("this person has currently")
                print(f"{m["borrowed"]}")

    def borrow(self):

        member_id = input("enter the member ID : ").strip()  
        members = [m for m in Library.data["members"] if m["id"] == member_id]
        if not members :
            print("no such ID exists")
            return
        member = members[0] #taking the 0th index dictionary if two dictionary have same id's 

        book_id = input("enter the book ID : ")
        books = [b for b in Library.data["books"] if b["id"] == book_id]

        if not books :
            print("sorry no such ID of book exists")
            return
        book = books[0]

        if book["available_copies"] <= 0:
            print("Sorry no copy of this book is available")
            return
        
        borrow_entry = {
            "book_id" : book["id"],
            "title" : book["title"],
            "borrow_on" : (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }

        member["borrowed"].append(borrow_entry)
        book["available_copies"] -= 1
        Library.save_data()

    def return_book(self):
        member_id = input("enter the member ID : ").strip()  
        members = [m for m in Library.data["members"] if m["id"] == member_id]
        if not members :
            print("no such ID exists")
            return
        
        member = members[0]
        if not member["borrowed"] :
            print("no borrowed books")
            return
        
        print("borrowed books")
        for i,b in enumerate(member["borrowed"],start = 1):
            print(f"{i}. {b["title"]} ({b["book_id"]})")

        try :
            choice = int(input("enter book number to return  : ")) 
            selected =    member["borrowed"].pop(choice-1)
        except Exception as err:
            print("invalid value")

        books = [bk for bk in Library.data["books"] if bk["id"] == selected["book_id"]]   
        if books:
            books[0]["available_copies"] += 1    

        Library.save_data()    



hello = Library()

while True : 

    print("="*50)
    print("Library Management System")
    print("1. Add Book")
    print("2. List Books")
    print("3. Add Members")
    print("4. List Members")
    print("5. Borrow Books")
    print("6. Return Book")
    print("0. Exit the Portal")
    print("-"*50)

    choice = int(input("What operation do you want to perform : "))

    if choice == 1:
        hello.add_book()
    elif choice == 2:
        hello.list_books()
    elif choice == 3:
        hello.add_member()
    elif choice == 4:
        hello.list_members()   
    elif choice == 5:
        hello.borrow()     
    elif choice == 6:
        hello.return_book()
    elif choice == 0 :
            exit(0)
