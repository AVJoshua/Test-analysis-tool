# Welcome User
def welcomeUser():
    print("\nWelcome to the analysis tool, i will mine and analyze a body of text from a file you give me!")

# Get Username
def getUsername():
    #Print message prompting user to input their name
    userNameFromInput = input("\nto begin, please enter your username:\n")
    return userNameFromInput

#Greet the user
def greetUser(name):
    print("Hello," + name)
    
welcomeUser()
userName = getUsername()
greetUser(userName)

