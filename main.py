import json
import copy
import random

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Å", "Ä", "Ö"]
letterStats = {"A" : [10, 1], "B": [2, 4], "C": [2, 8], "D": [6,1], "E": [8,1], "F":[2,4], "G":[3,2], "H":[2,3], "I":[5,1], "J":[1,7], "K":[3,3], "L":[7,1], "M":[3,3], "N":[7,1], "O":[5,2], "P":[2,4], "Q":[1,10], "R":[9,1], "S":[8,1], "T":[7,1], "U":[3,4], "V":[2,3], "Y":[2,8], "Å":[2,4], "Ä":[2,4], "Ö":[2,4]}
board = []
hand = []
points = []
letterBag = []
numberOfPlayers = 2
handSize = 7
currentPlayer = 0

with open("words.json", "r", encoding="utf-8") as file:
    words = set(json.load(file)["words"])

def initHand():
    singlePlayerHand = []
    for i in range(handSize):
        singlePlayerHand.append("#")
    for i in range (numberOfPlayers):
        hand.append(singlePlayerHand.copy())
initHand()

def initPoints():
    for i in range(numberOfPlayers):
        points.append(0)
initPoints()

def initBoard():
    for i in range(15):
        rows = []
        for j in range(15):
            multiplier = 1
            if j % 2 == (i % 2):
                multiplier = 2
            
            rows.append({
                "letter": "#",
                "occupied": False,
                "multiplier": multiplier
            })
        board.append(rows)

initBoard()

def displayBoard():
    boardString = "    A B C D E F G H I J K L M N O\n "
    for i, row in enumerate(board):
        if (i + 1 < 10):
            boardString += " "
        boardString += str(i + 1) + " "
        for k, cell in enumerate(row):
            if cell["occupied"]:
                boardString += cell["letter"] + " "
            else:
                boardString += "# "
                #boardString += (str(cell["multiplier"] > 1 and cell["multiplier"] or "#")) + " "

        boardString += "\n "
    print(boardString)

displayBoard()

def initLetterBag():
    global letterStats
    global letterBag
    for letter in letterStats:
        print(letter)
        for i in range(letterStats[letter][0]):
            letterBag.append([letter, letterStats[letter][1]])
    random.shuffle(letterBag)
    print(letterBag)
initLetterBag()

def displayHand():
    handString = ""
    for i in hand[currentPlayer]:
        if i == "#":
            handString += str(i) + ", "
            continue
        handString += (str(i) + "(" + str(letterStats[i][1]) + "), ") 
    print ("Dina bokstäver och deras poängvärden: " + handString)

def getNewLetter():
    letter = ""
    for i in letterBag:
        if i[0] != "#":
            letter = i[0]
            letterBag[letterBag.index(i)][0] = "#"
            return letter
    print("Slut på bokstäver")


def updateHand():
    for i in hand[currentPlayer]:
        if i == "#":
            hand[currentPlayer][hand[currentPlayer].index(i)] = getNewLetter()


def characterExistAt(x, y):
    if x < 0 or y < 0:
        return False

    if x > 14 or y > 14:
        return False
    
    if not board[y]:
        return False
    
    if not board[y][x]:
        return False
    
    return board[y][x]["occupied"]

def checkNeighboringWordsOnXaxis(x, y, currentLetter):
    # check letter found at (x-1, y) and continue check letters at (x-deltaX, y)
    # creates a string of all letters found on x axis
    xAxisChars = currentLetter
    deltaX = 1
    while True:
        tempX = x-deltaX
        if characterExistAt(tempX, y):
            print(f"found letter {board[y][tempX]["letter"]} at (x-{deltaX}, y)")

            xAxisChars = board[y][tempX]["letter"] + xAxisChars
            deltaX += 1
        else:
            break

    # check letter found at (x-1, y) and continue check letters at (x-deltaX, y)
    deltaX = 1
    while True:
        tempX = x+deltaX
        if characterExistAt(tempX, y):
            print(f"found letter at (x+{deltaX}, y)")

            xAxisChars = xAxisChars + board[y][tempX]["letter"]
            deltaX += 1
        else:
            break

    # check if letters are found on xAxis and a valid word
    if len(xAxisChars) > 1 and not checkWord(xAxisChars):
        print(f"tried to combo with inavlid word: {xAxisChars}")
        return True

    if len(xAxisChars) > 1 and checkWord(xAxisChars):
        print(f"found valid word: {xAxisChars}")

    return False

