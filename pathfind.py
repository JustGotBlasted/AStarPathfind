from node import Node
import pygame as p
import random

LENGTH = 600
HEIGHT = 600
X = 40
Y = 40

def main():
    p.init()
    screen = p.display.set_mode((LENGTH, HEIGHT))
    p.display.set_caption("A*")
    time = p.time.Clock()

    grid = []

    for y in range(Y):
        grid.append([])

        for x in range(X):
            n = Node(None, (x, y), True, 0)
            grid[y].append(n)
    
    start = (0, 0)
    end = (X - 1, Y - 1)


    calculated = False
    open = []
    closed = []
    path = []
    

    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                break
            elif p.mouse.get_pressed(num_buttons=3)[0] or p.mouse.get_pressed(num_buttons=3)[2]:
                mouse_pos = p.mouse.get_pos()
                x, y = mouse_pos[0] * X // LENGTH, mouse_pos[1] * Y // HEIGHT

                if 0 <= x < X and 0 <= y < Y and start != (x, y) and end != (x, y):
                    grid[y][x].traversable = p.mouse.get_pressed(num_buttons=3)[2]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z or e.key == p.K_x: # Places starting and ending nodes
                    mouse_pos = p.mouse.get_pos()
                    x, y = mouse_pos[0] * X // LENGTH, mouse_pos[1] * Y // HEIGHT

                    if 0 <= x < X and 0 <= y < Y and start != (x, y) and end != (x, y):
                        n = grid[y][x]
                        n.traversable = True

                        if e.key == p.K_z:
                            start = (x, y)
                        else:
                            end = (x, y)
                elif e.key == p.K_BACKSPACE: # Clears untraversable nodes, open nodes, closed nodes, and path nodes
                    for row in grid:
                        for n in row:
                            n.traversable = True
                    
                    open = []
                    closed = []
                    path = []
                elif e.key == p.K_SPACE: # Pathfinds
                    open, closed, path = pathfind(screen, time, grid, start, end)
                    calculated = True
                elif e.key == p.K_r: # Randomize maze
                    for r in grid:
                        for n in r:
                            if n.position != start and n.position != end:
                                if random.randint(1, 3) == 1:
                                    n.traversable = False
                                else:
                                    n.traversable = True
                    
                    open = []
                    closed = []
                    path = []


        
        drawGrid(screen, grid, start, end, open, closed, path)

        p.display.flip()
        time.tick(60)
    

def pathfind(screen, time, grid, start, end):
    open = [Node(None, start, True, 0)] # list of nodes that haven't been evaluated but can be
    closed = [] # list of nodes that are already evaluated
    path = [] # list of nodes that lead to the end


    while len(open) > 0:
        current = None

        cost = 999999
        for n in open:
            n.updateHCost(end)
            n.updateFCost()

            if n.fcost < cost or (n.fcost == cost and n.gcost > current.gcost):
                current = n
                cost = n.fcost
        
        if current.position == end:
            path.append(current)
            break

        open.remove(current)
        closed.append(current)


        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        availableDirs = []

        for dir in directions:
            coord = (dir[0] + current.position[0], dir[1] + current.position[1])

            if 0 <= coord[0] < X and 0 <= coord[1] < Y:
                neighbor = grid[coord[1]][coord[0]]

                if not neighbor.traversable or neighbor in closed:
                    continue


                if (abs(dir[0]) == 1 and abs(dir[1]) == 1) and not ((dir[0], 0) in availableDirs or (0, dir[1]) in availableDirs): # Don't move diagonally if both adjacent nodes are not traversable
                    continue


                if neighbor in open:
                    oldParent = neighbor.parent
                    oldCost = neighbor.gcost

                    neighbor.parent = current
                    neighbor.updateGCost(start)

                    if oldCost > neighbor.gcost:
                        neighbor.parent = current
                    else:
                        neighbor.parent = oldParent
                        neighbor.gcost = oldCost
                else:
                    neighbor.parent = current
                    neighbor.gcost = current.gcost + (14 if abs(dir[0]) == 1 and abs(dir[1]) == 1 else 10)

                    open.append(neighbor)
                
                availableDirs.append(dir)
        


   
        
        drawGrid(screen, grid, start, end, open, closed, path)
        p.display.flip()
        time.tick(60)
    

    if len(path) > 0:
        currentNode = path[0]

        while currentNode.position != start:
            path.append(currentNode)

            parent = currentNode.parent
            currentNode = parent
    

    return open, closed, path

    


def drawGrid(screen, grid, start, end, open, closed, path):#
    s = p.Surface((LENGTH//X, HEIGHT//Y))
    colors=["gray85", "gray90"]

    for x in range(X):
        for y in range(Y):
            s.fill(colors[(x+y) % 2])
            screen.blit(s, (x*LENGTH//X, y*HEIGHT//Y))


            n = grid[y][x]

            if not n.traversable:
                changeNodeColor(screen, x, y, "black")
            elif (x, y) == start:
                changeNodeColor(screen, x, y, "blue")
            elif (x, y) == end:
                changeNodeColor(screen, x, y, "orange")
            elif n in path:
                changeNodeColor(screen, x, y, "green")
            elif n in open:
                changeNodeColor(screen, x, y, "purple")
            elif n in closed:
                changeNodeColor(screen, x, y, "red")
    

def changeNodeColor(screen, x, y, color):
    s = p.Surface((LENGTH//X, HEIGHT//Y))
    s.fill(color)
    s.set_alpha(200)
    screen.blit(s, (x*LENGTH//X, y*HEIGHT//Y))


if __name__ == "__main__":
    main()