from parser.RecipeParse import RecipeParse
import json
import math
import sys

ALL_FOOD_GROUPS = [
    "Dairy and Egg Products",
    "Spices and Herbs",
    "Baby Foods",
    "Fats and Oils",
    "Poultry Products",
    "Soups, Sauces, and Gravies",
    "Sausages and Luncheon Meats",
    "Breakfast Cereals",
    "Fruits and Fruit Juices",
    "Pork Products",
    "Vegetables and Vegetable Products",
    "Nut and Seed Products",
    "Beef Products",
    "Beverages",
    "Finfish and Shellfish Products",
    "Legumes and Legume Products",
    "Lamb, Veal, and Game Products",
    "Baked Products",
    "Snacks",
    "Sweets",
    "Cereal Grains and Pasta",
    "Fast Foods",
    "Meals, Entrees, and Sidedishes",
    "Ethnic Foods",
    "Restaurant Foods",
]

DONT_INCLUDE_GROUPS = [
	"Spices and Herbs",
	"Baby Foods",
	"Breakfast Cereals",
	"Beverages",
	"Snacks",
	"Fast Foods",
	"Meals, Entrees, and Sidedishes",
	"Ethnic Foods",
	"Restaurant Foods",
	"Dairy and Egg Products",
	"Baked Products"
]

NON_VEGETARIAN_GROUPS = [
    "Sausages and Luncheon Meats",
    "Pork Products",
    "Beef Products",
    "Finfish and Shellfish Products",
    "Lamb, Veal, and Game Products",
    "Poultry Products",
    "Ethnic Foods"
]

NON_PESCETARIAN_GROUPS = [
    "Sausages and Luncheon Meats",
    "Pork Products",
    "Beef Products",
    "Lamb, Veal, and Game Products",
    "Poultry Products",
    "Ethnic Foods"
]

MEAT_AND_FISH_GROUPS = [
    "Sausages and Luncheon Meats",
    "Pork Products",
    "Beef Products",
    "Finfish and Shellfish Products",
    "Lamb, Veal, and Game Products",
]

PRIMARY_COOKING_METHODS = [
	"bake",
	"steam",
	"grill",
	"roast",
	"boil",
	"fry",
	"barbeque",
	"baste",
	"broil",
	"poach",
	"freeze",
	"cure",
	"saute"
]

SECONDARY_COOKING_METHODS = [
	"chop",
	"grate",
	"cut",
	"shake",
	"mince",
	"stir",
	"mix",
	"crush",
	"squeeze",
	"beat",
	"blend",
	"caramelize",
	"dice",
	"dust",
	"glaze",
	"knead",
	"pare",
	"shred",
	"toss",
	"whip",
	"sprinkle",
	"grease",
	"arrange",
	"microwave",
	"coat",
	"turning",
	"preheat",
	"broil"
]

TOOLS = ['pan', 'bowl', 'baster', 'knife', 'oven', 'beanpot', 'chip pan', 'cookie sheet', 'cooking pot', 'crepe pan', 'double boiler', 'doufeu', 'dutch oven', 'food processor', 'frying pan', 'skillet', 'griddle', 'karahi', 'kettle', 'pan', 'pressure cooker', 'ramekin', 'roasting pan', 'roasting rack', 'saucepansauciersaute pan', 'splayed saute pan', 'souffle dish', 'springform pan', 'stockpot', 'tajine', 'tube panwok', 'wonder pot', 'pot', 'apple corer', 'apple cutter', 'baster', 'biscuit cutter', 'biscuit press', 'bowl', 'bread knife', 'browning tray', 'butter curler', 'cake and pie server', 'cheese knife', 'cheesecloth', 'knife', 'cherry pitter', 'chinoise', 'cleaver', 'corkscrew', 'cutting board', 'dough scraper', 'egg poacher', 'egg separator', 'egg slicer', 'egg timer', 'fillet knife', 'fish scaler', 'fish slice', 'flour sifter', 'food mill', 'funnel', 'garlic press', 'grapefruit knife', 'grater', 'gravy strainer', 'ladle', 'lame', 'lemon reamer', 'lemon squeezer', 'mandoline', 'mated colander pot', 'measuring cup', 'measuring spoon', 'grinder', 'tenderiser', 'thermometer', 'melon baller', 'mortar and pestle', 'nutcracker', 'nutmeg grater,oven glove', 'blender', 'fryer', 'pastry bush', 'pastry wheel', 'peeler', 'pepper mill', 'pizza cutter', 'masher', 'potato ricer', 'pot-holder', 'rolling pin', 'salt shaker', 'sieve', 'spoon', 'fork', 'spatula', 'spider', 'tin opener', 'tongs', 'whisk', 'wooden spoon', 'zester', 'microwave']

