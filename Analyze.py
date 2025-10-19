from random_username.generate import generate_username

# Welcome User
def welcomeUser():
    print("\nWelcome to the analysis tool, i will mine and analyze a body of text from a file you give me!")

# Get Username
def getUsername():
    #Print message prompting user to input their name
    userNameFromInput = input("\nto begin, please enter your username:\n")

    if len(userNameFromInput) < 5 or not userNameFromInput.isidentifier():
        print("Your username must be atleast 5 characters long, alphanumeric only (a-z/A-Z/0-9), have no spaces, and cannot start with a number!")
        print("Assigning new username...")
        return generate_username()[0]
         


    return userNameFromInput

#Greet the user
def greetUser(name):
    print("Hello," + name)
    
welcomeUser()
userName = getUsername()
greetUser(userName)

