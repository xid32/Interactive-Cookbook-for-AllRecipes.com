from unidecode import unidecode
from fractions import Fraction
from nltk import word_tokenize
from to_meat import to_meat
import copy
import json


def to_unhealthy():

    f = open('recipe_representation.json')
    rep = json.load(f)

    ingradient_list = rep['ingredients']
    ingradient_double = copy.deepcopy(ingradient_list)

    for i in range(len(ingradient_list)):

        if not is_unhealthy(ingradient_list[i]["ingredient_name"]):
            continue

        get_quantity = unidecode(ingradient_list[i]['quantity']).split()
        if len(get_quantity) > 0:
            if len(get_quantity) == 1:
                quantity_num = float(Fraction(get_quantity[0]))
            else:
                quantity_num = float(Fraction(get_quantity[0]) + Fraction(get_quantity[1]))

            quantity_double = quantity_num * 2
            ingradient_double[i]['quantity'] = str(quantity_double)

            print(ingradient_list[i]['ingredient_name'] + ' doubled, from ' + str(quantity_num) + ' to ' + str(quantity_double))

    # print('All ingredients doubled! Methods, tools and directions remains the same.')

    recipe_double = {}
    recipe_double['name'] = rep['name']
    recipe_double['directions'] = rep['directions']
    recipe_double['ingredients'] = ingradient_double
    recipe_double['methods'] = rep['methods']
    recipe_double['tools'] = rep['tools']

    # Save new recipe as a file
    with open('recipe_representation.json', 'w') as fp:
        json.dump(recipe_double, fp, sort_keys=True, indent=4)

def is_unhealthy(name):
    unhealthy = ["salt", "oil", "sugar"]
    for token in word_tokenize(name):
        if token.lower() in unhealthy:
            return True
    return False

if __name__ == '__main__':
    print("Will try to replace some healthy ingredients with unhealthy ones and increase the amount of unhealthy ingredients")
    to_unhealthy()
    # Add more meat
    to_meat()
    print("Junkified!")
