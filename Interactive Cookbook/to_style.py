import json
from parse import findDirection, findIngredient
from fetchURL import fetchURL
import urllib.request
from get_ingredients import get_ingredients_withURL
import random
from nltk.corpus import stopwords


VEG = ['brussels sprouts','tofu','bamboo','long beans','bean sprouts','green pepper','red pepper','red bell pepper','fresh jalapeno peppers','acorn squash', 'amaranth', 'anaheim chile', 'arrowroot', 'artichoke', 'arugula', 'asparagus', 'baby candy cane beets', 'baby oyster mushrooms', 'banana squash', 'beets', 'belgian endive', 'bell peppers', 'bitter melons', 'black radish', 'black salsify', 'bok choy', 'boniato', 'broccoflower', 'broccoli', 'broccoli rabe', 'broccolini', 'brussels sprouts', 'burdock root', 'butter lettuce', 'buttercup squash', 'butternut squash', 'cactus', 'cardoon', 'carnival squash', 'carrot', 'cauliflower', 'celeriac', 'celery', 'chanterelle mushroom', 'chayote squash', 'cherry tomato', 'chinese eggplant', 'chinese long bean', 'cipolline onions', 'collard greens', 'corn', 'corn salad', 'crookneck squash', 'cucumber', 'daikon radish', 'dandelion greens', 'delicata squash', 'eggplant', 'endive', 'enoki mushrooms', 'fava beans', 'fennel', 'fiddlehead ferns', 'fingerling potato', 'french beans', 'gai lan', 'galangal root', 'garlic', 'ginger root', 'green beans', 'green cabbage', 'green onion', 'green soybeans', 'green tomato', 'hearts of palm', 'horseradish root', 'hubbard squash', 'iceberg lettuce', 'jalapeno peppers', 'jerusalem artichokes', 'jicama', 'kabocha squash', 'kale', 'kohlrabi', 'lamb’s quarters', 'leaf lettuce', 'leek', 'manoa lettuce', 'morel mushrooms', 'mushrooms', 'mustard greens', 'okra', 'olives', 'ong choy spinach', 'onion', 'opo squash', 'parsnips', 'peas', 'pearl onions', 'potato', 'pumpkin', 'purple asparagus', 'purple hull peas', 'purslane', 'radicchio', 'radish', 'red leaf lettuce', 'red potato', 'rhubarb', 'romaine lettuce', 'rutabaga', 'salad savoy leafy vegetable', 'serrano chili peppers', 'shallots', 'shiitake mushrooms', 'snow peas', 'sorrel', 'spinach', 'sugar snap peas', 'summer squash', 'sweet dumpling squash', 'sweet potato', 'swiss chard', 'tarragon', 'tomatillo', 'tomato', 'turnip', 'upland cress', 'vidalia onions', 'wasabi root', 'watercress', 'white asparagus', 'winged beans', 'yam', 'yucca root', 'yukon gold potatoes', 'zucchini']
FRUIT = ['apple', 'apricots, fresh', 'apricots, dried', 'armenian cucumber', 'asian pears', 'avocado', 'banana', 'barbados cherry', 'black crowberry', 'black currants', 'blackberries', 'blood orange', 'blueberries', 'boysenberries', 'breadfruit', 'brown turkey fig', 'cactus pear', 'canary melon', 'cantaloupe', 'cape gooseberries', 'cara cara navel orange', 'caribbean june plum', 'carissa', 'casaba melon', 'champagne grapes', 'cherimoya', 'cherries', 'cherries, sour', 'chokecherries', 'clementines', 'coconut', 'concord grapes', 'cotton candy grapes', 'crab apples', 'cranberries, fresh', 'cranberries, dried', 'crenshaw melon', 'custard apple', 'd’agen sugar plum', 'dates', 'date plum', 'durian', 'elderberries', 'feijoa', 'fig, fresh', 'fig, dried', 'galia melon', 'golden kiwifruit', 'grape juice', 'grapefruit', 'grapes', 'guava', 'honeycrisp apple', 'honeydew melon', 'huckleberries', 'jackfruit', 'jambolan', 'jujube', 'kaffir lime', 'key lime', 'kiwano', 'kiwifruit', 'kumquat', 'lemon', 'lime', 'loganberries', 'longan', 'loquat', 'lychee', 'mamey sapote', 'mango', 'mangosteen', 'mandarin orange', 'maradol papaya', 'mediterranean medlar', 'mulberries', 'muscadine grapes', 'nectarine', 'orange', 'papaya', 'passion fruit', 'peach', 'pear', 'persian melon', 'persimmon', 'pineapple', 'plantain', 'plum', 'plum, dried', 'pomegranate', 'pummelo', 'quince', 'raisins', 'raspberries', 'red banana', 'red currants', 'rose apple', 'salmonberry', 'sapodilla', 'sapote', 'sharon fruit', 'soursop', 'south african baby pineapple', 'star fruit', 'strawberries', 'strawberry guava', 'strawberry papaya', 'sugar apple', 'surinam cherry', 'tangerine', 'ugli fruit', 'water coconut', 'watermelon', 'wild blueberries']
MEAT = ['mussel','steak','shrimp','anchovy','bacon','beef','buffalo','caribou','catfish','chicken','clams','cod','cornish game hen','crab','duck','eel','emu','goat','goose','grouse','halibut','ham','kangaroo','lamb','lobster','mackerel','mahi mahi','octopus','ostrich','oysters','pheasant','pork','quail','rabbit','salmon','sardines','scallops','shark','shrimp','snake','squab','squid','swordfish','tilapia','tuna','turkey','veal','venison','egg','yolk']
OTHER = ['oil','pancetta', 'olive oil', 'rosemary','salt', 'ketchup', 'brown sugar', 'cider vinegar', 'cooking spray', 'green bell pepper', 'dried thyme', 'seasoned salt', 'ground black pepper', 'prepared mustard', 'worcestershire sauce', 'hot pepper sauce', 'milk', 'oats', 'elbow macaroni', 'salt', 'butter', 'sour cream', 'cream cheese', 'shredded sharp cheddar cheese', 'all-purpose flour', 'ground cayenne pepper', 'shredded mild cheddar cheese', 'pecans', 'pure maple syrup', 'smoked paprika', 'chipotle pepper powder', 'water', 'uncooked arborio rice', 'dried basil', 'italian seasoning', 'crumbled feta cheese', 'paprika', 'pepper', 'italian seasoned bread crumbs', 'sugar', 'curry powder', 'poultry seasoning', 'salt and freshly ground black pepper to taste', 'vegetable oil', 'buttermilk', 'bulk italian sausage', 'chopped fresh basil', 'chopped fresh parsley', 'grated parmesan cheese', 'lasagna noodles', 'ricotta cheese', 'ground nutmeg', 'shredded mozzarella cheese', 'rice wine vinegar', 'salt and pepper to taste', 'hot chile paste', 'teriyaki sauce', 'yellow bell pepper', 'blanched slivered almonds', 'chopped fresh mint', 'green bell pepper', 'condensed cream of cheddar cheese soup', 'ground black pepper to taste', 'dried bread crumbs', 'sweet italian sausage', 'white sugar', 'dried basil leaves', 'mozzarella cheese', 'shredded cheddar cheese', 'condensed cream of mushroom soup', 'prepared yellow mustard', 'salt to taste', 'cabbage', 'monosodium glutamate', 'spring roll wrappers', 'oil for frying', 'dry pancit (canton) noodles', 'dried rosemary', 'white wine', 'dry fettuccini pasta', 'heavy cream', 'grated romano cheese', 'kaiser roll', 'hungarian hot paprika', 'barbeque sauce', 'light brown sugar', 'chili powder', 'salt and black pepper to taste', 'margarine', 'dried sage', 'capers', 'panko bread crumbs', 'olive oil for frying', 'fresh mozzarella', 'grated provolone cheese', 'uncooked elbow macaroni', 'bread crumbs', 'enriched white rice', 'soy sauce to taste', 'sesame oil', 'seasoned bread crumbs', 'rubbed sage', 'ground mustard', 'arborio rice', 'dry white wine', 'sea salt to taste', 'freshly ground black pepper to taste', 'finely chopped chives', 'freshly grated parmesan cheese', 'whole-grain bread', 'sliced toasted almonds', 'swiss cheese', 'medium seashell pasta', 'mascarpone cheese', 'paprika to taste', 'monterey jack cheese', 'soft white bread', 'red wine', 'cold butter', 'dried oregano', 'mayonnaise', 'dry stuffing mix', 'baking powder', 'seasoned dry bread crumbs', 'ground chuck', 'dried italian herbs', 'cayenne pepper', 'plain bread crumbs', 'dijon mustard', 'hot pepper sauce to taste', 'fresh parsley', 'dried italian herb seasoning']

