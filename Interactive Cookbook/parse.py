import json
from fetchURL import fetchURL

def findIngredient(s):
    start = s.find('"recipeIngredient": [') 
    end = start
    while s[end] != ']':
        end += 1
    return s[start:end+1]

def findDirection(s):
    start = s.find('"recipeInstructions": [') 
    end = start
    while s[end] != ']':
        end += 1
    jsonObj = json.loads("{" + s[start:end+1] + "}")
    return jsonObj


# fetchURL('https://www.allrecipes.com/recipe/278271/air-fryer-stuffed-mushrooms/')
# f = open("url.txt", "r")
# s = f.read()

# print(findDirection(s))

# fetchURL('https://www.allrecipes.com/recipe/278271/air-fryer-stuffed-mushrooms/')
# f = open("url.txt", "r")
# s = f.read()

# print(findIngredient(s))
# print("\n\n")
# print(json.dumps(findDirection(s), indent=4, sort_keys=True))
# print("\n\n")

