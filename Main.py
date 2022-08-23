import pygame
import sys
from math import *
import numpy as np

pygame.init()
clock = pygame.time.Clock()

# Initializing the Screen
horizontal_blocks=6
vertical_blocks=11
blocks = 40
width = blocks*horizontal_blocks
height = blocks*vertical_blocks
display = pygame.display.set_mode((width, height))
d = blocks//2 - 2
cols = int(width//blocks)
rows = int(height//blocks)
grid = []
turns = 0

# Colors
background = (21, 67, 96)
red = (231, 76, 60)
green = (88, 214, 141)
white = (255, 255, 255)
players = [red, green]
font = pygame.font.SysFont("Times New Roman", 20)

#title of the game window 
pygame.display.set_caption("Chain Reaction Player, Isis vs AI" )

def printState(state):
    x = ''
    for row in state:
        for con in row:
            x += str(con) + ' '
        print(x)
        x = ''

class Node ():

    def __init__(self, state,value,operators = None,operator=None, parent=None,objective=None):
        self.state= state
        self.value = value
        self.children = []
        self.parent=parent
        self.operator=operator
        self.level=0
        self.operators=operators
        self.v=0

    def add_child(self, value, state, operator):
        node=type(self)(value=value, state=state, operator=operator,parent=self,operators=self.operators)
        node.level=node.parent.level+1
        self.children.append(node)
        return node
    
    def add_node_child(self, node):
        node.level=node.parent.level+1
        self.children.append(node)    
        return node

    #Devuelve todos los estados según los operadores aplicados
    def getchildrens(self):
        return [
            self.getState(i) 
                if not self.repeatStatePath(self.getState(i)) 
                    else None for i,op in enumerate(self.operators)]
        
    def getState(self, index):
        pass
    
    def __eq__(self, other):
        return self.state == other.state
    
    def __lt__(self, other):
        return self.f() < other.f()
    
    
    def repeatStatePath(self, state):
        n=self
        while n is not None and n.state!=state:
            n=n.parent
        return n is not None
        
    def pathObjective(self):
        n=self
        result=[]
        while n is not None:
            result.append(n)
            n=n.parent
        return result

    def cost(self):
        return 1
    
    def f(self): 
        return self.cost()+self.heuristic()

    def heuristic(self):
        return 0
    ### Crear método para criterio objetivo
    ### Por defecto vamos a poner que sea igual al estado objetivo, para cada caso se puede sobreescribir la función
    def isObjective(self):
        pass

class NodeChain(Node):
    ## Vamos a añadir el jugador, pues en dependencia del jugador se hace una cosa u otra.
    
    def __init__(self, player,**kwargs):
        super(NodeChain, self).__init__(**kwargs)
        self.player=player
        if player == (88, 214, 141):
            self.v=float('-inf')
        else:
            self.v=float('inf')

    def getState(self, index):
        #print(len(self.operators))
        state=self.state
        global turns
        nextState=None
        (x,y)=self.operators[index]
        if state[x][y].color == self.player or state[x][y].noAtoms == 0:
            nextState = []
            for i in range(len(state)):
                nextState.append([])
                for j in range(len(state[i])):
                    nextState[i].append(state[i][j].copy())
            
            newCellsToExplote = 1
            nextState[x][y].noAtoms += 1
            nextState[x][y].color = (88, 214, 141) if turns%2!=0 else (231, 76, 60)
            turns+=1
            #print('before while')
            #printState(nextState)
            while (newCellsToExplote>0):
                nextState,newCellsToExplote = gridround(nextState)
                if checkwin(nextState):
                    break
        #if nextState is not None:
            #print('after while')
            #printState(nextState)
        return nextState if state!=nextState else None

    #Costo acumulativo(valor 1 en cada nivel)
    def cost(self):
        return self.level

    ##Ver si el nodo es un nodo objetivo
    def isObjective(self):
        return checkwin(self.state)

    def heuristic(self):
        # Creacion arreglo a de posibilidades
        h=0 
        
        #verdes a punto de estallar-rojas a punto de estallar
        """
        for c in self.state:
            for f in c:
                if f.noAtoms == len(f.neighbors)-1:
                    if f.color == green:
                        h+=1
                    else:
                        h-=1
        """
        for c in self.state:
            for f in c:
                if f.color == (88, 214, 141):
                    h+=1
                else:
                    h-=1
        
        return h
        
class Tree():
    def __init__(self, root ,operators):
        self.root=root
        self.operators=operators

    def reinitRoot(self):
        self.root.operator=None
        self.root.parent=None
        self.root.objective=None
        self.root.children = []
        self.root.level=0

    def alphabeta(self, node, depth, alpha, beta, player):

        #print(depth==0)
        #print(checkwin(node.state))
        if depth == 0 or checkwin(node.state):
            node.v = node.heuristic()
            return node.heuristic()
        if player == (88, 214, 141):
            value=float('-inf')
            children = node.getchildrens()
            for i,child in enumerate(children):
                if child is not None:
                    newChild=type(self.root)(value=node.value+'-'+str(i),state=child.copy(),operator=i,parent=node, operators=node.operators,player=(231, 76, 60))
                    newChild=node.add_node_child(newChild)
                    value = max(value,self.alphabeta(newChild, depth-1, alpha,beta,(231, 76, 60)))
                    alpha = max(alpha,value)
                    if alpha>=beta:
                        break
        else:
            value=float('inf')
            children = node.getchildrens()
            for i,child in enumerate(children):
                if child is not None:
                    newChild=type(self.root)(value=node.value+'-'+str(i),state=child.copy(),operator=i,parent=node, operators=node.operators,player=(88, 214, 141))
                    newChild=node.add_node_child(newChild)
                    value = min(value,self.alphabeta(newChild, depth-1, alpha,beta,(88, 214, 141)))
                    beta = min(beta,value)
                    if alpha>=beta:
                        break
        node.v = value
        return value 
    
    def sAlphaBeta(self, depth = 2):
        self.reinitRoot()
        self.root.v= self.alphabeta(self.root, depth, float('-inf'), float('+inf'), (88, 214, 141))
        values=[c.v for c in self.root.children]
        maxvalue=max(values)
        index=values.index(maxvalue)
        return self.root.children[index] if not self.root.isObjective() else self.root

# Class for Each Spot in Grid
class Spot():
    def __init__(self,color = None, neighbors = None,noAtoms = 0):
        self.color = color
        if neighbors == None:
            self.neighbors = []
        else:
            self.neighbors = neighbors
        self.noAtoms = noAtoms

    def addNeighbors(self, i, j):
        if i > 0:
            self.neighbors.append(grid[i - 1][j])
        if i < cols - 1:
            self.neighbors.append(grid[i + 1][j])
        if j < rows - 1:
            self.neighbors.append(grid[i][j + 1])
        if j > 0:
            self.neighbors.append(grid[i][j - 1])

    def __str__(self):
        return f"{self.color}: {self.noAtoms}"
    
    def copy(self):
        return Spot(color = self.color, neighbors = self.neighbors.copy(), noAtoms = self.noAtoms)

# Quit or Close the Game Window
# Initializing the Grid with "Empty or 0"
def initializeGrid():
    global grid

    grid = [[]for _ in range(cols)]
    for i in range(cols):
        for j in range(rows):
            newObj = Spot()
            grid[i].append(newObj)
    for i in range(cols):
        for j in range(rows):
            grid[int(i)][int(j)].addNeighbors(i, j)

# Draw the Grid in Pygame Window   
def drawGrid(currentIndex):
    r = 0
    c = 0
    for i in range(max(height,width)//blocks):
        r += blocks
        c += blocks
        pygame.draw.line(display, players[currentIndex], (c, 0), (c, height))
        pygame.draw.line(display, players[currentIndex], (0, r), (width, r))

# Draw the Present Situation of Grid
def showPresentGrid(vibrate = 1):
    r = -blocks
    c = -blocks
    padding = 2
    for i in range(cols):
        r += blocks
        c = -blocks 
        for j in range(rows):
            c += blocks
            if grid[int(i)][int(j)].noAtoms == 0:
                grid[int(i)][int(j)].color = None
            elif grid[int(i)][int(j)].noAtoms == 1:
                pygame.draw.ellipse(display, grid[int(i)][int(j)].color, (r + blocks/2 - d/2 + vibrate, c + blocks/2 - d/2, d, d))
            elif grid[int(i)][int(j)].noAtoms == 2:
                pygame.draw.ellipse(display, grid[int(i)][int(j)].color, (r + 5, c + blocks/2 - d/2 - vibrate, d, d))
                pygame.draw.ellipse(display, grid[int(i)][int(j)].color, (r + d/2 + blocks/2 - d/2 + vibrate, c + blocks/2 - d/2, d, d))
            elif grid[int(i)][int(j)].noAtoms == 3:
                angle = 90
                x = r + (d/2)*cos(radians(angle)) + blocks/2 - d/2
                y = c + (d/2)*sin(radians(angle)) + blocks/2 - d/2
                pygame.draw.ellipse(display, grid[int(i)][int(j)].color, (x - vibrate, y, d, d))
                x = r + (d/2)*cos(radians(angle + 90)) + blocks/2 - d/2
                y = c + (d/2)*sin(radians(angle + 90)) + 5
                pygame.draw.ellipse(display, grid[int(i)][int(j)].color, (x + vibrate, y, d, d))
                x = r + (d/2)*cos(radians(angle - 90)) + blocks/2 - d/2
                y = c + (d/2)*sin(radians(angle - 90)) + 5
                pygame.draw.ellipse(display, grid[int(i)][int(j)].color, (x - vibrate, y, d, d))

    pygame.display.update()

# GAME OVER
def gameOver(playerIndex):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    game2()

        text = font.render(f"Player {playerIndex} Won!" , True, white)
        text2 = font.render("Press \'r\' to Reset!", True, white)
        text3 = font.render("Press \'q\' to Quit!", True, white)

        display.blit(text, ((width-160)/2, height/3))
        display.blit(text2, ((width-160)/2, height/2 ))
        display.blit(text3, ((width-160)/2, height/2 ))

        pygame.display.update()
        clock.tick(60)

#
def gridround (gride):
    newCellsToExplote = 0
    for j,col in enumerate(gride):
        for i,cell in enumerate(col):
            #check if the cell needs to explote, in that case add an atom to their neighbors
            if cell.noAtoms >= len(cell.neighbors):
                cell.noAtoms = cell.noAtoms-len(cell.neighbors)
                for m in range(len(cell.neighbors)):
                    cell.neighbors[m].noAtoms += 1
                    cell.neighbors[m].color = cell.color
                    if cell.neighbors[m].noAtoms >= len(cell.neighbors[m].neighbors):
                        newCellsToExplote+=1
    return gride,newCellsToExplote

#verify if the game is over and return True if it is
def checkwin(gride):
    firstcolor=None
    global turns
    if turns>2:
        for col in gride:
            for cell in col:
                if cell.noAtoms!=0:
                    if firstcolor==None:
                        firstcolor=cell.color
                    if firstcolor!=cell.color:
                        return False
        return True
    return False

#  The new game method    
def game2():
    initializeGrid()
    loop = True
    currentPlayer = 0
    vibrate = .5
    global grid
    global turns

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i = x/blocks
                j = y/blocks
                if grid[int(i)][int(j)].color == players[int(currentPlayer)] or grid[int(i)][int(j)].noAtoms == 0:
                    turns += 1
                    newCellsToExplote=1
                    grid[int(i)][int(j)].noAtoms += 1
                    grid[int(i)][int(j)].color = players[currentPlayer]
                    while (newCellsToExplote>0):
                        grid,newCellsToExplote = gridround(grid)
                        if turns>1 and checkwin(grid):
                            break
                    currentPlayer += 1
                    if currentPlayer >= 2:
                        currentPlayer = 0

        display.fill(background)
        # Vibrate the Atoms in their Cells
        vibrate *= -1
        drawGrid(currentPlayer)
        showPresentGrid(vibrate)
        pygame.display.update()
        if checkwin(grid):
            if currentPlayer == 0:
                gameOver("Red")
            else:
                gameOver("Green")
        clock.tick(20)    

#The method to play with the IA
def GameIA():
    global grid
    initializeGrid()
    loop = True
    turns = 0
    currentPlayer = 0
    vibrate = .5
    operators = [(i,j) for i,f in enumerate(grid) for j,c in enumerate(f)]
    node = NodeChain(player=(88, 214, 141),value="inicio",state = grid, operators= operators)
    while loop:

        if currentPlayer == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    i = x/blocks
                    j = y/blocks
                    if grid[int(i)][int(j)].color == players[currentPlayer] or grid[int(i)][int(j)].noAtoms == 0:
                        newCellsToExplote=1
                        grid[int(i)][int(j)].noAtoms += 1
                        grid[int(i)][int(j)].color = players[currentPlayer]
                        while (newCellsToExplote>0):
                            grid,newCellsToExplote = gridround(grid)
                            if turns>1 and checkwin(grid):
                                break
                        currentPlayer = 1
                        turns += 1

        else: 
            operators = [(i,j) for i,f in enumerate(grid) for j,c in enumerate(f)]
            node = NodeChain(True,value="inicio",state = grid, operators= operators)
            tree = Tree(node, operators)
            grid = tree.sAlphaBeta().state
            printState(grid)
            turns += 1
            currentPlayer = 0

        display.fill(background)
        # Vibrate the Atoms in their Cells
        vibrate *= -1
        drawGrid(currentPlayer)
        showPresentGrid(vibrate)
        pygame.display.update()
        if turns>1 and checkwin(grid):
            gameOver("Green")
        clock.tick(20)

()#sebas sos un tajado
GameIA()