T_VEG = ['garlic', 'cucumber', 'long beans', 'cherry tomato', 'red pepper', 'onion', 'red bell pepper', 'tomato', 'green onion', 'carrot', 'corn', 'shallots', 'jalapeno peppers', 'mushrooms', 'zucchini', 'bean sprouts', 'ginger root', 'leaf lettuce', 'bamboo']
T_FRUIT = ['lime', 'coconut', 'mango', 'lemon', 'apple', 'kaffir lime', 'orange', 'dates']
T_MEAT = ['mussel','chicken', 'eel', 'shrimp', 'bacon', 'egg', 'steak', 'beef', 'crab', 'pork']
T_OTHER = ['jasmine rice', 'vegetable oil', 'sliced ginger', 'white sugar', 'salt', 'water', 'pandan leaves', 'chopped ginger', 'Thai bird chile peppers', 'dark soy sauce', 'soy sauce', 'distilled white vinegar', 'salted soybean paste', 'fresh cilantro', 'tapioca flour', 'fish sauce', 'light soy sauce', 'ground white pepper', 'Thai chilies', 'palm sugar', 'roasted peanuts', 'rice vinegar', 'ground black pepper', 'fresh rice noodles', 'oyster sauce', 'fresh Thai basil leaves', 'uncooked short-grain white rice', 'tapioca starch', 'toasted sesame seeds', 'Thai fish sauce', 'Thai red curry paste', 'finely chopped unsalted peanuts', 'ground coriander', 'yellow curry powder', 'chili oil', 'chopped fresh cilantro', 'chopped unsalted peanuts', 'wooden skewers', 'prepared Thai peanut sauce', 'dried red chile peppers', 'ground cumin', 'paprika', 'ground turmeric', 'light or dark brown sugar', 'ground ginger', 'turmeric  ', 'chili powder', 'coarsely chopped peanuts', 'thinly sliced scallions', 'curry powder', 'whole cilantro leaves', 'tiger prawns', 'Panang curry paste', 'cooking oil', 'fresh red chile peppers', 'brown sugar', 'minced Thai chilies', 'very thinly sliced fresh basil leaves', 'rice wine vinegar', 'chopped cilantro', 'chopped peanuts', 'dry white wine', 'Asian fish sauce', 'tom yum paste', 'chopped green chile pepper', 'fresh coriander', 'fresh basil', 'smooth natural peanut butter', 'toasted sesame oil', 'galangal', 'olive oil', 'grated fresh ginger ', 'red curry paste', 'light brown sugar', 'rice noodles', 'butter', 'white wine vinegar', 'crushed peanuts', 'dried rice noodles', 'tamarind paste', 'coarsely ground peanuts', 'chopped fresh chives', 'sugar', 'curry paste', 'ginger', 'peanut butter', 'all-purpose flour', 'green curry paste', 'fresh ginger', 'cilantro leaves', 'crunchy peanut butter', 'Thai tea leaves', 'vanilla extract', 'crushed cardamom pods', 'crushed cloves', 'ground cinnamon', 'half-and-half', 'crushed ice', 'cooked basmati rice', 'honey', 'hot chile paste', 'Udon noodles', 'chopped fresh mint leaves', 'sweet chili sauce', 'peanut oil for frying', 'serrano peppers', 'sweet Thai basil', 'cilantro sprigs', 'green bell pepper', 'creamy peanut butter', 'hot sauce', 'packed brown sugar', 'cayenne pepper','dried flat rice noodles', 'Asian chile pepper sauce', 'chopped unsalted dry-roasted peanuts', 'uncooked long grain white rice', 'vegetable broth', 'Thai chile peppers', 'chile sauce', 'sliced yellow bell pepper', 'hot pepper sauce', 'nutmeg', 'black pepper', 'ground cloves', 'allspice', 'bay leaves', 'plain yogurt', 'sesame oil', 'milk', 'teriyaki sauce', 'chopped roasted peanuts', 'Thai glutinous rice', 'Himalayan salt ']

