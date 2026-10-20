import json
import copy

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Å", "Ä", "Ö"]
board = []
hand = ["G", "L", "A", "S", "S"]

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
        boardString += str(i + 1) + " "
        if (i + 1 < 10):
            boardString += " "
        for k, cell in enumerate(row):
            if cell["occupied"]:
                boardString += cell["letter"] + " "
            else:
                boardString += "# "

        boardString += "\n "
    print(boardString)

displayBoard()

with open("words.json", "r", encoding="utf-8") as file:
    words = set(json.load(file)["words"])


def checkWord(word):
    return word in words

def increaseCoordinate(coordinate, direction, delta):

    x = alphabet.index(coordinate[0])

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
    for i in word.upper():
        x, y = increaseCoordinate(coordinate, direction, positionDelta)
        #print("X, y: " + str(x), str(y))
        #print("letter: " + i)
        #print(board[y][x]["letter"])
        if x > 14 or y > 14:
            print("outside board size")
            reset(savedBoard, savedHand)
            return False
        if board[y][x]["letter"] != "#" and board[y][x]["letter"] != i:
            print("tring to overwrite letter")
            reset(savedBoard, savedHand)
            return False
        elif board[y][x]["letter"] == "#":
            if i not in hand:
                print("letter not in hand")
                reset(savedBoard, savedHand)
                return False
            hand[hand.index(i)] = "#"
            board[y][x]["letter"] = i

        board[y][x]["letter"] = i
        board[y][x]["occupied"] = True
        wordPoints += 1
        positionDelta+=1

    print("checks succeded, word: '" + word + "' written")
    return True


        


        

print("hand: " + str(hand))        
placeWord("glass", "C5", "L")
print("hand: " + str(hand))
displayBoard()
print("sax" in words)