from gameMechanics import *

class heuristic1:
    pass

    #Given a 6x6 grid, the heuristic is the number of blocked squares in front of the Ambulance (A)
    def calc_heuristic(game):
        blockedSquares = 0

        for x in reversed(game[2]):
            if x == 'A':
                break
            elif x != '.':
                blockedSquares += 1

        return blockedSquares

class heuristic2:
    pass
    
    #Given a 6x6 grid, the heuristic is the number of cars blocking the ambulance (A)
    def calc_heuristic(game):
        cars = 0
        seenCars = []

        for x in reversed(game[2]):
            if x == 'A':
                break
            elif x != '.' and x not in seenCars:
                cars += 1
                seenCars.append(x)
        
        return cars


class heuristic3:
    pass

    #Heuristic 1 multiplied by a constant
    def calc_heuristic(game):
        
        #Constant
        h3Constant = 5

        return heuristic1.calc_heuristic(game) * h3Constant

class heuristic4:
    pass

    #Heuristic that calculates the number of cars blocking the ambulance (A) + the number of vehicles blocking the cars in the way of the ambulance
    def calc_heuristic(game):
        cars = 0
        seenCars = []

        for col, x in enumerate(reversed(game[2])):
            if x == 'A':
                break
            elif x != '.' and x not in seenCars:
                cars += 1
                seenCars.append(x)
                #If there are any cars blocking this car towards the bottom of the grid
                countRow = 3
                while countRow < 6:
                    if game[countRow][5 - col] != '.' and game[countRow][5 - col] not in seenCars:
                        cars += 1
                        seenCars.append(game[countRow][5 - col])
                    countRow += 1

                #If there are any cards blocking this car towards the top of the grid
                countRow = 1
                while countRow >= 0 :
                    if game[countRow][5 - col] != '.' and game[countRow][5 - col] not in seenCars:
                        cars += 1
                        seenCars.append(game[countRow][5 - col])
                    countRow -= 1

        return cars

                
                

