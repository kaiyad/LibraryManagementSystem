#!/usr/bin/env python

# Number of times a user can attempt afte login failure
max_login_attempts:str = 3

# stores if the user is an admin or a student
is_admin:bool = False 

# stores the current user
current_user = None

# Max duration of time a book can be request to be borrowed for
max_duration = 25 

# Max number of copies a studnet can borrow at one time
max_copies = 3

class Student(object):
    '''This class deals with student data
    '''
    user_data = {1:{'Id': '1','UserName': 'john123',  'Password': 'Password@123' , 'Copies': 0}}
    def __init__(self, id = None,  user_name="", password="",copies=0):
        self.user_name = user_name
        self.password = password
        self.id = id
        self.copies = copies

    def __str__(self):
        return self.user_name

class Admin(object):
    '''This class deals with Admin data
    '''
    user_data = {1:{'Id': '1','Name': 'John Doe', 'UserName': 'admin',  'Password': 'Password#11'}}
    
    def __init__(self, id=None, username="", password=""):
        self.username = username
        self.password = password
        self.id = id

    def __str__(self):
        return self.username
