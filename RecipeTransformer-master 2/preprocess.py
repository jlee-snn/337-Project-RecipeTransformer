import json

IMPORTANT_NUTRIENTS = [
  "Energy",
  "Total lipid (fat)",
  "Carbohydrate, by difference",
  "Protien",
  "Water",
  "Sodium, Na",
  "Fiber, total dietary",
  "Starch"
]

IGNORED_GROUPS = [
  "Fast Foods",
  "Ethnic Foods",
  "Restaurant Foods",
  "Baby Foods",
  "Meals, Entrees, and Sidedishes"
]

with open("food-data.json", "r") as f:
    data = json.loads(f.read())

output = []

for item in data:
    if (item["group"] not in IGNORED_GROUPS) and (len(item["portions"]) != 0):
        food = {}
        food["description"] = item["description"]
        food["group"] = item["group"]
        food["portions"] = [item["portions"][0]]
        nutrients = [n for n in item["nutrients"] if n["description"] in IMPORTANT_NUTRIENTS and n["units"] in ["g", "mg"]]
        food["nutrients"] = nutrients
        output.append(food)

open("processed-food-data.json", "w").write(json.dumps(output, indent=4))
