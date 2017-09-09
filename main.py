from xml.etree import ElementTree
import requests
import pygame

pygame.init()
display = (800, 100)                            # Tuple of display size
gameDisplay = pygame.display.set_mode(display)  # Make window with dimensions specified
pygame.display.set_caption("RSS Client By: Frank Walsh")
clock = pygame.time.Clock()                     # Making the game clock
font = pygame.font.SysFont('calibri', 50)       # Font for printing onscreen

def main():
    # Boolean value to check and see if the window is still active
    crashed = False
    # Timer variable used to time refresh of content
    timer = 0
    # initialize arrays to hold xml text elements
    # Master array holds array of all arrays
    cbcNLNews = []
    cnnTopNews = []
    cnnMoney = []
    masterArray = [cbcNLNews, cnnTopNews, cnnMoney]

    # Urls to get RSS data from
    CNNTopurl = 'http://rss.cnn.com/rss/edition.rss'
    CBCurl = 'http://www.cbc.ca/cmlink/rss-canada-newfoundland'
    cnnMoneyURL = 'http://rss.cnn.com/rss/money_news_international.rss'

    # Calls function to fill the empty arrays with news headlines
    getNews(CBCurl, cbcNLNews)
    getNews(CNNTopurl, cnnTopNews)
    getNews(cnnMoneyURL, cnnMoney)

    # Initial coordinates of the text and speed
    x = 800
    speed = 2
    textCoords = [x, 20]

    #All news string holds all the headlines a master string
    allNewsString = makeBigString(masterArray)
    # Strings to render is an array that contains the massive string spliced into renderable length
    stringsToRender = splitBigString(allNewsString)
    #Active string controls what string is rendered at the moment
    activeString = 0

    # Loop that runs as long as the program is not crashed
    while not crashed:
        # Gets events that occur in the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If the window is closed, crashed is flagged as true and stopes the game loop
                crashed = True

        # Below is where the graphics are handled
        # Fills the background with black
        gameDisplay.fill((255, 255, 255))

        # Moves the text left
        x -= speed
        # Then updates the coordinates
        textCoords = [x, 20]
        textCoords2 = [x + 13821, 20]

        # Handles the geometry of the strings being rendered
        # 13821 is the lenght of a string 700 characters long
        if x < (-13821):
            # If it's 700 chars left then the active string is updated
            activeString += 1
            if activeString > len(stringsToRender):
                # If it's the last string in the array, it resets
                activeString = 0
            #Then x is reset and everything proceeds normally
            x += 13821

        printText(stringsToRender[activeString], textCoords)
        printText(stringsToRender[activeString+1], textCoords2)
        pygame.display.update()

        clock.tick(60)

        # Timer adds sixty milliseconds to it's clock
        timer += 60
        # Updates content if the timer is greater than the number of milliseconds in 6 hours
        if timer > 6*60*60*1000:
            updateContent()

    # Once everything is over the window is destroyed
    pygame.quit()
    quit()



# Function that actually prints the text
# bigString param is the the appended mass news string
# textCoords gives the placement of the coordinates on the screen
def printText(bigString, textCoords):
    text = font.render(bigString, True, [0,0,0])
    gameDisplay.blit(text, textCoords)
    'print(text.get_width())'

# Creates one long string containing all the news headlines seperated by '....'
# Param masterArray contains an the arrays of text from various news sources
def makeBigString(masterArray):
    # Initilize the string
    bigString = ' '

    # Loop through the number of subArrays in the masterArray
    for subArrays in masterArray:
        # Then loop through the strings contained in the sub arrays
        for strings in subArrays:
            bigString += strings
            bigString += ' // '
    return bigString



# The pygame lib only allows strings upto 2048 characters to be in a string
# This function splices the strings into chunkcs of 2047 to be rendered
def splitBigString(bigString):
    # Initilizes the array
    stringsThatCanRender = []

    # Using integer division, the number of strings to be made is determined
    totalNumOfChars = len(bigString)
    stringsToMake = totalNumOfChars//700 + 1

    # Loops through the number of strings to be made
    for i in range(stringsToMake):
        # The empty array is then appended with the big string split by intervals of 2047
       stringsThatCanRender.append(bigString[(i*700):((i+1)*700)])

    return stringsThatCanRender


# Used to refresh the arrays containing news
def updateContent():
    main()


# Function that goes to the website and retrives the RSS XML
# url is the url of the RSS feed
# arrayOfNews is any empty array, strings are appended to this
def getNews(url, arrayOfNews):

    # Gets the raw data from website
    response = requests.get(url)

    # Converts the raw data to string, then ElementTree is used to find the elements
    stringData = response.text
    tree = ElementTree.fromstring(stringData)

    # All RSS feeds follow the same path to get to headlines
    # There are three layers that must be penetrated, the path will always be: 'rss/channel/item'
    # Hence the three nested for loops below
    # First for loop opens the rss element
    for child in tree:
        # Second loop opens the channel element
        for doubleChild in child:
            # Inside channel element there ~10 elements describing the feed
            # If statment is used to filter them (Something more elegant could probably be done with ET)
            if doubleChild.tag == 'item':
                # Third for loop filters through the elements in each article for the headline
                for tripleChild in doubleChild:
                    if tripleChild.tag == 'title':
                        # Finally the headline is appended to it's array
                        arrayOfNews.append(tripleChild.text)

# Call the main function to begin the program
main()