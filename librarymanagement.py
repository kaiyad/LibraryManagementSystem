#!/usr/bin/env python
import json
from os import system, name
import getpass
from datetime import datetime
from colorama import Fore
from time import sleep
import logging
logging.basicConfig(filename="lms.log", filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


import libraryconfig as config
from libraryconfig import Student, Admin


def clear(): 
    """ This function clears the console irrespective of the Operating System and returns an empty string """
    try:
            # for windows 
            if name == "nt": 
                _ = system("cls") 
            # for mac and linux(here, os.name is "posix") 
            else: 
                _ = system("clear") 
            return ""
    except Exception as inst:
        print("could not clear the console")
        logger.error("could not clear the console")
        logger.critical(inst)
        logger.critical(inst.args)
        logger.critical(type(inst))
        menu = Menu()
        menu.main_menu()

def close_application():
    """ This functon exits the Application """
    try:
        logger.info(f"Application closed by the user {config.current_user} ")
        exit( "Closing the Application")
    except Exception as inst:
        print("could not close the application")
        logger.error("could not close the application")
        logger.critical(inst)
        logger.critical(inst.args)
        logger.critical(type(inst))
        exit()

class Book(object):
    """
    This Class deals with the library operations of adding, updating, deleting, requesting, returning of the books
    """

    # Dictionary to store books
    book_data = {1: { "Id": "123", "Name":  "C programming", "Author": "Dennis Ritchie", "Price": 2450, "Version": 1, "Available":    True, "TakenBy": None, "IssuedDate":None, "Duration":None}, 
    2: { "Id": "132", "Name":  "Learn Python", "Author": "Mark Lutz", "Price": 3000, "Version": 5, "Available": True, "TakenBy":      None, "IssuedDate":None, "Duration":None} }

    def __init__(self, id:int=None, name:str=None, author:list = [], price:float=None, version:int=None, available:bool=True , takenby:str=None, issueddate:str=None, returneddate:str=None, duration:int=None):
        self.id = id
        self.name = name
        self.author = author
        self.price = price
        self.version = version
        self.available = available
        self.takenby = takenby
        self.issueddate = issueddate
        self.duration = duration
        if  id:
            self.book_data[len(self.book_data)+1] = { "Id": id, "Name":  name, "Author": author, "Price": price, "Version": version, "Available": available, "TakenBy": takenby, "Duration": duration, "IssuedDate": issueddate, "ReturnedDate": returneddate} 

    def is_available(self, book_id,):
        """ This  function checks whether book is assigned to some student 
        Arguments:
        book_id -- Id of the book
        Return:
        True --  If the book is not assigned already
        False -- If the book is assigned already or any exception occurs
        """
        try:
            for  book in self.book_data:
                if book_id == self.book_data[book]["Id"]:
                    return self.book_data[book]["Available"]
            else:
                return False
        except Exception as inst:
            print("could not check for the assigment of the book")
            logger.error("could not check for the assigment of the book")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            return False
        
    def in_library(self, book_id):
        """ This  function checks whether book is available in the library 
        Arguments:
        book_id -- Id of the book
        Return:
        True --  If the book is in library
        False -- If the book is not in library or any exception occurs
        """
        try:
            for  book in self.book_data:
                if book_id == self.book_data[book]["Id"]:
                    return True
            else:
                return False
        except Exception as inst:
            print("could not check for the avilability of the book")
            logger.error("could not check for the availability of the book")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            return False

    def list_books(self, **kwargs):
        """Returns List of Books"""
        return self.book_data


    def create_book(self, id, name, author, price, version ):
        """
        This function adds  a new book to the Book List of the Library
        Arguments:
        id: Id of the book
        name: Name of the book
        author: Author of the book
        price: Price of the book
        version: Release version of the book
        Return:
        True -> If successfully added a book
        False -> If failed to  add a book or any occurence of an exception
        """
        try:
            book_num = len(self.book_data)+1
            self.book_data[book_num] = { "Id": id, "Name":  name, "Author": author, "Price": price, "Version": version, "Available": self.  available, "TakenBy": self.takenby} 
            return self.in_library(id)
        except Exception as inst:
            print("could not add the book")
            logger.error("could not add the book")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            return False

    def delete_book(self, id):
        """
        This function removes a selected book from the books list of the library
        arguments:
        id -> Id of the book to be removed
        Return:
        True -> If book is removed from the book list
        False -> If book could not be removed from the list or any occurence of an Exception
        """
        try:
            for  book in self.book_data:
                if id == self.book_data[book]["Id"]:
                    del self.book_data[book]
                    break
            if not self.in_library(id):
                return True
            else:
                return False
        except Exception as inst:
            print("could not remove the book")
            logger.error("could not remove the book")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            return False
    
    def issue_book(self, id):
        """ 
        This function issues a book on request from the user
        checks:
        If user reached maimum limit of copies request
        If the max duration to have the book is 25 days
        arguments:
        id -> Id of the book
        return:
        True -> if book is issued
        False -> If books is not issued or any occurence of exception
        """
        try:
            for  book in self.book_data:
                if id == self.book_data[book]["Id"]:
                    if config.current_user["Copies"] >= config.max_copies:
                        print(Fore.YELLOW, "You have maximum allowed number of copies with you.\nPlease return before requesting", Fore.RESET)
                        return False
                    duration = int(input(f"Enter the duration in days (maximum {config.max_duration} days): "))
                    if duration > config.max_duration:
                        print(Fore.YELLOW,f"Duration Exceeded maximum limit of {config.max_duration} days", Fore.RESET)
                        return False
                 
                    self.book_data[book]["TakenBy"] = config.current_user["Id"] 
                    self.book_data[book]["IssuedDate"] = str(datetime.now())
                    self.book_data[book]["Available"] = False
                    self.book_data[book]["Duration"] = duration
                    config.current_user["Copies"] += 1
                    break

            if not self.is_available(id):
                return True
            else:
                return False
        except Exception as inst:
            print("could not issue the book")
            logger.error("could not issue the book")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            return False
    
    def collect_book(self, id):
        """
        This function collects the book when return by user
        arguments:
        id -> Id of the book
        return:
        True -> if book is collected
        False -> if book is not collected or any occurence of Exception
        """
        try:
            for  book in self.book_data:
                if id == self.book_data[book]["Id"]:
                    self.book_data[book]["TakenBy"] = None
                    self.book_data[book]["IssuedDate"] = None
                    self.book_data[book]["Available"] = True
                    self.book_data[book]["Duration"] = None
                    config.current_user["Copies"] -=1
                    break

            if self.is_available(id):
                return True
            else:
                return False
        except Exception as inst:
            print("could not collect the book")
            logger.error("could not collect the book")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            return False

    def update_book(self, id):
        """
        This function updates the book details
        arguments:
        id: Id of the book to be updated
        return:
        True: If the details of the book are updated
        False: If the details could not be updated or any occurences of Exception
        """
        try:
            for  book in self.book_data:
                if id == self.book_data[book]["Id"]:
                    print("What do you want to update: ")
                    print("1. Name")
                    print("2. Author")
                    print("3. Price")
                    print("4. Version")
                    print("0. Back Menu")

                    option = input("Enter your choice: ")
                    if option == "1":
                        self.book_data[book]["Name"] = input("Enter Name: ")

                    elif option == "2":
                        self.book_data[book]["Author"] = input("Enter Author: ")

                    elif option == "3":
                        self.book_data[book]["Price"] = int(input("Enter Price: "))

                    elif option == "4":
                        self.book_data[book]["Version"] = int(input("Enter Version: "))

                    elif  option == "0":
                        return  True

                    else:
                        print(Fore.YELLOW, "Invalid choice", Fore.RESET)
                        return self.update_book(id)

                    return self.update_book(id)
            else:
                return False
        except Exception as inst:
            print("could not update the book details")
            logger.error("could not update the book details")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            return False

class  Authorization(object):
    """
    Thi class deals with Authorization and Authentication of the user(student/Admin)
    """
    def __init__(self, username="", password=""):
        self.username = username
        self.password = password

    def is_authenticated(self, username, password,):
        """
        This function authenticates and authorizes access according to the use role
        arguments:
        username: username of the user
        pasword: Password of the user

        return:
        True -> if credentials are authenticated
        False -> if credentials could not be authnticated
        """
        try:
            handle = Admin() if config.is_admin else Student()
            data = handle.user_data
            for  key in  data:
                if  data[key]["UserName"] == username and data[key]["Password"] == password:
                    config.current_user =  data[key]
                    return True
            else:
                return False
        except Exception as inst:
            print("could not authenticate the user")
            logger.error("could not authenticate the user")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            return False

class Menu(object):
    """ This class deals with menu operations for all the Library Functionalities """

    def navigate_menu(self):
        """ This function deals with navigation options 
        Main Menu
        Close Application"""
        try:
            print("\n")
            print("1. Main Menu")
            print("0. Close Application")
            option = input("Enter your choice: ")
            if option == "1":
                self.main_menu()
            elif option == "0":
                close_application()
            else:
                print(Fore.YELLOW, "Invalid choice", Fore.RESET)
                self.navigate_menu()
        except Exception as inst:
            print("Faced some issue with navigation")
            logger.error("Faced some issue with navigation")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            self.main_menu()

    def login_menu(self):
        """ This function deals with the Login Menu Operations
        Login as a Student or Admin """
        try:
            attempts = 0
            print("L O G I N")
            print("-"*9)
            while attempts< config.max_login_attempts:
                print("1. Login as an Admin")
                print("2. Login as a Student")
                print("3. Close Application")
                print("\n")
                attempts += 1
                # Login option as an administratior or as a Student
                option = input("Enter your choice: ")
                if option == "1":
                    print("You have selected 1. Login as an Admin")
                    config.is_admin = True
                elif option == "2":
                    print("You have selected 2. Login as a Student")
                    config.is_admin= False
                elif option == "3":
                    print("You have selected 3. Close Application")
                    print(clear(),Fore.LIGHTCYAN_EX, "Good Bye......", Fore.RESET)
                    close_application()
                else:
                    print(clear(),Fore.YELLOW, "Enter a valid option", Fore.RESET)
                    continue
                # Calling authorization method for respective user role
                auth = Authorization()
                username = input("Enter your user name: ")
                password =  getpass.getpass(prompt="Enter your password: ")
                if auth.is_authenticated(username, password):
                    print(clear(), Fore.GREEN, "Login Successful", Fore.RESET)
                    logger.info(f"Login succesful for {username} with password {password}")
                    break
                else:
                    config.is_admin = False
                    print(clear(), Fore.YELLOW, "Login Failed", Fore.RESET)
                    logger.warning(f"Login failed for {username} with password {password} at attempt {attempts}")
            else:
                print(clear(), Fore.RED, "Attempts exhausted", Fore.RESET)
                logger.error("Application closed after exhausting login attempts ")
                close_application()
        except Exception as inst:
            print("Faced some issue with navigation")
            logger.error("Faced some issue with navigation")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            close_application()

    def main_menu(self):
        """ This Function deals wih main menu of Library Operations 
        for students and admin"""
        try:
            clear()
            print("L I B R A R Y\tM E N U")
            print("-"*24)
            if config.is_admin:
                print("1. Show Books")
                print("2. Add Books")
                print("3. Remove Books")
                print("4. Update Books")
                print("0. Close Applicaton")
            else:
                print("1. Show Books")
                print("2. Request Books")
                print("3. Return Books")
                print("0. Close Applicaton")

            print("\n")
            option = input("Enter your choice: ")
            if option == "1":
                self.showbook_menu()

            elif  option == "2":
                if config.is_admin:
                    self.addbook_menu()
                else:
                    self.requestbook_menu()

            elif option == "3":
                if config.is_admin:
                    self.removebook_menu()
                else:
                    self.returnbook_menu()

            elif option == "4" and config.is_admin:
                self.updatebook_menu()

            elif option == "0":
                close_application()

            else:
                print(Fore.YELLOW, "Invalid choice", Fore.RESET)
                self.main_menu()
        except Exception as inst:
            print("Faced some issue with Main menu")
            logger.error("Faced some issue with Main Menu")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            self.navigate_menu()

    def addbook_menu(self):
        """ This fucntion deals with calling the add method to add a book to the library """
        try:
            clear()
            print("A D D\tN E W\tB O O K")
            print("-"*25)
            handle = Book()
            book_id = input("Enter Book Id: ")
            if not handle.in_library(book_id):
                response = handle.create_book(book_id, input("Enter Book Name: "), input("Enter Book Author: "), input("Enter Book Price: "), input("Enter Book Version: "))
                if response:
                    print(Fore.GREEN, "successfully added the book" , Fore.RESET)
                    logger.info( f"created a book wiith Id  {book_id}")
                else:
                    logger.error(f"Failed to add the book with Id {book_id}")
                    print(Fore.RED, "could not add the book", Fore.RESET)
            else:
                print(Fore.YELLOW, f"book already exists with id {book_id}", Fore.RESET)
            self.navigate_menu()
        except Exception as inst:
            print("Failed to add book")
            logger.error("Failed to add book")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            self.navigate_menu()

    def removebook_menu(self):
        """ This function deals with calling the remove method  of a book """
        try:
            clear()
            print("R E M O V E\tB O O K")
            print("-"*21)
            handle = Book()
            book_id = input("Enter Book Id: ")
            if handle.in_library(book_id):
                response = handle.delete_book(book_id)
                if response:
                    print(Fore.GREEN, "successfully deleted the book" , Fore.RESET)
                    logger.info( f"deleted a book wiith Id  {book_id}")
                else:
                    logger.error(f"Failed to delete the book with Id {book_id}")
                    print(Fore.RED, "could not delete the book", Fore.RESET)
            else:
                print(Fore.YELLOW, f"book do not exist with id {book_id}", Fore.RESET)
            self.navigate_menu()
        except Exception as inst:
            print("Failed to remove book")
            logger.error("Failed to remove book")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            self.navigate_menu()

    def showbook_menu(self):
        """ This fucntion deals with viewing the books in the library books list """
        try:
            clear()
            print("S H O W\t B O O K S")
            print("-"*16)
            handle = Book()
            data  =  handle.book_data

            print("B O O K S")
            print("-"*9)
            for book in data:
                cur_book = data[book]
                print(str(json.dumps(cur_book, indent=4)))
                print("\n")
            self.navigate_menu()
        except Exception as inst:
            print("Failed to show books")
            logger.error("Failed to show books")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            self.navigate_menu()

    def updatebook_menu(self):
        """ This function deals with calling the update method of a book """
        try:
            clear()
            print("U P D A T E\tB O O K")
            print("-"*21)
            handle = Book()
            book_id = input("Enter Book Id: ")
            if handle.in_library(book_id):
                response = handle.update_book(book_id)
                if response:
                    print(Fore.GREEN, "successfully updated the book" , Fore.RESET)
                    logger.info( f"updated a book wiith Id  {book_id}")
                else:
                    logger.error(f"Failed to update the book with Id {book_id}")
                    print(Fore.RED, "could not update the book", Fore.RESET)
            else:
                print(Fore.YELLOW, f"book does not exist with id {book_id}", Fore.RESET)
            self.navigate_menu()
        except Exception as inst:
            print("Failed to return book")
            logger.error("Failed to return book")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            self.navigate_menu()

    def requestbook_menu(self):
        """
        This function requests book from the library book list
        """
        try:
            clear()
            print("R E Q U E S T\tB O O K")
            print("-"*24)
            handle = Book()
            book_id = input("Enter Book Id: ")
            if handle.is_available(book_id):
                response = handle.issue_book(book_id)
                if response:
                    print(Fore.GREEN, "successfully issued the book" , Fore.RESET)
                    logger.info( f"issued a book wiith Id  {book_id}")
                else:
                    logger.error(f"Failed to issue the book with Id {book_id}")
                    print(Fore.RED, "could not issue the book", Fore.RESET)
            else:
                print(Fore.YELLOW, f"book is currently no available  id {book_id}", Fore.RESET)
            self.navigate_menu()
        except Exception as inst:
            print("Failed to request book")
            logger.error("Failed to request book")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            self.navigate_menu()

    def returnbook_menu(self):
        """
        This fucntion returns the book to the book list
        """
        try:
            clear()
            print("R E T U R N\tB O O K")
            print("-"*15)
            handle = Book()
            book_id = input("Enter Book Id: ")
            if handle.in_library(book_id) and not handle.is_available(book_id):
                response = handle.collect_book(book_id)
                if response:
                    print(Fore.GREEN, "successfully returned the book" , Fore.RESET)
                    logger.info( f"returned a book wiith Id  {book_id}")
                else:
                    logger.error(f"Failed to return the book with Id {book_id}")
                    print(Fore.RED, "could not return the book", Fore.RESET)
            else:
                print(Fore.YELLOW, f"book is currently not available  id {book_id}", Fore.RESET)
            self.navigate_menu()
        except Exception as inst:
            print("Failed to return book")
            logger.error("Failed to return book")
            logger.critical(inst)
            logger.critical(inst.args)
            logger.critical(type(inst))
            self.navigate_menu()

if  __name__ == "__main__":
    print("\n\t\t***** Welcome To Library Management System *****\t\t\n")
    logger.info("Entered the Application")
    menu = Menu()
    #Login Functionality
    menu.login_menu()
    sleep(2)
    # Library Transactions Menu
    menu.main_menu()

