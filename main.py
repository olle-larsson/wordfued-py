import json

with open("words.json", "r", encoding="utf-8") as file:
    words = set(json.load(file)["words"])

print("saxen" in words)