#!/usr/bin/env python3.7

import sys

# Import recipies data set frm JSON file
import json
with open("recipes.json", 'r') as f:
	recipes = json.load(f)

output = set()
if len(sys.argv) < 2:
	print("Usage: ./findIngredient <skillLevel>")
else:
	skill = int(sys.argv[1])
	for ingredient, info in recipes.items():
		if info["Learn"] <= skill and info["Yellow"] > skill:
			output.add(ingredient)

	# Print results
	outputSortedList = sorted(output)	
	print("Ingredients that can give you skill at level " + str(skill) + ":")
	print("\n".join(outputSortedList))