def checkNeighboringWordsOnYaxis(x, y, currentLetter):
    # check letter found at (x, y-1) and continue check letters at (x, y-deltaY)
    # creates a string of all letters found on y axis
    yAxisChars = currentLetter
    deltaY = 1
    while True:
        tempY = y-deltaY
        if characterExistAt(x, tempY):
            print(f"found letter {board[tempY][x]["letter"]} at (x, y-{deltaY})")

            yAxisChars = board[tempY][x]["letter"] + yAxisChars
            deltaY += 1
        else:
            break

    # check letter found at (x, y+1) and continue check letters at (x-deltaX, y)
    deltaY = 1
    while True:
        tempY = y+deltaY
        if characterExistAt(x, tempY):
            print(f"found letter at (x, y+{deltaY})")

            yAxisChars = yAxisChars + board[tempY][x]["letter"]
            deltaY += 1
        else:
            break

    # check if letters are found on yAxis and is a valid word
    if len(yAxisChars) > 1 and not checkWord(yAxisChars):
        print(f"tried to combo with invalid word: {yAxisChars}")
        return True

    if len(yAxisChars) > 1 and checkWord(yAxisChars):
        print(f"found valid word: {yAxisChars}")

    
    return False

def checkWord(word):
    return word.lower() in words

def increaseCoordinate(coordinate, direction, delta):

    x = alphabet.index(coordinate[0].upper())

    y = coordinate[1]
    if (len(coordinate) == 3):
        y = y + coordinate[2]
    y = int(y)-1 # convert to 0-index

    print("x, y: " + str(x), str(y))

    if direction == "V":
        x = x + delta
    elif direction == "L":
        y = y + delta
    return x, y

def reset(savedBoard, savedHand):
    global board
    global hand
    board = savedBoard
    hand[currentPlayer] = savedHand[currentPlayer]


