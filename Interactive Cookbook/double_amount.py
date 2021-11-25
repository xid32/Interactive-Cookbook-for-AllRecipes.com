from unidecode import unidecode
from fractions import Fraction
import copy
import json


def double_amount():

    f = open('recipe_representation.json')
    rep = json.load(f)

    ingradient_list = rep['ingredients']
    ingradient_double = copy.deepcopy(ingradient_list)

    for i in range(len(ingradient_list)):
        if ingradient_list[i]['quantity'] == "adjustable amount of your choice":
            ingradient_double[i]['quantity'] = "adjustable amount of your choice"
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

    print('All ingredients doubled! Methods, tools and directions remains the same.')

    recipe_double = {}
    recipe_double['name'] = rep['name']
    recipe_double['directions'] = rep['directions']
    recipe_double['ingredients'] = ingradient_double
    recipe_double['methods'] = rep['methods']
    recipe_double['tools'] = rep['tools']

    # Save new recipe as a file
    with open('recipe_representation.json', 'w') as fp:
        json.dump(recipe_double, fp, sort_keys=True, indent=4)

if __name__ == '__main__':
    double_amount()
