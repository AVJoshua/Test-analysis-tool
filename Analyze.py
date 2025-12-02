from random_username.generate import generate_username
from nltk.tokenize import sent_tokenize, word_tokenize
import re


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
    print("Hello, " + name)
    
# Get Text from file
def getArticleText():
    f = open("./files/article.txt")
    rawText = f.read()
    f.close()
    return rawText.replace("\n", " ")

# Extract sentences from Raw Text Body
def tokenizeSentences(rawText):
    return sent_tokenize(rawText)

# Extract Words from list of Sentences 
def tokenizeWords(sentences):
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence))      
    return words

# Get the key sentences based on search pattern of key word
def extractKeySentences(sentences, searchPattern):
    matchedSentences = []
    for sentence in sentences:
        #If sentences matches desired pattern, add to matchedSentences
        if re.search(searchPattern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences
# Get the average words per sentence excluding punctuation
def getWordsPerSentence(sentences):
    totalwords = 0
    for sentence in sentences:
        totalwords += len(sentence.split(" "))
        
    return totalwords / len(sentences)

# Get User Details
welcomeUser()
userName = getUsername()
greetUser(userName)


#Extract and Tokenize Text
articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWords = tokenizeWords(articleSentences)

#Get Analytics
stockSearchPattern = "/[0-9]|[%$€£¥]|thousand|million|billion|trillion|profit|loss/g"
keySentences = extractKeySentences(articleSentences, stockSearchPattern)
wordsPerSentence = getWordsPerSentence(articleSentences)

# Print for testing
print("GOT:")
print(wordsPerSentence)