def to_thai():
    f = open('recipe_representation.json')
    rep = json.load(f)
    directions = rep['directions']
    stop_word = stopwords.words('english')
    new_direction = []
    total = []
    for i in directions:
        old = i["action"]
        action = i["action"].split()
        pos = []
        for a in range(len(action)):
            if action[a] not in stop_word:
                pos.append(a)
        ingredient = []
        for j in pos:
            for k in MEAT:
                if action[j].find(k)>=0 or k.find(action[j])>=0:
                    action[j] = T_MEAT[random.randint(0,len(T_MEAT)-1)]
                    ingredient.append(action[j])
                    break
            for k in VEG:
                if action[j].find(k)>=0 or k.find(action[j])>=0:
                    action[j] = T_VEG[random.randint(0,len(T_VEG)-1)]
                    ingredient.append(action[j])
                    break
            for k in FRUIT:
                if action[j].find(k)>=0 or k.find(action[j])>=0:
                    action[j] = T_FRUIT[random.randint(0,len(T_FRUIT)-1)]
                    ingredient.append(action[j])
                    break
            for k in OTHER:
                if action[j].find(k)>=0 or k.find(action[j])>=0:
                    action[j] = T_OTHER[random.randint(0,len(T_OTHER)-1)]
                    ingredient.append(action[j])
                    break
        new = ''
        for word in action:
            new+=word
            new+=' '
        for word in ingredient:
            if word not in total:
                total.append(word)
        new_direction.append({"action":new,"ingredients":ingredient,"methods":i["methods"],"time":i["time"],"tools":i["tools"]})
    rep["directions"] = new_direction

    pos = 0
    new_ing = rep["ingredients"]
    for j in new_ing:
        if pos<len(total):
            j["ingredient_name"] = total[pos]
            pos+=1

    rep["ingredients"] = new_ing
    with open('recipe_representation.json', 'w') as fp:
        json.dump(rep, fp, sort_keys=True, indent=4)
    print("Finish transformation")

#s = "https://www.allrecipes.com/recipe/166101/apricot-chicken-with-balsamic-vinegar/"
if __name__ == '__main__':
    to_thai()
    
