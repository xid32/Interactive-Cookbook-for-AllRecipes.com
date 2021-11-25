import json
import sys
import unicodedata
import requests
from bs4 import BeautifulSoup


class Ingredient:
    def __init__(self, ingredient_name, quantity, measurement, preparation):
        self.ingredient_name = ingredient_name
        self.quantity = quantity
        self.measurement = measurement
        self.preparation = preparation


def get_ingredients(key_words):
    URL = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re' % key_words
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    recipe_a_tags = soup.select(selector="article.fixed-recipe-card div.fixed-recipe-card__info > a")
    recipe_list = []
    for a_tag in recipe_a_tags:
        ingredient_list = []

        recipe_link = a_tag['href']
        page = requests.get(recipe_link)
        soup = BeautifulSoup(page.content, 'html.parser')
        ingredient_inputs = soup.select(selector="ul.ingredients-section li label input")

        for i in ingredient_inputs:
            ing_name = i['data-ingredient']
            ing_preparation = ''

            if "," in ing_name:
                parts = ing_name.split(",")
                ing_name = parts[0]
                ing_preparation = parts[1].strip()

            ing_quantity = i['data-quantity']
            ing_measurement = i['data-unit']

            ingredient_list.append(Ingredient(ing_name, ing_quantity, ing_measurement, ing_preparation))
        recipe_list.append(ingredient_list)

    with open("output.txt", "w", encoding='utf8') as file:
        for recipe in recipe_list:
            for ingredient in recipe:
                d = ingredient.__dict__
                r = json.dumps(d, ensure_ascii=False).encode('utf8').decode()
                file.write(r + "\n")
                print(r)
            file.write("\n")
            print("\n")



def get_ingredients_withURL(recipe_link):
    recipe_list = []
    ingredient_list = []
    page = requests.get(recipe_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    ingredient_inputs = soup.select(selector="ul.ingredients-section li label input")

    for i in ingredient_inputs:
        ing_name = i['data-ingredient']
        ing_preparation = ''

        if "," in ing_name:
            parts = ing_name.split(",")
            ing_name = parts[0]
            ing_preparation = parts[1].strip()

        ing_quantity = i['data-quantity']
        ing_measurement = i['data-unit']

        ingredient_list.append(Ingredient(ing_name, ing_quantity, ing_measurement, ing_preparation))
    recipe_list.append(ingredient_list)

    ingradient_list = []
    for ingredient in recipe_list[0]:
        d = ingredient.__dict__
        ingradient_list.append(d)
    return ingradient_list


if __name__ == '__main__':
    ingredient_value = 'guinnes cupcakes'
    get_ingredients(ingredient_value)

