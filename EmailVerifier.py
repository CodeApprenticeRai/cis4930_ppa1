import sys
sys.path.append(".")

import re, pymongo, time, pprint

class EmailVerifier:
    def command_line_routine(self, db=None):
        print("You've selected the function: Email Verifier")

        print("\n\nHistory:")

        if ( type(db) == type(None) ):
            db_client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = db_client["function_solution_records"]

        collection = db["records"]

        # TODO: Clean this up.
        print("Email", "IsValid", "Time", sep="\t")
        for record in collection.find({ "function_name": "EmailVerifier"}):
            print( record["parameters"]["email"], record["solution"], record["time"], sep="\t" )

        print( "*"*5, "End of History", "*"*5, "\n\n", sep="" )

        email_string = input("Enter an email string: ")

        print("The email string is{}valid.\n\n".format(" " if self.verify_email(email_string) else " not "))
        return None

    def verify_email(self, email, db):

        pattern = re.compile("[A-Za-z!$%*\+\-\=?^_{|}~]+[A-Za-z!$%*\+\-\=?^_{|}~.]*[A-Za-z!$%*\+\-\=?^_{|}~+]@[A-Za-z]*\.[A-Za-z]*")
        result  = True if pattern.fullmatch(email) else False
        current_unix_time = int( time.time() )

        if ( type(db) == type(None) ):
            db_client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = db_client["function_solution_records"]

        collection = db["records"]

        data = {
            "function_name": "EmailVerifier",
            "time": current_unix_time,
            "parameters": {
                "email": email
            },
            "solution": result
        }

        collection.insert_one(data)

        return result