def filter_food_groups(recipe_in, groups):
    """
    Takes a recipe url and a list of food groups to avoid, replaces ingredients
    in the ingredient list with suitable alternatives not in the banned groups
    """
    with open("food-data.json", "r") as f:
        print "Loading data from food-data.json"
        food_data = json.loads(f.read())
	recipe = recipe_in
    subs = {}
    recipe["primary cooking method"] = "none"
    recipe["cooking methods"] = []
    recipe["cooking tools"] = []
    clean_steps = []
    for instruction in recipe['steps']:
    	if instruction.strip() != "":
    		instruction_tokens = instruction.lower().replace(',','').split()
    		matches1 = [itm for itm in instruction_tokens if itm in PRIMARY_COOKING_METHODS]
    		matches2 = [itm for itm in instruction_tokens if itm in SECONDARY_COOKING_METHODS]
    		matches3 = [itm for itm in instruction_tokens if itm in TOOLS]
    		if len(matches1) > 0:
    			recipe["primary cooking method"] = matches1[0]
    		if len(matches2) > 0:
    			recipe["cooking methods"] = recipe["cooking methods"] + matches2
    		if len(matches3) > 0:
    			recipe["cooking tools"] = recipe["cooking tools"] + matches3
    		clean_steps.append(instruction.strip())
    recipe['steps'] = clean_steps
    for ingredient in recipe["ingredients"]:
        nut_info = resolve_ingredient(ingredient["name"], food_data)
        if nut_info[u'group'] in groups:
            print "Attempting to replace:", nut_info[u'description']
            print "Group: " + nut_info[u'group']
            replacement = find_similar_food(nut_info, groups, food_data)
            print "Replacing with: ", replacement[u'description']
            print "Group: " + replacement[u'group']
            subs[ingredient["name"]] = replacement[u'description']
    for ingredient in recipe["ingredients"]:
        if ingredient["name"] in subs:
            ingredient["name"] = subs[ingredient["name"]]
    return recipe

def to_vegetarian(recipe):
    return filter_food_groups(recipe, NON_VEGETARIAN_GROUPS)

def to_pescetarian(recipe):
    return filter_food_groups(recipe, NON_PESCETARIAN_GROUPS)

