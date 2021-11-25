from unidecode import unidecode
from fractions import Fraction
from nltk import word_tokenize
import copy
import json
from to_veg import to_veg


# Reduce unhealthy ingredient by 50%
def to_healthy():

    f = open('recipe_representation.json')
    rep = json.load(f)

    ingradient_list = rep['ingredients']
    ingradient_half = copy.deepcopy(ingradient_list)

    for i in range(len(ingradient_list)):
        if not is_unhealthy(ingradient_list[i]["ingredient_name"]):
            continue
        get_quantity = unidecode(ingradient_list[i]['quantity']).split()
        if len(get_quantity) > 0:
            if len(get_quantity) == 1:
                quantity_num = float(Fraction(get_quantity[0]))
            else:
                quantity_num = float(Fraction(get_quantity[0]) + Fraction(get_quantity[1]))

            if len(ingradient_list[i]['measurement']) != 0:
                quantity_half = quantity_num / 2
            else:
                quantity_half = quantity_num // 2
            ingradient_half[i]['quantity'] = str(quantity_half)

            print(ingradient_list[i]['ingredient_name'] + ' cut by half, from ' + str(quantity_num) + ' to ' + str(quantity_half))

    recipe_half = {}
    recipe_half['name'] = rep['name']
    recipe_half['directions'] = rep['directions']
    recipe_half['ingredients'] = ingradient_half
    recipe_half['methods'] = rep['methods']
    recipe_half['tools'] = rep['tools']

    # Save new recipe as a file
    with open('recipe_representation.json', 'w') as fp:
        json.dump(recipe_half, fp, sort_keys=True, indent=4)



def is_unhealthy(name):
    unhealthy = ["salt", "oil", "sugar"]
    for token in word_tokenize(name):
        if token.lower() in unhealthy:
            return True
    return False

if __name__ == '__main__':
    print("Will try to replace some meat with vegetables and reduce the amount unhealthy ingredient")
    to_healthy()
    # Add some vegetables
    to_veg()
    print("Healthified!")
