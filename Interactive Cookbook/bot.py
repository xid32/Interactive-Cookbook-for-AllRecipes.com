"""import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')"""

import random
import get_directions
import get_ingredients
import re
import Levenshtein as lev


ask_input = ["walk me through a recipe from allrecipes.com."]
ask_response = ["Sure. Please specify a URL."]

url_response = ["Alright. So let's start working with {} What do you want to do?"]

ingredients_input = ["1", "Show me the ingredients list."]

navigation_utterances = ["go back one step", "go to the next step", "take me to the"]

thanks_input = ["Thanks", "Thanks again!", "Thanks!"]
yes_input = ["Yes", "Yes, please.", "please."]


def leven(str1, str2):
    return lev.ratio(str1.lower(), str2.lower()) > 0.50


def generate_ask_response(ask):
    for input_ in ask_input:
        if leven(ask.lower(), input_):
            return random.choice(ask_response)        


def generate_url_response(url):
    if "https://" in url.lower():
        return random.choice(url_response)


def generate_ingredients_response(option):
    if option in ingredients_input:
        str = ""
        final_str = ""
        for ing in ingredients:
            str = ing['quantity'] + " " + ing["measurement"] + " " + ing["ingredient_name"]
            if ing['preparation'] != "":
                str += ", " + ing['preparation']
            str = " ".join(str.split())
            final_str += str + "\n"
        return final_str

def is_go_over_steps(human_text):
    key_words = ["2", "2.", "[2]", "go over recipe steps"]
    return human_text.lower() in key_words

def is_navigation(human_text):
    txt = human_text.lower()
    if txt == "next" or txt == "back": return True
    if txt in navigation_utterances: return True
    for utter in navigation_utterances:
        if leven(txt, utter):
            return True
    return False

def return_number_str(num):
    if num == 1:
        return str(num) + "st"
    elif num == 2:
        return str(num) + "nd"
    elif num == 3:
        return str(num) + "rd"
    else:
        return str(num) + "th"


bot_name = "Sous-chef"
name = ""
direction = None
ingredients = None
steps = 0
flag = True
search_url = "https://www.google.com/search?q="

ask_flag = True
url_flag = True
recipe_flag = False

while flag:
    print("User: ", end="")
    # print("\n")
    # print("ask ",ask_flag)
    # print("url ", url_flag)
    # print("recipe ",recipe_flag)

    human_text = input()
    # print("generate_ask_response ", generate_ask_response(human_text))
    # print("\n")
    if generate_ask_response(human_text) is not None and ask_flag:
        print(bot_name + ": " + generate_ask_response(human_text))
        ask_flag = False
    elif generate_url_response(human_text) is not None and not ask_flag and url_flag:
        parse = human_text.split("/")
        name = parse[-2]

        direction = get_directions.get_directions(human_text)
        ingredients = get_ingredients.get_ingredients_withURL(human_text)

        print(bot_name + ": " + generate_url_response(human_text).format('"' + name + '"'))
        print(bot_name + ": " + "[1] Go over ingredients list or [2] Go over recipe steps.")
        url_flag = False
    elif generate_ingredients_response(human_text) is not None and not ask_flag and not url_flag:
        print(bot_name + ": " + "Here are the ingredients for {}:".format(name))
        print(generate_ingredients_response(human_text))
        print(bot_name + ": Please enter 2 if you want to go over recipe steps")
    elif is_go_over_steps(human_text) and not ask_flag and not url_flag:
        print(bot_name + ": The " + return_number_str(steps + 1) + " step is: " + direction[steps]['action'])
        recipe_flag = True
    elif human_text in yes_input and not ask_flag and not url_flag and recipe_flag:
        steps += 1
        if 0 <= steps < len(direction):
            print(bot_name + ": The " + return_number_str(steps + 1) + " step is: " + direction[steps]['action'])
            recipe_flag = True
        else:
            steps -= 1
            print(bot_name + ": Invalid Steps")
    elif (human_text[:14] in navigation_utterances or is_navigation(human_text)) and not ask_flag and not url_flag and recipe_flag:
        list = re.findall(r'\d+', human_text)
        add = 0
        if "one" in human_text or "back" in human_text:
            steps -= 1
            add = 1
        elif "next" in human_text:
            steps += 1
            add = -1
        elif len(list) > 0:
            steps = int(list[0]) - 1

        if 0 <= steps < len(direction):
            print(bot_name + ": The " + return_number_str(steps + 1) + " step is: " + direction[steps]['action'])
            recipe_flag = True
        else:
            steps += add
            print(bot_name + ": Invalid Steps")
    elif human_text == "How do I do that?" and not ask_flag and not url_flag and recipe_flag:
        print(bot_name + ": No worries. I found a reference for you:" + search_url + direction[steps]['action'].replace(
            " ", "+"))
    elif "How do I" in human_text and not ask_flag and not url_flag and recipe_flag:
        left = human_text.removeprefix("How do I")
        left.strip().replace(" ", "+")
        print(bot_name + ": No worries. I found a reference for you:" + search_url + left)
    elif human_text in thanks_input and not ask_flag and not url_flag and recipe_flag:
        print(bot_name + ": Should I continue to the " + return_number_str(steps + 2) + " step?")
    elif human_text == "quit":
        print(bot_name+": Bye. Good Luck!")
        break
    else:
        print(bot_name + ": Sorry, I don't understand. Could you rephrase the question, please?")