def remove_unhealthy(recipe_in, nutrient_name):
    """
    Removes ingredient in recipe with highest amounts of specified
    ingredients, replaces them with similar foods that are healthier
    """

    with open("processed-food-data.json", "r") as f:
        "Loading food data...."
        food_data = json.loads(f.read())

    recipe = recipe_in
    subs = {}
    clean_steps = []
    recipe["primary cooking method"] = "none"
    recipe["cooking methods"] = []
    recipe["cooking tools"] = []
    for instruction in recipe["steps"]:
    	if instruction.strip() != "":
    		instruction_tokens = instruction.lower().replace(',','').split()
    		matches1 = [itm for itm in instruction_tokens if itm in PRIMARY_COOKING_METHODS]
    		matches2 = [itm for itm in instruction_tokens if itm in SECONDARY_COOKING_METHODS]
    		matches3 = [itm for itm in instruction_tokens if itm in TOOLS]
    		if len(matches1) > 0:
    			recipe["primary cooking method"] = matches1[0]
    		if len(matches2) > 0:
    			recipe["cooking methods"] = recipe["cooking methods"] + matches2
    		if len(matches3) > 0:
    			recipe["cooking tools"] = recipe["cooking tools"] + matches3
    		clean_steps.append(instruction.strip())
    recipe['steps'] = clean_steps
    highest_amount = float("-inf")
    nutrient = {}
    ingredient_name = ""

    for ingredient in recipe["ingredients"]:
        nut_info = resolve_ingredient(ingredient["name"], food_data)
        amnt = get_amount_of_nutrient(nut_info, nutrient_name, "g")
        if nut_info[u'group'] not in DONT_INCLUDE_GROUPS:
        	if amnt > highest_amount:
        	    highest_amount = amnt
        	    nutrient = nut_info
        	    ingredient_name = ingredient["name"]
    print "Attempting to replace: ", nutrient[u'description']
    print "Group: ", nutrient['group']
    print "Nutrient content: ", highest_amount

    replacement = find_healthier_food(nutrient, nutrient_name, highest_amount, food_data)
    print "Replacing with:", replacement[u'description']
    print "Group: " + replacement['group']
    print "Nutrient Content: ", get_amount_of_nutrient(replacement, nutrient_name, "g")
    subs[ingredient_name] = replacement[u'description']

    for ingredient in recipe["ingredients"]:
        if ingredient["name"] in subs:
            ingredient["name"] = subs[ingredient["name"]]
    return recipe

def get_amount_of_nutrient(nut_info, nutrient_name, unit):
    total_nut_amount = [n for n in nut_info["nutrients"]
            if n["units"] == unit and n["description"] == nutrient_name][0]["value"]
    return total_nut_amount

def to_lowfat(recipe):
    return remove_unhealthy(recipe, u'Total lipid (fat)')

def to_low_carb(recipe):
	return remove_unhealthy(recipe, u'Carbohydrate, by difference')

def resolve_ingredient(name, data):
    """
    Takes an ingredient name (as given by our allrecipies parser), and returns a
    dict from the FDA database with the closest match for this ingredient.
    """
    name_tokens = name.lower().replace(',','').split()
    #if "pepper" in name_tokens:
    #	name_tokens = [u'pepper']
    best_match = {}
    best_match_tokens = []
    matching_words = 0
    for ingredient in data:
    	ingredient_tokens = ingredient[u'description'].lower().replace(',','').split()
    	#print ingredient_tokens
    	matches = [itm for itm in ingredient_tokens if itm in name_tokens]
    	"""
    	Figured that the best match would be the one with the shortest ingredient name length if there is
    	a conflict where two ingredients have the same number of matches.
    	"""
    	if len(matches) == matching_words:
    		if len(ingredient_tokens) < len(best_match_tokens):
    			best_match = ingredient
    			best_match_tokens = ingredient_tokens
    	if len(matches) > matching_words:
    		matching_words = len(matches)
    		best_match = ingredient
    		best_match_tokens = ingredient_tokens
    return best_match

def find_similar_food(ingredient, groups, data):
    """
    Takes an ingredient (the whole dict) and a list of banned groups, and finds
    a similar ingredient in the food database
    """
    best_distance = float("inf")
    best_match = {}
    distance = float("inf")
    for item in data:
    	if item[u'group'] not in groups:
    		if item[u'group'] not in DONT_INCLUDE_GROUPS:
    			distance = calculate_distance(ingredient, item)
            	if distance < best_distance:
                	    best_distance = distance
                	    best_match = item
    print best_distance
    return best_match