#unfinished
#in the form: "hej", "C4", "V"
#does not check connected words 
#does not check proper placement (middle of board/next to other word)
#checks that the word exists, that the letters needed exist and places word
def placeWord(word, coordinate, direction):
    direction = direction.upper()
    if (not checkWord(word)):
        print("word not in word list")
        return False
    if (direction !="V" and direction != "L"):
        print("direction format wrong")
    positionDelta = 0
    wordPoints = 0
    savedHand = hand[currentPlayer].copy()
    savedBoard = copy.deepcopy(board)
    for currentLetter in word.upper():
        x, y = increaseCoordinate(coordinate, direction, positionDelta)
        #print("X, y: " + str(x), str(y))
        #print("letter: " + currentLetter)
        #print(board[y][x]["letter"])
        if x > 14 or y > 14:
            print("outside board size")
            reset(savedBoard, savedHand)
            return False
        if board[y][x]["letter"] != "#" and board[y][x]["letter"] != currentLetter:
            print("tring to overwrite letter")
            reset(savedBoard, savedHand)
            return False
        elif board[y][x]["letter"] == "#":
            if currentLetter not in hand[currentPlayer]:
                print("letter not in hand")
                reset(savedBoard, savedHand)
                return False
            hand[currentPlayer][hand[currentPlayer].index(currentLetter)] = "#"
            board[y][x]["letter"] = currentLetter
        else:
            if direction == "V":
                if checkNeighboringWordsOnYaxis(x, y, currentLetter):
                    print("neighboring word check failed")
                    reset(savedBoard, savedHand)
                    return False
            else:
                if checkNeighboringWordsOnXaxis(x, y, currentLetter):
                    print("neighboring word check failed")
                    reset(savedBoard, savedHand)
                    return False
        

        board[y][x]["letter"] = currentLetter
        board[y][x]["occupied"] = True
        wordPoints += letterStats[currentLetter][1]
        positionDelta+=1

    # checking the entire words, without counting the letter you just placed
    x, y = increaseCoordinate(coordinate, direction, 0)
    deltaX = 1
    deltaY = 1
    yAxisChars = word
    xAxisChars = word
    while True:
        if direction == "V":
            tempY = y-deltaY
            if characterExistAt(x, tempY):
                print(f"found letter {board[tempY][x]["letter"]} at (x, y-{deltaY})")
    
                yAxisChars = board[tempY][x]["letter"] + yAxisChars
                deltaY += 1
            else:
                break
        else:
            tempX = y-deltaX
            if characterExistAt(x, tempX):
                print(f"found letter {board[tempX][x]["letter"]} at (x, y-{deltaX})")
    
                xAxisChars = board[tempX][x]["letter"] + xAxisChars
                deltaX += 1
            else:
                break
    
    y = y + len(word)
    x = x + len(word)
    deltaX = 1
    deltaY = 1

    while True:
        if direction == "V":
            tempY = y+deltaY
            if characterExistAt(x, tempY):
                print(f"found letter {board[tempY][x]["letter"]} at (x, y-{deltaY})")
    
                yAxisChars = board[tempY][x]["letter"] + yAxisChars
                deltaY += 1
            else:
                break
        else:
            tempX = y+deltaX
            if characterExistAt(x, tempX):
                print(f"found letter {board[tempX][x]["letter"]} at (x, y-{deltaX})")
    
                xAxisChars = board[tempX][x]["letter"] + xAxisChars
                deltaX += 1
            else:
                break
    

    print("checks succeded, word: '" + word + "' written")
    return wordPoints

def exchangeLetters(letterString):
    for letter in letterString:
        if letter.upper() not in hand[currentPlayer]:
            return False
        hand[currentPlayer][hand[currentPlayer].index(letter.upper())] = "#"
    return True

def exchangeOrPlace():
    choice = input("Vill du byta bokstäver (b) eller placera ett ord (p)? ")
    choice = choice.upper()
    if choice == "B" or choice == "P":
        return choice

    print("Ogiltigt val, skriv bara 'p' eller 'b'")
    return False

            
def main():
    displayBoard()
    global points
    global currentPlayer
    print("Spelare " + str(currentPlayer + 1) + "s tur")
    pointsString = "Poäng: "
    for i in range(numberOfPlayers):
        pointsString += "Spelare " + str(i+1) + ": " + str(points[i]) + ", "
    print(pointsString)
    updateHand()
    displayHand()
    choice = exchangeOrPlace()
    if choice == False:
        return False
    if choice == "B":
        if not exchangeLetters(input("Vilka bokstäver vill du byta? ")):
            print("Du har inte alla bokstäver du skrev, och skriv endast bokstäver")
            return False
        currentPlayer = (currentPlayer + 1)%numberOfPlayers
        print("Lyckades byta ut bokstäver \n")
        return True
    
    word = input("Välj ord att placera: ")
    coordinate = input("Välj coordinat att placera på (ex: D3): ")
    direction = input("Välj riktning, vågrät (V) eller lodrät (L): ")
    newPoints = placeWord(word, coordinate, direction)
    if not newPoints:
        return False
    points[currentPlayer]+= newPoints
    currentPlayer = (currentPlayer + 1)%numberOfPlayers


while True:
    main()

# print("hand: " + str(hand))        
# placeWord("glass", "C5", "L")
# print("hand: " + str(hand))
# displayBoard()

placeWord("våg", "D3", "L")
displayBoard()
