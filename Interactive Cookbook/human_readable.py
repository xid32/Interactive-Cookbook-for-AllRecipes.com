import json

def main():
    f = open('recipe_representation.json')
    recipe = json.load(f)
    print('Recipe: ' + recipe['name'])
    print('Ingredient:')
    for i in recipe['ingredients']:
        print(' - '+i['quantity']+' '+i['preparation'] +' ' +i['measurement']+' ' +i['ingredient_name'])
    print('Direction')

    j = 0
    for i in range(len(recipe['directions'])):
        if recipe['directions'][i]['action']:
            print(str(j+1) + '. ' + recipe['directions'][i]['action'])
            j += 1


if __name__ == '__main__':
    main()
    