def find_healthier_food(ingredient, nutrient_name, amount, data, percent_diff_acceptable=0.2):
    """
    Finds shortest distance food with less of specified nutrient than original,
    for most food groups, also ensures we get one in the same group, but treats
    all meats the same in terms of food groups
    """
    best_distance = float("inf")
    best_match = {}

    if ingredient[u'group'] in MEAT_AND_FISH_GROUPS:
        acceptable_groups = MEAT_AND_FISH_GROUPS
    else:
        acceptable_groups = [ingredient[u'group']]


    for item in data:
        total_nut_amount = get_amount_of_nutrient(item, nutrient_name, "g")
        percent_difference = total_nut_amount - amount/ float(amount)

        if percent_difference <= percent_diff_acceptable and item["group"] in acceptable_groups:
            distance = calculate_distance(ingredient, item)
            if distance < best_distance:
                best_distance = distance
                best_match = item

    if len(best_match.keys()) == 0:
        if percent_diff_acceptable < 0.01:
            "Giving up, no healthier foods availabe"
            return ingredient
        else:
            print "Could not find better ingredient! Trying again with", percent_diff_acceptable * 0.8
            return find_healthier_food(ingredient, nutrient_name, amount, data,
                    percent_diff_acceptable * 0.8)

    return best_match

def calculate_distance(ingredient, arg_ingredient):
	"""
	Each ingredient has different numbers of nutrients, so the distance is calculated
	by only using nutrients present in both ingredients (of the first 5 nutrients).
	"""
	distance = 0.0
	ingredient_nutrients = {}
	arg_ingredient_nutrients = {}
	for i in range(0, 4):
		ingredient_nutrients[ingredient[u'nutrients'][i][u'description']] = ingredient[u'nutrients'][i][u'value']
	for i in range(0, 4):
		arg_ingredient_nutrients[arg_ingredient[u'nutrients'][i][u'description']] = arg_ingredient[u'nutrients'][i][u'value']
	for nutrient in ingredient_nutrients.keys():
		count = 0
		if nutrient in arg_ingredient_nutrients.keys():
			count = float(ingredient_nutrients[nutrient]) - float(arg_ingredient_nutrients[nutrient])
			count = count * count
			distance = distance + count
	distance = 	float(math.sqrt(distance))
	return distance



def pretty_print_dict(dict):
    print json.dumps(dict, indent = 4)
    return

def parse_it(url):
	recipe = RecipeParse(url)
	recipe["primary cooking method"] = "none"
	recipe["cooking methods"] = []
	recipe["cooking tools"] = []
	clean_steps = []
	for instruction in recipe['steps']:
		if instruction.strip() != "":
			instruction_tokens = instruction.lower().replace(',','').split()
			matches1 = [itm for itm in instruction_tokens if itm in PRIMARY_COOKING_METHODS]
			matches2 = [itm for itm in instruction_tokens if itm in SECONDARY_COOKING_METHODS]
			matches3 = [itm for itm in instruction_tokens if itm in TOOLS]
			if len(matches1) > 0:
				recipe["primary cooking method"] = matches1[0]
			if len(matches2) > 0:
				recipe["cooking methods"] = recipe["cooking methods"] + matches2
    		if len(matches3) > 0:
    			recipe["cooking tools"] = recipe["cooking tools"] + matches3
    		clean_steps.append(instruction.strip())
	
	recipe['steps'] = clean_steps
	pretty_print_dict(recipe)
	return recipe

def to_asian(recipe_in):
	with open("food-data.json", "r") as f:
		"Loading food data...."
		food_data = json.loads(f.read())
	recipe = recipe_in
	recipe["primary cooking method"] = "none"
	recipe["cooking methods"] = []
	recipe["cooking tools"] = []
	clean_steps = []
	for instruction in recipe['steps']:
		if instruction.strip() != "":
			instruction_tokens = instruction.lower().replace(',','').split()
			matches1 = [itm for itm in instruction_tokens if itm in PRIMARY_COOKING_METHODS]
			matches2 = [itm for itm in instruction_tokens if itm in SECONDARY_COOKING_METHODS]
			matches3 = [itm for itm in instruction_tokens if itm in TOOLS]
			if len(matches1) > 0:
				recipe["primary cooking method"] = matches1[0]
			if len(matches2) > 0:
				recipe["cooking methods"] = recipe["cooking methods"] + matches2
			if len(matches3) > 0:
				recipe["cooking tools"] = recipe["cooking tools"] + matches3
			clean_steps.append(instruction.strip())
	recipe['steps'] = clean_steps
	for ingredient in recipe["ingredients"]:
		nut_info = resolve_ingredient(ingredient["name"], food_data)
		asian_sauce = resolve_ingredient("teriyaki", food_data)
		asian_spices = resolve_ingredient("ground ginger spices", food_data)
		rice = resolve_ingredient("white rice", food_data)
		if nut_info[u'group'] == "Soups, Sauces, and Gravies":
			ingredient["name"] = asian_sauce[u'description']
		if nut_info[u'group'] =="Spices and Herbs":
			ingredient["name"] = asian_spices[u'description']
		if nut_info[u'group'] == "Cereal Grains and Pasta":
			ingredient["name"] = rice[u'description']
	return recipe

