import base64
from io import BytesIO
import nltk, re, json
from random_username.generate import generate_username
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')
nltk. download ('vader_lexicon')
wordLemmatizer = WordNetLemmatizer()
stopWords = set(stopwords.words('english'))
sentimentAnalyzer = SentimentIntensityAnalyzer()


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


# Convert part of speech from pos_tag() function
# into wordnet compatible pos tag
posToWordnetTag = {
    "J": wordnet.ADJ,
    "v": wordnet.VERB,
    "N": wordnet.NOUN,
    "R": wordnet.ADV
}

def treebankPosToWordnetPos(partOfSpeech):
    posFirstChar = partOfSpeech[0]
    if posFirstChar in posToWordnetTag:
        return posToWordnetTag[posFirstChar]
    return wordnet.NOUN


# Convert raw list of (word, POS) tuple to a list of strings 
# that only include valid english words
def cleansedWordList(posTaggedWordTuples):
    cleansedWords = []
    invalidWordPattern = "[^a-zA-Z-]"
    for posTaggedWordTuple in  posTaggedWordTuples:
        word = posTaggedWordTuple[0]
        pos = posTaggedWordTuple[1]
        cleansedWord = word.replace(".", "").lower()
        if (not re.search(invalidWordPattern, cleansedWord)) and len(word) > 1 and cleansedWord not in stopWords:
             cleansedWords.append(wordLemmatizer.lemmatize(cleansedWord, treebankPosToWordnetPos(pos)))
    return cleansedWords

def analyzeText(textToAnalyze):
    articleSentences = tokenizeSentences(textToAnalyze)
    articleWords = tokenizeWords(articleSentences)

    #Get Sentence Analytics
    stockSearchPattern = "/[0-9]|[%$€£¥]|thousand|million|billion|trillion|profit|loss"
    keySentences = extractKeySentences(articleSentences, stockSearchPattern)
    wordsPerSentence = getWordsPerSentence(articleSentences)

    # Get Word Analytics
    wordsPosTagged = nltk.pos_tag(articleWords)
    articleWordsCleansed = cleansedWordList(wordsPosTagged)

    # Generate word cloud
    separator = " "
    wordCloudFilePath = "results/wordcloud.png"
    wordcloud = WordCloud(width = 1000, height = 700, \
    background_color="salmon", colormap="Set3", collocations=False).generate(separator.join(articleWordsCleansed))
    # wordcloud.to_file(wordCloudFilePath)
    imgIo = BytesIO()
    wordcloud.to_image().save(imgIo, format='PNG')
    imgIo.seek(0)

    encodedWordCloud = base64.b64encode(imgIo.getvalue()).decode('utf-8')

    # Run Sentiment Analysis
    sentimentResult = sentimentAnalyzer.polarity_scores(textToAnalyze)

    # Collate analysis into one dictionary
    finalResult = {
        "data": {
            "keySentences": keySentences,
            "wordsPerSentence": round(wordsPerSentence, 1),
            "sentiment": sentimentResult,
            "wordCloudFilePath": wordCloudFilePath,
            "wordCloudImage": encodedWordCloud
        },
        "metadata": {
            "sentencesAnalyzed": len(articleSentences),
            "wordsAnalyzed": len(articleWordsCleansed),

        }
    }
    return finalResult

def runAsFile():
    # Get User Details
    welcomeUser()
    userName = getUsername()
    greetUser(userName)


    #Extract and Tokenize Text
    articleTextRaw = getArticleText()
    analyzeText(articleTextRaw)
