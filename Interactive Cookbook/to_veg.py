from nltk import word_tokenize
import json
from unidecode import unidecode
from fractions import Fraction
import random
import copy


def to_veg():

    # Assume that you already called get_directions() which saved our representation as a file
    # A file with name "recipe_representation" is already in the current directory

    f = open('recipe_representation.json')
    rep = json.load(f)

    meats = ["turkey", "chicken", "pork", "beef", "brisket", "duck", "lamb", "ham", "sausage",
            "fish", "shrimp", "seafood", "salmon", "venison", "rabbit", "goat", "poultry", "goose", "meat",
            "bacon", ""]

    veg_list = ["tempeh", "tofu", "seitan", "black beans", "oat flakes", "lentils",
                "green seplt"]
    meat_sub = {}


    for meat in meats:
        meat_sub[meat] = random.choice(veg_list)

    recipe_transformation = {}
    
    recipe_transformation["name"] = rep["name"]

    # Ingredients:  Meat to Vegetables
    print("Transforming Ingredients: ")
    recipe_transformation["ingredients"] = get_transformed_ingredients(rep["ingredients"], meat_sub)

    # Directions: Meat to Vegetables
    # print(rep["directions"])
    print("Transforming Directions: ")
    recipe_transformation["directions"] = get_transformed_directions(rep["directions"], meat_sub)

    # Tools and Methods remain the same
    recipe_transformation["tools"] = rep["tools"]
    recipe_transformation["methods"] = rep["methods"]




    # Save new recipe as a file
    with open('recipe_representation.json', 'w') as fp:
        json.dump(recipe_transformation, fp, sort_keys=True, indent=4)

def get_transformed_ingredients(ingredients, meat_sub):
    transformed_ingredients = []
    for ingredient in ingredients:
        name = ingredient["ingredient_name"]
        if is_meat(name, meat_sub):
            transformed_ingredient = {}
            transformed_ingredient["ingredient_name"] = get_meat_sub(name, meat_sub)
            transformed_ingredient["measurement"] = ""
            transformed_ingredient["preparation"] = ""
            transformed_ingredient["quantity"] = "adjustable amount of your choice"
            transformed_ingredients.append(transformed_ingredient)
        else:
            transformed_ingredients.append(ingredient)
    return transformed_ingredients

def get_transformed_directions(directions, meat_sub):
    transformed_directions = []


    for direction in directions:
        old_ingredients = direction["ingredients"]
        new_ingredients = []
        old_action = direction["action"]
        new_action = ""
        # Ingredient field

        if old_ingredients:
            for old_ingredient in old_ingredients:
                if is_meat(old_ingredient, meat_sub):
                    new_ingredients.append(get_meat_sub(old_ingredient, meat_sub))
                    new_action = get_new_veg_action(old_ingredient, old_action, meat_sub)
                    break

                else:
                    new_ingredients.append(old_ingredient)
                    new_action = old_action
        else:
            new_ingredients = []
            new_action = old_action


        transformed_directions.append({"ingredients":new_ingredients, "tools": direction["tools"], "methods":direction["methods"], "time":direction["time"], "action": new_action})


    return transformed_directions


def is_meat(name, meat_sub):
    for token in word_tokenize(name):
        if token in meat_sub:
            return True
    return False

def get_meat_sub(name, meat_sub):
    for token in word_tokenize(name):
        if token in meat_sub:
            print("Replaced ", name, " with: ", meat_sub[token])
            return meat_sub[token]

def get_new_veg_action(old_ingredient, old_action, meat_sub):
    if old_ingredient in old_action:
        # print("replace: ", old_ingredient, " with ", get_meat_sub(old_ingredient, meat_sub))
        return old_action.replace(old_ingredient, get_meat_sub(old_ingredient, meat_sub))
    else:
        # print("replace: ", old_ingredient, " with ", replace_meat(old_ingredient, old_action, meat_sub))
        return replace_meat(old_ingredient, old_action, meat_sub)

def replace_meat(old_ingredient, old_action, meat_sub):
    for token in word_tokenize(old_ingredient):
        if token in meat_sub:
            if token in old_action:
                print("token: ", token)
                return old_action.replace(token, meat_sub[token])
            # return "add " + meat_sub[token]
            # return old_ingredient.replace(token, meat_sub[token])
    return old_action

if __name__ == '__main__':
    to_veg()
    