def to_southern(recipe_in):
	with open("food-data.json", "r") as f:
		"Loading food data...."
		food_data = json.loads(f.read())
	recipe = recipe_in
	recipe["primary cooking method"] = "none"
	recipe["cooking methods"] = []
	recipe["cooking tools"] = []
	clean_steps = []
	for instruction in recipe['steps']:
		if instruction.strip() != "":
			instruction_tokens = instruction.lower().replace(',','').split()
			matches1 = [itm for itm in instruction_tokens if itm in PRIMARY_COOKING_METHODS]
			matches2 = [itm for itm in instruction_tokens if itm in SECONDARY_COOKING_METHODS]
			matches3 = [itm for itm in instruction_tokens if itm in TOOLS]
			if len(matches1) > 0:
				recipe["primary cooking method"] = matches1[0]
			if len(matches2) > 0:
				recipe["cooking methods"] = recipe["cooking methods"] + matches2
			if len(matches3) > 0:
				recipe["cooking tools"] = recipe["cooking tools"] + matches3
			clean_steps.append(instruction.strip())
	recipe['steps'] = clean_steps
	for ingredient in recipe["ingredients"]:
		nut_info = resolve_ingredient(ingredient["name"], food_data)
		southern_sauce = resolve_ingredient("barbeque sauce", food_data)
		southern_spices = resolve_ingredient("ground ginger spices", food_data)
		meat = resolve_ingredient("spare ribs", food_data)
		if nut_info[u'group'] == "Soups, Sauces, and Gravies":
			ingredient["name"] = southern_sauce[u'description']
		if nut_info[u'group'] in ["Sausages and Luncheon Meats", "Pork Products", "Beef Products", "Lamb, Veal, and Game Products"]:
			ingredient["name"] = meat[u'description']
	return recipe

def no_duplicates(lst):
	return list(set(lst))

def main():
	recipe = {}
	recipe = RecipeParse(sys.argv[1])
	to_choice = sys.argv[2]
	to_cuisine = sys.argv[3]
	to_health = sys.argv[4]
	if to_choice == "1":
		recipe = to_vegetarian(recipe)
	if to_choice == "2":
		recipe = to_pescetarian(recipe)
	if to_cuisine == "1":
		recipe = to_asian(recipe)
	if to_cuisine == "2":
		recipe = to_southern(recipe)
	if to_health == "1":
		recipe = to_lowfat(recipe)
	if to_health == "2":
		recipe = to_low_carb(recipe)
	print "====================================================================="
	print "Recipe Name: " + recipe["Info"]['recipe']
	print "Rating: " + recipe["Info"]['rating']
	print "====================================================================="
	print "Ingredients: "
	for dict in recipe["ingredients"]:
		print dict["name"]
	print "====================================================================="
	print "Instructions: "
	for i in range(0, len(recipe["steps"])):
		j = i + 1
		print "Step " + str(j) + ": " + recipe["steps"][i]
	print "====================================================================="
	print "Primary Cooking Method: " + recipe["primary cooking method"]
	seconds = no_duplicates(recipe["cooking methods"])
	print_seconds = ""
	for i in seconds:
		print_seconds = print_seconds + " " + str(i)
	print "Secondary Cooking Methods: " + print_seconds
	tools = no_duplicates(recipe["cooking tools"])
	print_tools = ""
	for j in tools:
		print_tools = print_tools + " " + str(j)
	print "Cooking Tools: " + print_tools
	return recipe

#main()

