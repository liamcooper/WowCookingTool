# WowCookingTool

## Introduction
Do you keep stockpiling cooking mats thinking you'll get around to level cooking on your alt at a later stage?

Do you find yourself wondering "How much cooking could I level just with all the materials I have stashed on my bank alts?"?

Then this is the tool for you!

This tool lets you enter you current cooking level and the amount of different ingredients you have available and outputs the following to a text file:
1. A step by step list of what crafts to do at each skill level
2. The maximum level achievable with the available ingredients
3. A sum of all the required recipes used in YOUR crafting sequence
4. A sum of all spices etc. required for the planned crafts

## Working principle
1. Will only plan crafts that are GUARANTEED to give you a skill up (i.e. "orange" crafts)
2. When multiple crafts are available will prioritize the recipe that will become "yellow" first

## Requirements:
1. `recipes.json` and `calculate.py` in the same folder
2. Python3 installed (written for 3.7 but should work for 3.x)

## Usage:
1. Open `calculate.py` in your text editor of choice
2. Edit `skillLevel` to indicate your current cooking level
3. Edit the `ingredients` structure to show your current stockpile of the various ingredients
4. Run `calculate.py` (e.g. `./calculate.py`)
5. The step by step guide is now available in `output.txt`