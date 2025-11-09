from random_username.generate import generate_username

# Welcome User
def welcomeUser():
    print("\nWelcome to the analysis tool, i will mine and analyze a body of text from a file you give me!")

# Get Username
def getUsername():
    maxAttempt = 3
    attempt = 0
    while attempt < maxAttempt:
        #Print message prompting user to input their name
        inputPrompt =  ""
        if attempt == 0:
            inputPrompt = "\nto begin, please enter your username:\n"
        else:
            inputPrompt = "\nPlease try again:\n"
        userNameFromInput = input(inputPrompt)
        #validate username
        if len(userNameFromInput) < 5  or not userNameFromInput.isidentifier():
            print("\nYour username must be atleast 5 characters long, alphanumeric only (a-z/A-Z/0-9), have no spaces, and cannot start with a number!")
        else:
            return userNameFromInput
        attempt +=1
    print("\n Exhausted all " + str(maxAttempt) + " attempts, Assigning new username instead...\n")
    return generate_username()[0]
                


    

#Greet the user
def greetUser(name):
    print("Hello," + name)
    
welcomeUser()
userName = getUsername()
greetUser(userName)

