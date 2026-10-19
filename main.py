import json
import copy

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
board = []
hand = ["A", "H", "E", "J"]

def initBoard():
    for i in range(15):
        row = []
        for j in range(15):
            row.append({
                "letter": "#",
                "occupied": False
            })
        board.append(row)

initBoard()

def displayBoard():
    boardString = ""
    for i, rowY in enumerate(board):
        for k, cell in enumerate(rowY):
            if cell["occupied"]:
                boardString += cell["letter"] + " "
            else:
                boardString += "# "

        boardString += "\n"
    print(boardString)

displayBoard()

with open("words.json", "r", encoding="utf-8") as file:
    words = set(json.load(file)["words"])


def checkWord(word):
    return word in words

def increaseCoordinate(coordinate, direction, delta):

    x = alphabet.index(coordinate[0]) + 1

    y = coordinate[1]
    if (len(coordinate) == 3):
        y = y + coordinate[2]
    y = int(y)

    if direction.upper() == "V":
        x = x + delta
    elif direction.upper() == "L":
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
    if (not checkWord(word)):
        print("word not in word list")
        return False
    if (direction.upper() !="V" and direction.upper() != "L"):
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
placeWord("hej", "A14", "V")
print("hand: " + str(hand))
displayBoard()
print("sax" in words)