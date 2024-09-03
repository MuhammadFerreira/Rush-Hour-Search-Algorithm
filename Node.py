#Node class with game state and list of children
class Node:
    def __init__(self, parent, changeFromParent, game, currentFuel, children, depth, heuristicValue):
        self.parent = parent
        self.changeFromParent = changeFromParent
        self.game = game
        self.currentFuel = currentFuel
        self.children = children
        self.depth = depth
        self.heuristicValue = heuristicValue
        self.fValue = self.heuristicValue + self.depth
    