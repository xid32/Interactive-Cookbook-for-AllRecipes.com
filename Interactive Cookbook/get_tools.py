from fetchURL import fetchURL
import nltk
import re


def findDirection(s):
    start = s.find('"recipeInstructions": [')
    end = start
    while s[end] != ']':
        end += 1
    return s[start:end+1]

def find_all(s, c):
    idx = s.find(c)
    while idx != -1:
        yield idx
        idx = s.find(c, idx + 1)

def get_steps(direction):
    l = find_all(direction, '"text":')
    steps = []
    step = ''
    for i in l:
        start = i+9
        end = start
        while direction[end] != '"':
            end += 1
        steps.append(direction[start: end-2])
        step = step + ' ' + direction[start: end-2]
    return step[1:]

def get_relist():
    using_ = re.compile(r"(?:(?: using ))(.*)")
    bring_ = re.compile(r"(?:(?: bring ))(.*)")
    preheat_ = re.compile(r"(?:(?: preheat ))(.*)")
    with_ = re.compile(r"(?:(?: with ))(.*)")
    in_ = re.compile(r"(?:(?: in ))(.*)")
    on_ = re.compile(r"(?:(?: on ))(.*)")
    by_ = re.compile(r"(?:(?: by ))(.*)")
    into_ = re.compile(r"(?:(?: into ))(.*)")
    relist = [using_, bring_, preheat_, with_, in_, on_, by_, into_]
    return relist

def get_tools():
    # fetchURL('https://www.allrecipes.com/recipe/270363/guinness-cupcakes-with-espresso-frosting/')
    f = open("url.txt", "r")
    s = f.read()

    dir = findDirection(s)
    st = get_steps(dir)
    st = ' ' + st
    stop_words = ['back', 'size', 'water', 'row', 'side', 'mixture', 'heat']
    tools = []
    relist = get_relist()
    for r in relist:
        tls = re.findall(r, st.lower())
        if len(tls) > 0:
            for c in tls:
                words = nltk.word_tokenize(c)
                tags = nltk.pos_tag(words)
                tool = ''
                for t in tags:
                    if t[1] == 'NN':
                        if t[0] in stop_words:
                            continue
                        tool += t[0]
                        tool += ' '
                    else:
                        if len(tool) > 0:
                            tools.append(tool[:-1])
                            break
    return list(set(tools))

fetchURL("https://www.allrecipes.com/recipe/166101/apricot-chicken-with-balsamic-vinegar/")
TOOLS = get_tools()

def get_tools_wrapper():
    return get_tools()
















