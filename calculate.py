#!/usr/bin/env python3.7

# =============================================================================
# ========== User additions below this line ===================================
# =============================================================================

# Enter starting cooking skill
skillLevel = 1

# List amount of available ingredients
ingredients = {
    "Bear Meat":                    40,
    "Big Bear Meat":                0,
    "Boar Ribs":                    0,
    "Buzzard Wing":                 0,
    "Chunk of Boar Meat":           50,
    "Clam Meat":                    20,
    "Coyote Meat":                  0,
    "Crawler Meat":                 0,
    "Darkclaw Lobster":             0,
    "Lean Wolf Flank":              0,
    "Lion Meat":                    0,
    "Meaty Bat Wing":               20,
    "Mystery Meat":                 0,
    "Raptor Egg":                   0,
    "Raptor Flesh":                 0,
    "Raw Brilliant Smallfish":      0,
    "Raw Bristle Whisker Catfish":  0,
    "Raw Glossy Mightfish":         0,
    "Raw Greater Sagefish":         0,
    "Raw Longjaw Mud Snapper":      0,
    "Raw Mithril Head Trout":       0,
    "Raw Nightfin Snapper":         0,
    "Raw Rainbow Fin Albacore":     0,
    "Raw Redgill":                  0,
    "Raw Rockscale Cod":            0,
    "Raw Sagefish":                 0,
    "Raw Spotted Yellowtail":       0,
    "Raw Summer Bass":              0,
    "Raw Sunscale Salmon":          0,
    "Raw Whitescale Salmon":        0,
    "Red Wolf Meat":                0,
    "Sandworm Meat":                0,
    "Scorpid Stinger":              0,
    "Small Egg":                    0,
    "Stag Meat":                    0,
    "Strider Meat":                 0,
    "Stringy Wolf Meat":            0,
    "Tangy Clam Meat":              0,
    "Tender Crab Meat":             0,
    "Tender Crocolisk Meat":        0,
    "Tender Wolf Meat":             0,
    "Thunder Lizard Tail":          0,
    "Turtle Meat":                  0,
    "Tiger Meat":                   0,
    "White Spider Meat":            0,
    "Zesty Clam Meat":              0
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

    # "Announce" the craft
    outputFile.write(str(skillLevel) + ": " + recipes[candidate]["Recipe"] + " (" + str(candidate) + ")\n")

    # Add recipe name to set of used recipes
    usedRecipies.add(recipes[candidate]["Recipe"])

    # Add the used ingredient to the count
    sumIngredients(candidate, recipes[candidate]["Amount"])

    # Add additional mats to the total sum
    sumAddMats(usedAddMats, recipes[candidate]["AddMats"])

    # Increment current skill level
    skillLevel += 1

    # "Consume" the ingredient
    ingredients[candidate] = ingredients[candidate]-recipes[candidate]["Amount"] 

# Announce final skill level reached
outputFile.write("\nSkill reached: " + str(skillLevel))

## Announce list of recipes used
outputFile.write("\n\nRecipes required:\n")
outputFile.write("\n".join(usedRecipies))

outputFile.write("\n\nIngredients used:\n")
printDict(usedIngredients)

# Announce additional mats used
outputFile.write("\n\nAdditional mats required:\n")
printDict(usedAddMats)
outputFile.write("\n")

# Close output file
outputFile.close()