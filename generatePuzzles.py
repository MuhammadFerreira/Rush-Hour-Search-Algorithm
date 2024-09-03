import urllib.request
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

uf = urllib.request.urlopen("https://www.thinkfun.com/wp-content/themes/thinkfun/rush-hour-challenges/data.json")
html = uf.read()

#turn the html into a JSON array
import json
data = json.loads(html)

#pick a random puzzle
import random

puzzles = []

while len(puzzles) < 10:
    puzzle = random.choice(data)
    if puzzle not in puzzles and puzzle['moves'] <= 5:
        puzzles.append(puzzle)

while len(puzzles) < 20:
    puzzle = random.choice(data)
    if puzzle not in puzzles and puzzle['moves'] <= 10:
        puzzles.append(puzzle)

while len(puzzles) < 30:
    puzzle = random.choice(data)
    if puzzle not in puzzles and puzzle['moves'] <= 20:
        puzzles.append(puzzle)

while len(puzzles) < 40:
    puzzle = random.choice(data)
    if puzzle not in puzzles and puzzle['moves'] <= 30:
        puzzles.append(puzzle)

while len(puzzles) < 50:
    puzzle = random.choice(data)
    if puzzle not in puzzles and puzzle['moves'] > 30:
        puzzles.append(puzzle)


#for each puzzle by replacing A with X, X with A and - with .
for puzzle in puzzles:
    puzzle['challenge'] = puzzle['challenge'].replace('X', '1')
    puzzle['challenge'] = puzzle['challenge'].replace('A', 'X')
    puzzle['challenge'] = puzzle['challenge'].replace('1', 'A')
    puzzle['challenge'] = puzzle['challenge'].replace('X', 'X')
    puzzle['challenge'] = puzzle['challenge'].replace('-', '.')

    #30% chance of having fuel levels
    if random.randint(0, 100) < 30:
        #count the number of unique characters in the puzzle that is not a .
        unique = set(puzzle['challenge'])
        unique.discard('.')

        #count unique characters
        count = len(unique)

        #pick a random number from 1 to the number of unique characters
        numberOfFuelLevels = random.randint(1, count)

        #Select numberOfFuelLevels unique random characters from the puzzle
        fuelLevels = random.sample(unique, numberOfFuelLevels)

        #for each fuel level, pick a random number from 1 to 100
        for fuelLevel in fuelLevels:
            puzzle['challenge'] = puzzle['challenge'] + " " + fuelLevel + str(random.randint(1, 100))

        


#print the puzzles into a file
with open('puzzlesNew.txt', 'w') as f:

    f.write("#\n# 50 Random Rush-Hour Puzzles\n#\n\n")

    for num, puzzle in enumerate(puzzles):
        f.write("# Puzzle " + str(num+1) + "\n")
        f.write(puzzle['challenge'])
        f.write('\n\n')

