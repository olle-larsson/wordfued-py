import json
import copy

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Å", "Ä", "Ö"]
board = []
hand = ["G", "L", "A", "S", "S", "V", "E", "J", "Å", "G"]
points = 0

with open("words.json", "r", encoding="utf-8") as file:
    words = set(json.load(file)["words"])

def initBoard():
    for i in range(15):
        rows = []
        for j in range(15):
            rows.append({
                "letter": "#",
                "occupied": False
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

        boardString += "\n "
    print(boardString)

displayBoard()

def characterExistAt(x, y):
    return board[y] and board[y][x] and board[y][x]["occupied"]

def checkNeighboringWords(x, y, currentLetter):
    # check letter found at (x-1, y) and continue check letters at (x-deltaX, y)
    # creates a string of all letters found on x axis
    xAxisChars = currentLetter
    if characterExistAt(x-1, y):
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
    if characterExistAt(x+1, y):
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
    
    return False

def checkWord(word):
    return word in words

def increaseCoordinate(coordinate, direction, delta):

    x = alphabet.index(coordinate[0].upper())

    y = coordinate[1]
    if (len(coordinate) == 3):
        y = y + coordinate[2]
    y = int(y)-1 # convert to 0-index

    if direction == "V":
        x = x + delta
    elif direction == "L":
        y = y + delta
    return x, y

def reset(savedBoard, savedHand):
    global board
    global hand
    board = savedBoard
    hand = savedHand

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
    savedHand = hand.copy()
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
            if currentLetter not in hand:
                print("letter not in hand")
                reset(savedBoard, savedHand)
                return False
            hand[hand.index(currentLetter)] = "#"
            board[y][x]["letter"] = currentLetter

        if checkNeighboringWords(x, y, currentLetter):
            print("neighboring word check failed")
            reset(savedBoard, savedHand)
            return False

        board[y][x]["letter"] = currentLetter
        board[y][x]["occupied"] = True
        wordPoints += 1
        positionDelta+=1

    print("checks succeded, word: '" + word + "' written")
    return wordPoints
        

def main():
    displayBoard()
    global points
    print("Poäng: " + str(points))
    print ("hand: " + str(hand))
    word = input("Välj ord att placera: ")
    coordinate = input("Välj coordinat att placera på (ex: D3): ")
    direction = input("Välj riktning, vågrät (V) eller lodrät (L): ")
    newPoints = placeWord(word, coordinate, direction)
    if not newPoints:
        return False
    points+= newPoints


while True:
    main()

# print("hand: " + str(hand))        
# placeWord("glass", "C5", "L")
# print("hand: " + str(hand))
# displayBoard()

# placeWord("våg", "D3", "L")
# displayBoard()