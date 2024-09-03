import copy

class gameMechanics:
    def __init__(self, initialGame):
        self.initialGame = initialGame
        self.convertedGame = self.convert(initialGame)
        self.cars = []
        self.carDirection = {}
        self.carLength = {}
        self.findDirectionAndLength(self.convertedGame)
        self.intialFuelLevels = {}
        self.getFuelLevels(initialGame)

    # Create a converter function to convert the game to 2D array
    def convert(self, game):
        #Split game into 6 character arrays
        game = [game[i:i+6] for i in range(0, 36, 6)]

        #For each item in array, split into characters array
        for i in range(len(game)):
            game[i] = list(game[i])

        return game
    
    #reconvert the game to a string
    def reconvert(game):
        gameString = ""
        for row in range(len(game)):
            for col in range(len(game[row])):
                gameString += game[row][col]
        return gameString
    
    #print string to 6X6 grid
    def printBoard(string):
        board = ""
        for i in range(0, len(string), 6):
            board += string[i:i+6]
            if i != 36:
                board += "\n"
        return board
    
    def getFuelLevels(self, game):
        #get string after 36 characters
        fuelString = game[36:]

        #Iterate through every word in the string
        for word in fuelString.split():
            #Get first character of word as key and the rest as int value
            self.intialFuelLevels[word[0]] = int(word[1:])
        
        #If the car is not in the fuel levels, set it to 100
        for car in self.cars:
            if car not in self.intialFuelLevels:
                self.intialFuelLevels[car] = 100


    #Function used to print the game
    def printGame(game):

        if game == None:
            print("No solution")
            return

        for row in range(len(game)):
            for col in range(len(game[row])):
                print(game[row][col], end=" ")
            print()

        #Function used to print the game
    def printGame(self, game):

        if game == None:
            print("No solution")
            return

        for row in range(len(game)):
            for col in range(len(game[row])):
                print(game[row][col], end=" ")
            print()

    #Find if the car is horitzontal or vertical
    def findDirectionAndLength(self, game):
        
        for row in range(len(game)):
            for col in range(len(game[row])):
                if game[row][col] != '.' and (game[row][col] not in self.cars):
                    self.cars.append(game[row][col])
                    #check if car is to the right 
                    if (col+1 <= 5) and game[row][col+1] == game[row][col]:
                        self.carDirection[game[row][col]] = 'h'
                        self.carLength[game[row][col]] = 2
                        #keep checking if car is to the right
                        x = 2
                        while (col+x <= 5) and game[row][col+x] == game[row][col]:
                            self.carLength[game[row][col]] += 1
                            x += 1
                    else:
                        self.carDirection[game[row][col]] = 'v'
                        self.carLength[game[row][col]] = 2
                        #keep checking if car is below
                        x = 2
                        while (row+x <= 5) and game[row+x][col] == game[row][col]:
                            self.carLength[game[row][col]] += 1
                            x += 1

        return self.carDirection



    #Function to move car right
    def moveRight(self, game, row, col, car):

        gameAfterMove = copy.deepcopy(game)

        if self.carDirection[car] != 'h':
            return None
        
        carBack = col
        carFront = col + self.carLength[car] - 1
                   
        #If the car is not at the right edge
        if carFront < 5 and game[row][carFront+1] == '.':
            #Move the car right
            gameAfterMove[row][carFront+1] = game[row][col]
            gameAfterMove[row][carBack] = '.'

            carBack += 1

            #Valet system to remove a horizontal car at Row 2 Col 5
            if carFront+1 == 5 and row == 2 and car != 'A':
                while carBack <= 5:
                    gameAfterMove[row][carBack] = '.'
                    carBack += 1
            return gameAfterMove  
        else:
            return None



    #Function to move car left
    def moveLeft(self, game, row, col, car):
        gameAfterMove = copy.deepcopy(game)

        if self.carDirection[car] != 'h':
            return None

        carFront = col
        carBack = col + self.carLength[car] - 1
        
                
        #If the car is not at the left edge
        if carFront > 0 and game[row][carFront-1] == '.':
                    
            #Move the car left
            gameAfterMove[row][carFront-1] = game[row][col]
            gameAfterMove[row][carBack] = '.'
            return gameAfterMove  
        else:
            return None 

    #Function to move car up
    def moveUp(self, game, row, col, car):

        gameAfterMove = copy.deepcopy(game)

        if self.carDirection[car] != 'v':
            return None
        
        carFront = row
        carBack = row + self.carLength[car] - 1

                
        #If the car is not at the top edge
        if row > 0 and game[carFront-1][col] == '.':
            #Move the car up
            gameAfterMove[carFront-1][col] = game[row][col]
            gameAfterMove[carBack][col] = '.'
            return gameAfterMove 
        else:
            return None   

    #Function to move car down
    def moveDown(self, game, row, col, car):

        gameAfterMove = copy.deepcopy(game)

        if self.carDirection[car] != 'v':
            return None
        
        carBack = row
        carFront = row + self.carLength[car] - 1

                
        #If the car is not at the bottom edge
        if carFront < 5 and game[carFront+1][col] == '.':
            #Move the car down
            gameAfterMove[carFront+1][col] = game[row][col]
            gameAfterMove[carBack][col] = '.'
            return gameAfterMove  
        else:
            return None  

    #Function to find every possible car moves from a given state and return a list of all possible states
    def findMoves(self, game, fuelLevels):
        moves = []
        direction = []
        changeInFuelLevels = []
        seenCars = []
        #Iterate through the game
        for row in range(len(game)):
            for col in range(len(game[row])):
                #If the car is not empty
                if game[row][col] != '.' and (game[row][col] not in seenCars):
                    seenCars.append(game[row][col])
                    #If the car is horizontal
                    if self.carDirection[game[row][col]] == 'h':

                        newGame = copy.deepcopy(game)
                        countMoves = 1

                        #Move the car right while it is possible
                        while self.moveRight(newGame, row, col+countMoves-1, game[row][col]) != None and countMoves <= fuelLevels[game[row][col]]:
                            newGame = self.moveRight(newGame, row, col+countMoves-1, game[row][col])
                            moves.append(newGame)
                            direction.append(str(game[row][col]) + ' Right ' + str(countMoves))

                            #copy the fuel levels
                            newFuelLevels = copy.deepcopy(fuelLevels)
                            #update the fuel levels for the car that moved
                            newFuelLevels[game[row][col]] -= countMoves
                            changeInFuelLevels.append(newFuelLevels)

                            countMoves += 1
                        
                        newGame = copy.deepcopy(game)
                        countMoves = 1
                        #Move the car left while it is possible
                        while self.moveLeft(newGame, row, col-countMoves+1, game[row][col]) != None and countMoves <= fuelLevels[game[row][col]]:
                            newGame = self.moveLeft(newGame, row, col-countMoves+1, game[row][col])
                            moves.append(newGame)
                            direction.append(str(game[row][col]) + ' Left  ' + str(countMoves))

                            #copy the fuel levels
                            newFuelLevels = copy.deepcopy(fuelLevels)
                            #update the fuel levels for the car that moved
                            newFuelLevels[game[row][col]] -= countMoves
                            changeInFuelLevels.append(newFuelLevels)

                            countMoves += 1
                        
                    #If the car is vertical
                    else:
                        newGame = copy.deepcopy(game)
                        countMoves = 1
                        #Move the car down while it is possible
                        while self.moveDown(newGame, row+countMoves-1, col, game[row][col]) != None and countMoves <= fuelLevels[game[row][col]]:
                            newGame = self.moveDown(newGame, row+countMoves-1, col, game[row][col])
                            moves.append(newGame)
                            direction.append(str(game[row][col]) + ' Down  ' + str(countMoves))

                            #copy the fuel levels
                            newFuelLevels = copy.deepcopy(fuelLevels)
                            #update the fuel levels for the car that moved
                            newFuelLevels[game[row][col]] -= countMoves
                            changeInFuelLevels.append(newFuelLevels)

                            countMoves += 1
                        
                        newGame = copy.deepcopy(game)
                        countMoves = 1
                        #Move the car up while it is possible
                        while self.moveUp(newGame, row-countMoves+1, col, game[row][col]) != None and countMoves <= fuelLevels[game[row][col]]:
                            newGame = self.moveUp(newGame, row-countMoves+1, col, game[row][col])
                            moves.append(newGame)
                            direction.append(str(game[row][col]) + ' Up    ' + str(countMoves))

                            #copy the fuel levels
                            newFuelLevels = copy.deepcopy(fuelLevels)
                            #update the fuel levels for the car that moved
                            newFuelLevels[game[row][col]] -= countMoves
                            changeInFuelLevels.append(newFuelLevels)
                            
                            countMoves += 1

        output = [moves, direction, changeInFuelLevels]
        return output