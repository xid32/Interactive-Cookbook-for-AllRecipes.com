from unidecode import unidecode
from fractions import Fraction
import copy
import json


def amount_cut_half():

    f = open('recipe_representation.json')
    rep = json.load(f)

    ingradient_list = rep['ingredients']
    ingradient_half = copy.deepcopy(ingradient_list)

    for i in range(len(ingradient_list)):
        if ingradient_list[i]['quantity'] == "adjustable amount of your choice":
            ingradient_half[i]['quantity'] = "adjustable amount of your choice"
            continue

        get_quantity = unidecode(ingradient_list[i]['quantity']).split()
        print(get_quantity)
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

    print('All ingredients cut by half! Methods, tools and directions remains the same.')

    recipe_half = {}
    recipe_half['name'] = rep['name']
    recipe_half['directions'] = rep['directions']
    recipe_half['ingredients'] = ingradient_half
    recipe_half['methods'] = rep['methods']
    recipe_half['tools'] = rep['tools']

    # Save new recipe as a file
    with open('recipe_representation.json', 'w') as fp:
        json.dump(recipe_half, fp, sort_keys=True, indent=4)

if __name__ == '__main__':
    amount_cut_half()
