from Node import Node

#import the game mechanics
from gameMechanics import *

class UCS:
    pass
    
    #UCS algorithm to find the shortest path from initial state to goal state
    def search(initialGame):

        #Initialise the game mechanics
        mechanics = gameMechanics(initialGame)

        #Create the root node
        root = Node(None, "Initial State", mechanics.convertedGame, mechanics.intialFuelLevels, mechanics.findMoves(mechanics.convertedGame, mechanics.intialFuelLevels), 0, 0)
        
        #Create a queue to store nodes
        queue = []
        
        #Create a list to store visited nodes
        visited = []
        visitedNodes = []
        
        #Add the root node to the queue
        queue.append(root)
        
        #While the queue is not empty
        while queue:
            
            #Pop the first node in the queue
            node = queue.pop(0)
            
            
            #If the node is not visited
            if node.game not in visited:
        
                # Add the node to the visited list
                visited.append(node.game)
                visitedNodes.append(node)
                
                #If the node is the goal state return the node
                if node.game[2][5] == 'A':
                    return [node, visitedNodes]
                
                #Add the children of the node to the queue
                for x, child in enumerate(node.children[0]):
                    queue.append(Node(node, node.children[1][x], child, node.children[2][x], mechanics.findMoves(child, node.children[2][x]), node.depth+1, 0))
        return [None, visitedNodes]









        
        