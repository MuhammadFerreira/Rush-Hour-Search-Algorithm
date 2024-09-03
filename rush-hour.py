from AStar import AStar
import pandas as pd
from GBFS import GBFS
from UCS import UCS
import time
from Node import Node
from heuritics import *
from gameMechanics import *
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

#Dataframe to store the results
df = pd.DataFrame(columns=['Puzzle Number', 'Algorithm', 'Heuristic', 'Length of the Solution', 'Length of the Search Path', ' Execution Time (in seconds)'])

#Function to print the results of the search
def printResults(gameNumber, searchType, line, resultNode, runTime, initialFuelLevels):
    #Print the solution to a new file
    f = open(r"C:\Users\Hamzah\Projects\COMP472-MP2\results\\"+str(searchType)+"-sol-"+str(gameNumber)+".txt", 'w')
    f.write("--------------------------------------------------------------------------------\n\n")
    f.write("Initial board configuration: " + line + "\n")

    #Get string after 36 characters
    f.write("!" + line[36:])
    f.write(gameMechanics.printBoard(line[0:36]))
    f.write("\nCar fuel available: " + str(initialFuelLevels) + "\n\n")

    if resultNode[0] == None:
        f.write("\nSorry, could not solve the puzzle as specified.\nError: no solution found. \n")
        f.write("\nRuntime: " + str(runTime) + " seconds\n")
        f.write("--------------------------------------------------------------------------------")
        f.close()
        return


    ansNode = copy.deepcopy(resultNode[0])

    solutionPath = []
    pathMoves = []
    pathFuel = []
    pathLength = len(resultNode[1])
    while ansNode != None:
        solutionPath.append(ansNode.game)
        pathMoves.append(ansNode.changeFromParent)
        pathFuel.append(ansNode.currentFuel)
        ansNode = ansNode.parent

    f.write("Runtime: " + str(runTime) + " seconds\n")
    f.write("Search Path Length: " + str(pathLength) + " states\n")
    f.write("Solution Path Length: " + str(resultNode[0].depth) + " moves\n")
    f.write("Solution Path: ".replace('\n',''))
    for x in reversed(pathMoves):
        if x == "Initial State":
            continue
        f.write((x + ", ").replace('\n',''))
    f.write("\n\n")
    
    for move, fuel, game in zip(reversed(pathMoves), reversed(pathFuel), reversed(solutionPath)):

        if move == "Initial State":
            continue

        f.write((move + "\t" + str(fuel[move[0]]) + "\t" + gameMechanics.reconvert(game) + "\t").replace('\n',''))

        #print values in hash table for fuel levels only if they are not 100
        for key, value in fuel.items():
            if value != 100:
                f.write((key + ":" + str(value) + " ").replace('\n','')) 
        f.write("\n")
    f.write("\n! ")
    
    for key, value in pathFuel[0].items():
        if value != 100:
            f.write((key + str(value) + " ").replace('\n','')) 
    f.write("\n")
    f.write(gameMechanics.printBoard(gameMechanics.reconvert(solutionPath[0])))
    f.write("\n\n--------------------------------------------------------------------------------\n\n")

    f.close()

#Funtction to print the results of the search
def printSearch(gameNumber, searchType, resultNode):
    #Print the solution to a new file
    f = open(r"C:\Users\Hamzah\Projects\COMP472-MP2\results\\"+str(searchType)+"-search-"+str(gameNumber)+".txt", 'w')
    
    
    for x in resultNode[1]:
        if searchType == "ucs":
            f.write(str(0) + " " + str(x.depth) + " " + str(0) + " " + gameMechanics.reconvert(x.game) + "\n")
        if "gbfs" in searchType:
            f.write(str(0) + " " + str(0) + " " + str(x.heuristicValue) + " " + gameMechanics.reconvert(x.game) + "\n")
        if "a" in searchType:
            f.write(str(x.fValue) + " " + str(x.depth) + " " + str(x.heuristicValue) + " " + gameMechanics.reconvert(x.game) + "\n")
    
    f.close()

#Time to run the program
start_time = time.time()


#Open file
f = open(r"C:\Users\Hamzah\Projects\COMP472-MP2\Sample\sample-input.txt", 'r')

#Read lines in file
lines = f.readlines()

#Close file
f.close()

gameNumber = 1

