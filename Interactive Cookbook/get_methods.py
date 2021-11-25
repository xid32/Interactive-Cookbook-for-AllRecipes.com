import json
from parse import findDirection
from fetchURL import fetchURL
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re
import urllib.request

primary_method = ['boil','bake','fry','roast','grill','steam','poach','simmer','broil','blanch','braise','stew']
other_method = ['bread machine', 'al dente', 'amandine', 'au gratin', 'au ju', 'baghaar', 'bain-marie', 'bard', 'barbecue', 'baste', 'bast', 'brais', 'brine', 'broast', 'brown', 'caramelize', 'casserole', 'charboil', 'chiffonade', 'velvet', 'coddle', 'conche', 'confit', 'cream', 'croquette', 'curdl', 'cure', 'deep fry', 'deglaze', 'deglaz', 'degrease', 'degreas', 'dredge', 'dry roast', 'dry', 'emulsifi', 'en papillote', 'en vessie', 'engastr', 'ferment', 'flambe', 'fillet', 'foam', 'fondue', 'fricassee', 'frost', 'garnish', 'glaze', 'gratin', 'hibachi', 'infuse', 'jug', 'juice', 'julien', 'julienne', 'kalua', 'karaage', 'kho', 'kinpira', 'lard', 'macer', 'marinate', 'marin', 'macerate', 'mince', 'microwave', 'parbake', 'parboil', 'pasteurize', 'pickle', 'puree', 'proof', 'reduce', 'reduct', 'render', 'rice', 'rotisserie', 'roux', 'saute', 'score', 'sear', 'season', 'smoke', 'sour', 'smother', 'sous-vide', 'steep', 'stir-fry', 'stuff', 'tandoor', 'temper', 'tenderize', 'tender', 'teriyaki', 'thermal', 'thicken', 'wok', 'zest', 'preheat', 'pre-heat', 'mix', 'sprinkle', 'coat', 'drizzle', 'glossary', 'chop', 'grate', 'stir', 'shake', 'crush', 'squeeze']

def get_method():
    f = open("url.txt", "r")
    s = f.read()

    text = findDirection(s)['recipeInstructions']
    content = []
    porter_stemmer = PorterStemmer()
    wordnet_lemmatizer = WordNetLemmatizer()
    m = []
    for i in text:
        t = re.sub(r'[^\w\s]', '', i['text']).split()
        ws = ''
        for j in t:
            if wordnet_lemmatizer.lemmatize(j).endswith('e'):
                ws+= wordnet_lemmatizer.lemmatize(j).lower()
            else:
                ws+= porter_stemmer.stem(j).lower()
            ws+=' '
        content.append(ws)

    pm = []
    om = []
    for i in content:
        for j in primary_method:
            if i.find(j)>=0 and j not in pm:
                pm.append(j)
        for j in other_method:
            if i.find(j)>=0 and j not in om:
                om.append(j)

    # print('Primary Methods:')
    # print(pm)
    # print('Other Methods:')
    # print(om)
    # print()
    return [pm, om]

def test():
    # s = 'https://www.allrecipes.com/recipe/21202/ham-and-cheese-breakfast-tortillas/' 
    # fetchURL(s)
    s = 'https://www.allrecipes.com/recipes/16376/healthy-recipes/lunches/'
    a = urllib.request.urlopen(s)
    a = a.readlines()
    urls = []

    for i in a:
        if str(i).find('https://www.allrecipes.com/recipe/')>=0:
            url = str(i)[str(i).find('https://www.allrecipes.com/recipe/'):]
            urls.append(url[:url.find('"')])
    for i in range(len(urls)):
        print('Recipe ' + str(i+1) + ':')
        fetchURL(urls[i])
        get_method()
    
