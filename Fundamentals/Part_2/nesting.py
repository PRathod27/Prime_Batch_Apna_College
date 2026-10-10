username = input("Enter username: ")
password = input("Enter password: ")

if ( username == "PREM" and password == "PREM"):
    print("Login Success")
else:
    if(username != "PREM"):
        print("Username invalid")
    else:
        print("Password invalid")