#Cycle through each line
for line in lines:
    
    #Skip empty lines or lines starting with #
    if line.strip() == '' or line[0] == '#':
        continue

    print("Game Number: " + str(gameNumber))

    mechanics = gameMechanics(line.strip())

    #Perform Uniform Cost Search
    start = time.time()
    ucs = UCS.search(line)
    end = time.time()

    ucsRunTime = round(end - start, 2)

    #add results to dataframe
    try:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'UCS', 'Heuristic': 'N/A', 'Length of the Solution': ucs[0].depth, 'Length of the Search Path': len(ucs[1]), ' Execution Time (in seconds)': ucsRunTime}, ignore_index=True)
    except:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'UCS', 'Heuristic': 'N/A', 'Length of the Solution': 'N/A', 'Length of the Search Path': len(ucs[1]), ' Execution Time (in seconds)': ucsRunTime}, ignore_index=True)
    

    #Print results to file
    printResults(gameNumber, "ucs", line, ucs, ucsRunTime, mechanics.intialFuelLevels)
    printSearch(gameNumber, "ucs", ucs)

    #Perform Greedy Best First Search with heuristic 1
    start = time.time()
    gbfsH1 = GBFS.search(line, heuristic1)
    end = time.time()

    gbfsRunTimeH1 = round(end - start, 2)

    #add results to dataframe
    try:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'GBFS', 'Heuristic': 'Heuristic 1', 'Length of the Solution': gbfsH1[0].depth, 'Length of the Search Path': len(gbfsH1[1]), ' Execution Time (in seconds)': gbfsRunTimeH1}, ignore_index=True)
    except:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'GBFS', 'Heuristic': 'Heuristic 1', 'Length of the Solution': 'N/A', 'Length of the Search Path': len(gbfsH1[1]), ' Execution Time (in seconds)': gbfsRunTimeH1}, ignore_index=True)

    #Print results to file
    printResults(gameNumber, "gbfs-h1", line, gbfsH1, gbfsRunTimeH1, mechanics.intialFuelLevels)
    printSearch(gameNumber, "gbfs-h1", gbfsH1)

    #Perform Greedy Best First Search with heuristic 2
    start = time.time()
    gbfsH2 = GBFS.search(line, heuristic2)
    end = time.time()

    gbfsRunTimeH2 = round(end - start, 2)

    #add results to dataframe
    try:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'GBFS', 'Heuristic': 'Heuristic 2', 'Length of the Solution': gbfsH2[0].depth, 'Length of the Search Path': len(gbfsH2[1]), ' Execution Time (in seconds)': gbfsRunTimeH2}, ignore_index=True)
    except:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'GBFS', 'Heuristic': 'Heuristic 2', 'Length of the Solution': 'N/A', 'Length of the Search Path': len(gbfsH2[1]), ' Execution Time (in seconds)': gbfsRunTimeH2}, ignore_index=True)

    #Print results to file
    printResults(gameNumber, "gbfs-h2", line, gbfsH2, gbfsRunTimeH2, mechanics.intialFuelLevels)
    printSearch(gameNumber, "gbfs-h2", gbfsH2)

    #Perform Greedy Best First Search with heuristic 3
    start = time.time()
    gbfsH3 = GBFS.search(line, heuristic3)
    end = time.time()

    gbfsRunTimeH3 = round(end - start, 2)

    #add results to dataframe
    try:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'GBFS', 'Heuristic': 'Heuristic 3', 'Length of the Solution': gbfsH3[0].depth, 'Length of the Search Path': len(gbfsH3[1]), ' Execution Time (in seconds)': gbfsRunTimeH3}, ignore_index=True)
    except:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'GBFS', 'Heuristic': 'Heuristic 3', 'Length of the Solution': 'N/A', 'Length of the Search Path': len(gbfsH3[1]), ' Execution Time (in seconds)': gbfsRunTimeH3}, ignore_index=True)

    #Print results to file
    printResults(gameNumber, "gbfs-h3", line, gbfsH3, gbfsRunTimeH3, mechanics.intialFuelLevels)
    printSearch(gameNumber, "gbfs-h3", gbfsH3)

    #Perform Greedy Best First Search with heuristic 4
    start = time.time()
    gbfsH4 = GBFS.search(line, heuristic4)
    end = time.time()

    gbfsRunTimeH4 = round(end - start, 2)

    #add results to dataframe
    try:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'GBFS', 'Heuristic': 'Heuristic 4', 'Length of the Solution': gbfsH4[0].depth, 'Length of the Search Path': len(gbfsH4[1]), ' Execution Time (in seconds)': gbfsRunTimeH4}, ignore_index=True)
    except:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'GBFS', 'Heuristic': 'Heuristic 4', 'Length of the Solution': 'N/A', 'Length of the Search Path': len(gbfsH4[1]), ' Execution Time (in seconds)': gbfsRunTimeH4}, ignore_index=True)

    #Print results to file
    printResults(gameNumber, "gbfs-h4", line, gbfsH4, gbfsRunTimeH4, mechanics.intialFuelLevels)
    printSearch(gameNumber, "gbfs-h4", gbfsH4)


    #Perform A* Search with heuristic 1
    start = time.time()
    aStarH1 = AStar.search(line, heuristic1)
    end = time.time()

    aStarRunTimeH1 = round(end - start, 2)

    #add results to dataframe
    try:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'A*', 'Heuristic': 'Heuristic 1', 'Length of the Solution': aStarH1[0].depth, 'Length of the Search Path': len(aStarH1[1]), ' Execution Time (in seconds)': aStarRunTimeH1}, ignore_index=True)
    except:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'A*', 'Heuristic': 'Heuristic 1', 'Length of the Solution': 'N/A', 'Length of the Search Path': len(aStarH1[1]), ' Execution Time (in seconds)': aStarRunTimeH1}, ignore_index=True)

    #Print results to file
    printResults(gameNumber, "a-h1", line, aStarH1, aStarRunTimeH1, mechanics.intialFuelLevels)
    printSearch(gameNumber, "a-h1", aStarH1)

    #Perform A* Search with heuristic 2
    start = time.time()
    aStarH2 = AStar.search(line, heuristic2)
    end = time.time()

    aStarRunTimeH2 = round(end - start, 2)

    #add results to dataframe
    try:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'A*', 'Heuristic': 'Heuristic 2', 'Length of the Solution': aStarH2[0].depth, 'Length of the Search Path': len(aStarH2[1]), ' Execution Time (in seconds)': aStarRunTimeH2}, ignore_index=True)
    except:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'A*', 'Heuristic': 'Heuristic 2', 'Length of the Solution': 'N/A', 'Length of the Search Path': len(aStarH2[1]), ' Execution Time (in seconds)': aStarRunTimeH2}, ignore_index=True)

    #Print results to file
    printResults(gameNumber, "a-h2", line, aStarH2, aStarRunTimeH2, mechanics.intialFuelLevels)
    printSearch(gameNumber, "a-h2", aStarH2)

    #Perform A* Search with heuristic 3
    start = time.time()
    aStarH3 = AStar.search(line, heuristic3)
    end = time.time()

    aStarRunTimeH3 = round(end - start, 2)

    #add results to dataframe
    try:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'A*', 'Heuristic': 'Heuristic 3', 'Length of the Solution': aStarH3[0].depth, 'Length of the Search Path': len(aStarH3[1]), ' Execution Time (in seconds)': aStarRunTimeH3}, ignore_index=True)
    except:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'A*', 'Heuristic': 'Heuristic 3', 'Length of the Solution': 'N/A', 'Length of the Search Path': len(aStarH3[1]), ' Execution Time (in seconds)': aStarRunTimeH3}, ignore_index=True)

    #Print results to file
    printResults(gameNumber, "a-h3", line, aStarH3, aStarRunTimeH3, mechanics.intialFuelLevels)
    printSearch(gameNumber, "a-h3", aStarH3)

    #Perform A* Search with heuristic 4
    start = time.time()
    aStarH4 = AStar.search(line, heuristic4)
    end = time.time()

    aStarRunTimeH4 = round(end - start, 2)

    #add results to dataframe
    try:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'A*', 'Heuristic': 'Heuristic 4', 'Length of the Solution': aStarH4[0].depth, 'Length of the Search Path': len(aStarH4[1]), ' Execution Time (in seconds)': aStarRunTimeH4}, ignore_index=True)
    except:
        df = df.append({'Puzzle Number': gameNumber, 'Algorithm': 'A*', 'Heuristic': 'Heuristic 4', 'Length of the Solution': 'N/A', 'Length of the Search Path': len(aStarH4[1]), ' Execution Time (in seconds)': aStarRunTimeH4}, ignore_index=True)

    #Print results to file
    printResults(gameNumber, "a-h4", line, aStarH4, aStarRunTimeH4, mechanics.intialFuelLevels)
    printSearch(gameNumber, "a-h4", aStarH4)

    gameNumber += 1

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter("MP2results2.xlsx", engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Results')

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Results']

# Set the column width and format.
worksheet.set_column(1, 1, 30)

# Close the Pandas Excel writer and output the Excel file.
writer.save()

end_time = time.time()

print("Total time: " + str(round(end_time - start_time, 2)) + " seconds")
    




    
    


    

  
    








