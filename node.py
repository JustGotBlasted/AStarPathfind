class Node:
    def __init__(self, parent, position, traversable, gcost) -> None:
        self.parent = parent
        self.position = position
        self.traversable = traversable
        self.gcost = -1
        self.hcost = -1
        self.fcost = -1
    

    def updateHCost(self, endNode):
        xd = abs(self.position[0] - endNode[0])
        yd = abs(self.position[1] - endNode[1])
        self.hcost = min(xd, yd) * 14 + abs(xd - yd) * 10
    

    def updateGCost(self, startNode):
        self.gcost = 0
        currentNode = self

        while currentNode.position != startNode:
            
            parent = currentNode.parent
            self.gcost += 14 if currentNode.position[0] != parent.position[0] and currentNode.position[1] != parent.position[1] else 10
            currentNode = parent


    def updateFCost(self):
        self.fcost = self.hcost + self.gcost
    

    def __repr__(self) -> str:
        return str(self.position)

    def __str__(self) -> str:
        return str(self.position)