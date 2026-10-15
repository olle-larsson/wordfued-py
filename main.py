import json

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
board = []

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

print("sax" in words)