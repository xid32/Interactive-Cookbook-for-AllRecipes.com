from get_tools import TOOLS, get_tools_wrapper
from fetchURL import fetchURL
from parse import findDirection
from get_methods import get_method
from get_ingredients import get_ingredients_withURL
from nltk import word_tokenize
import re
import json
import urllib.request


url = 'https://www.allrecipes.com/recipe/270363/guinness-cupcakes-with-espresso-frosting/'
def get_directions(url):
    parse = url.split('/')
    name = parse[-2]
    fetchURL(url)
    f = open("url.txt", "r")
    s = f.read()
    TOOLS = get_tools_wrapper()
    dirs = findDirection(s)["recipeInstructions"]
    methods = get_method()[0] + get_method()[1]
    ingredients = get_ingredients_withURL(url)
    dirs_rep = []
    for dir in dirs:
        text = dir["text"]
        sents = text.split(".")
        for sent in sents:
            if sent == "\n": continue
            dir_rep = {}
            dir_rep["action"] = sent
            dir_rep["tools"] = find_tools(sent)
            dir_rep["methods"] = find_methods(sent, methods)
            dir_rep["time"] = find_time(sent)
            dir_rep["ingredients"] = find_ingredients(ingredients, sent)
            dirs_rep.append(dir_rep)

    representation = {"name":name,"ingredients": ingredients, "methods": methods, "tools":TOOLS, "directions": dirs_rep}
    with open('recipe_representation.json', 'w') as fp:
        json.dump(representation, fp, sort_keys=True, indent=4)
    return dirs_rep
    
def find_methods(text, methods):
    methods_for_this_step = []
    for method in methods:
        if method in text:
            methods_for_this_step.append(method)
    return methods_for_this_step


def find_tools(text):
    TOOLS = get_tools_wrapper()
    tools_for_this_step = []
    for TOOL in TOOLS:
        if TOOL in text:
            tools_for_this_step.append(TOOL)
    return tools_for_this_step

def find_ingredients(ingredients, sent):
    ingredient_for_this_step = []
    for ingredient in ingredients:
        name = ingredient["ingredient_name"]
        if is_in(word_tokenize(name), sent):
            ingredient_for_this_step.append(name)
    return ingredient_for_this_step

def is_in(tokens, sent):
    for token in tokens:
        if token in sent: return True
    return False

# TODO: Remove Overlap time
def find_time(text):

    # Rules:
    to_ = re.findall(r"[0-9]+ to [0-9]+ minutes", text)
    hour_minute = re.findall(r"[0-9]+ hour and [0-9]+ minute", text)
    minute_second = re.findall(r"minute and [0-9]+ second", text)

    # Probably don't need hour_second and hour_minute_second since they are too specific
    second = re.findall(r" [0-9]+ second", text)
    minute = re.findall(r" [0-9]+ minute", text)
    hour = re.findall(r" [0-9]+ hour", text)


    rules = [to_, hour_minute, minute_second, second, minute, hour]
    time = {}
    for rule in rules:
        for item in rule:
            ind = text.find(item)
            while ind in time and ind < len(text):
                oldind = ind
                ind = text[oldind+len(item):].find(item)
                ind = oldind + len(item) + ind
            time[ind] = item
    # new_time_dict = dict(sorted(time.items(), key=lambda item: item[1]))
    # return new_time_dict
    return remove_overlap_time(time)

def remove_overlap_time(time_dict):
    interval = []
    for ind in time_dict:
        if is_compound_time(time_dict[ind]):
            start = ind
            end = start + len(time_dict[ind])
            interval.append((start, end))

    for ind in time_dict:
        if not is_compound_time(time_dict[ind]):
            start = ind
            if is_overlap(start, interval):
                time_dict[ind] = "removed"
    return time_dict

def is_compound_time(time):
    return ("hour" in time and "minute" in time) or ("minute" in time and "second" in time) 
    
def is_overlap(start, interval):
    for tup in interval:
        if tup[0] <= start + 1 and start + 1 <= tup[1]: return True
    return False

test_url = "https://www.allrecipes.com/recipe/166101/apricot-chicken-with-balsamic-vinegar/"
get_directions(test_url)

# print(json.dumps(get_directions(url), indent=4, sort_keys=True))
# print(find_time("heat for 5 hour and 15 minute, boil for 5 minute, wait 5 minute to cool"))

# dir = "5 hour, 5 hour, 5 hour, 5 hour, heat for 5 hour and 15 minute, boil for 5 minute, wait 5 minute to cool"
# dicti = find_time(dir)
# for key in dicti:
#     print(dir[key:key+16])

# def test(nums):
#     s = 'https://www.allrecipes.com/recipes/16376/healthy-recipes/lunches/'
#     a = urllib.request.urlopen(s)
#     a = a.readlines()
#     urls = []

#     for i in a:
#         if str(i).find('https://www.allrecipes.com/recipe/')>=0:
#             url = str(i)[str(i).find('https://www.allrecipes.com/recipe/'):]
#             urls.append(url[:url.find('"')])

#     for num in nums:
#         print(json.dumps(get_directions(urls[num]), indent=4, sort_keys=True))
#         # print(num)
#         # print(get_ingredients_withURL(urls[num]))
#         # print("\n\n\n")
#         break


# test(list(range(0, 10)))


