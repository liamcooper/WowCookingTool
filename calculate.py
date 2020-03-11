#!/usr/bin/env python3.7

# =============================================================================
# ========== User additions below this line ===================================
# =============================================================================

# Enter starting cooking skill
skillLevel = 1

# List amount of available ingredients
ingredients = {
    "Bear Meat":                    0,
    "Big Bear Meat":                40,
    "Boar Ribs":                    0,
    "Buzzard Wing":                 10,
    "Chunk of Boar Meat":           34,
    "Clam Meat":                    31,
    "Coyote Meat":                  0,
    "Crawler Meat":                 11,
    "Darkclaw Lobster":             0,
    "Giant Egg":                    125,
    "Kodo Meat":                    2,
    "Lean Wolf Flank":              100,
    "Lion Meat":                    21,
    "Meaty Bat Wing":               33,
    "Mystery Meat":                 88,
    "Raptor Egg":                   10,
    "Raptor Flesh":                 0,
    "Raw Brilliant Smallfish":      0,
    "Raw Bristle Whisker Catfish":  9,
    "Raw Glossy Mightfish":         0,
    "Raw Greater Sagefish":         0,
    "Raw Longjaw Mud Snapper":      0,
    "Raw Mithril Head Trout":       0,
    "Raw Nightfin Snapper":         0,
    "Raw Rainbow Fin Albacore":     4,
    "Raw Redgill":                  0,
    "Raw Rockscale Cod":            13,
    "Raw Sagefish":                 0,
    "Raw Spotted Yellowtail":       60,
    "Raw Summer Bass":              0,
    "Raw Sunscale Salmon":          0,
    "Raw Whitescale Salmon":        0,
    "Red Wolf Meat":                112,
    "Sandworm Meat":                0,
    "Scorpid Stinger":              22,
    "Small Egg":                    4,
    "Stag Meat":                    2,
    "Strider Meat":                 23,
    "Stringy Wolf Meat":            23,
    "Tangy Clam Meat":              78,
    "Tender Crab Meat":             10,
    "Tender Crocolisk Meat":        39,
    "Tender Wolf Meat":             8,
    "Thunder Lizard Tail":          14,
    "Turtle Meat":                  24,
    "Tiger Meat":                   6,
    "White Spider Meat":            9,
    "Zesty Clam Meat":              64
}
# =============================================================================
# ========== User additions above this line ===================================
# =============================================================================

# Import recipies data set frm JSON file
import json
with open("recipes.json", 'r') as f:
    recipes = json.load(f)

# Open output file for writing
outputFile = open("output.txt", 'w')

# Placeholders for adding information to during processing
usedRecipies = set()
usedIngredients = dict()
usedAddMats = dict()
outputDict = dict()

def findNextCraft(ingredients, recipes, currentSkill):
    temp = dict()
    # Iterate over the recipe dictionary
    for ingredient, info in recipes.items():
        # If at the current skill level the recipe can be learned but has
        # not yet turned yellow
        if info["Learn"] <= skillLevel and info["Yellow"] >= currentSkill:
            # Store recipe in "temp" dictionary
            temp[ingredient] = info

    candidateSkill = 999     # arbitrary large number
    candidateName = None

    # Iterate over "temp" dictionary
    for ingredient, info in temp.items():
        # If recipe turns yellow earlier than the current candidate
        if info["Yellow"] < candidateSkill:
            # If there's enough ingredient left for at least one craft
            if ingredients[ingredient] >= info["Amount"]:
                candidateSkill = info["Yellow"]
                candidateName = ingredient

    return candidateName

def printDict(dictName):
    for key, value in dictName.items():
        outputFile.write(str(key) + ": " + str(value) + "\n")
    return

def storeOutput(ingredient, recipes, currentSkill):
    # Check if this is the first item to be added (dictionary empty)
    if not bool(outputDict):
        # Add item at the start
        outputDict[1] =  {"Start": currentSkill, "Count": 1, "Recipe": recipes[ingredient]["Recipe"], "Ingredient": ingredient}
    else:
        lastCraft = list(outputDict.keys())[-1]
        #lastCraft = list(reversed(list(outputDict)))[0]
        if outputDict[lastCraft]["Ingredient"] == ingredient:
            # Increment count
            outputDict[lastCraft]["Count"] += 1
        else:
            # Add new post to output
            outputDict[lastCraft+1] =  {"Start": currentSkill, "Count": 1, "Recipe": recipes[ingredient]["Recipe"], "Ingredient": ingredient}
    return

def sumAddMats(listOfMats, listOfMatsToAdd):
    # Loop oven items to be added
    for key, value in listOfMatsToAdd.items():
        # If the item already exists
        if key in listOfMats:
            # Sum the existing and added amounts
            listOfMats[key] += listOfMatsToAdd[key]
        else:
            # Else add the new item
            listOfMats[key] = value
    return

def sumIngredients(ingredient, amount):
    if ingredient in usedIngredients:
        usedIngredients[ingredient] += amount
    else:
        usedIngredients[ingredient] = amount
    return

# Iterate as long as there are relevant recipes left
while True:
    # Exit loop if list of recipes to craft is empty
    if not recipes:
        break

    # Remove unavailable ingredients
    ingredients = dict([(k,v) for k,v in ingredients.items() if v != 0])

    # Remove recipes there's no ingredients for
    temp = recipes.copy()
    for key in temp.keys():
        if key not in ingredients:
            recipes.pop(key)

    # Remove recipes that have been outlevelled
    temp = recipes.copy()
    for ingredient, info in temp.items():
        if info["Yellow"] <= skillLevel:
            recipes.pop(ingredient)

    # Determine next suitable craft
    candidate = findNextCraft(ingredients, recipes, skillLevel)

    # Exit loop if no suitable crafts exist
    if not candidate:
        break

    # Store output
    storeOutput(candidate, recipes, skillLevel)

    # Add recipe name to set of used recipes if it isn't learned at a trainer
    if recipes[candidate]["Source"] == "Recipe":
        usedRecipies.add(recipes[candidate]["Recipe"])

    # Add the used ingredient to the count
    sumIngredients(candidate, recipes[candidate]["Amount"])

    # Add additional mats to the total sum
    sumAddMats(usedAddMats, recipes[candidate]["AddMats"])

    # Increment current skill level
    skillLevel += 1

    # "Consume" the ingredient
    ingredients[candidate] = ingredients[candidate]-recipes[candidate]["Amount"] 

# Print guide
for key, value in outputDict.items():
    outputFile.write(str(key) + ": Skill " + str(value["Start"]) + "->" + str(value["Start"] + value["Count"]) + " craft " + str(value["Recipe"]) + " (" + str(value["Ingredient"]) + ")\n")

# Announce final skill level reached
outputFile.write("\nSkill reached: " + str(skillLevel))

# Announce list of recipes used
outputFile.write("\n\nRecipes required:\n")
outputFile.write("\n".join(sorted(usedRecipies)))

# Announce ingredients used
outputFile.write("\n\nIngredients used:\n")
printDict(usedIngredients)

# Announce additional mats used
outputFile.write("\nAdditional mats required:\n")
printDict(usedAddMats)
outputFile.write("\n")

# Close output file
outputFile.close()

