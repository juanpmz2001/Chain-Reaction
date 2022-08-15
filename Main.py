import pygame
import sys
from math import *
from time import sleep
#from NodeChain import NodeChain
#import Tree 

# Initialization of Pygame
#close()
pygame.init()
clock = pygame.time.Clock()

# Initializing the Screen
horizontal_blocks=6
vertical_blocks=11
blocks = 40
width = blocks*horizontal_blocks
height = blocks*vertical_blocks
display = pygame.display.set_mode((width, height))

# Colors
background = (21, 67, 96)
border = (208, 211, 212)
red = (231, 76, 60)
white = (244, 246, 247)
violet = (136, 78, 160)
yellow = (244, 208, 63)
green = (88, 214, 141)

#Selected players
playerColor = [red, green]
noPlayers = 2
font = pygame.font.SysFont("Times New Roman", 20)
#title of the game window 
pygame.display.set_caption("Chain Reaction %d Player, Isis vs AI" % noPlayers)
#initialize players and scores
score = []
players = []
for i in range(noPlayers):
    score.append(0)
    players.append(playerColor[i])

d = blocks//2 - 2
cols = int(width//blocks)
rows = int(height//blocks)
grid = []


# print the grid state
def printer():
    for x in grid:
        for obj in x:
            print(obj.__str__())
# Quit or Close the Game Window
def close():
    #printer()
    pygame.quit()
    sys.exit()
# Class for Each Spot in Grid
class Spot():
    def __init__(self):
        self.color = border
        self.neighbors = []
        self.noAtoms = 0

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
# Initializing the Grid with "Empty or 0"
def initializeGrid():
    global grid, score, players
    score = []
    players = []
    for i in range(noPlayers):
        score.append(0)
        players.append(playerColor[i])
        
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
                grid[int(i)][int(j)].color = border
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

        display.blit(text, ((width-160)/2, height/3))
        display.blit(text2, ((width-160)/2, height/2 ))

        pygame.display.update()
        clock.tick(60)

def checkWon():
    num = 0
    for i in range(noPlayers):
        if score[i] == 0:
            num += 1
    if num == noPlayers - 1:
        for i in range(noPlayers):
            if score[i]:
                return i

    return 9999

def gridround ():
    win = None
    newCellsToExplote = 0
    for j,col in enumerate(grid):
        for i,cell in enumerate(col):
            #check if the cell needs to explote, in that case add an atom to their neighbors
            if cell.noAtoms >= len(cell.neighbors):
                cell.noAtoms = cell.noAtoms-len(cell.neighbors)
                for m in range(len(cell.neighbors)):
                    cell.neighbors[m].noAtoms += 1
                    cell.neighbors[m].color = cell.color
                    if cell.neighbors[m].noAtoms >= len(cell.neighbors[m].neighbors):
                        newCellsToExplote+=1
    return grid,newCellsToExplote

def checkwin():
    firstcolor=None
    for col in grid:
        for cell in col:
            if cell.noAtoms!=0:
                if firstcolor==None:
                    firstcolor=cell.color
                if firstcolor!=cell.color:
                    return False
    return True
          
def game2():
    initializeGrid()
    loop = True
    turns = 0
    currentPlayer = 0
    vibrate = .5
    global grid


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
                        grid,newCellsToExplote = gridround()
                        display.fill(background)
                        """"# Vibrate the Atoms in their Cells
                        vibrate *= -1
                        drawGrid(currentPlayer)
                        showPresentGrid(vibrate)
                        pygame.display.update()"""
                        if turns>1 and checkwin():
                            if currentPlayer == 0:
                                gameOver("Red")
                            else:
                                gameOver("Green")
                    currentPlayer += 1
                    if currentPlayer >= noPlayers:
                        currentPlayer = 0

        display.fill(background)
        # Vibrate the Atoms in their Cells
        vibrate *= -1
        drawGrid(currentPlayer)
        showPresentGrid(vibrate)
        pygame.display.update()

        res = checkWon()
        if res < 9999:
            gameOver(res)

        clock.tick(20)    
    

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
            if currentPlayer == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    i = x/blocks
                    j = y/blocks
                    if grid[int(i)][int(j)].color == players[int(currentPlayer)] or grid[int(i)][int(j)].color == border:
                        turns += 1
                        addAtom(i, j, players[currentPlayer])
                        currentPlayer += 1
                        if currentPlayer >= noPlayers:
                            currentPlayer = 0
                        
                    if turns >= noPlayers:
                        isPlayerInGame()
            else: 
                node = NodeChain(True,value="inicio",state = grid, operators= operators)
                tree = Tree(node, operators)
                grid = tree.sAlphaBeta().state
                currentPlayer += 1
                if currentPlayer >= noPlayers:
                    currentPlayer = 0

        display.fill(background)
        # Vibrate the Atoms in their Cells
        vibrate *= -1
        drawGrid(currentPlayer)
        showPresentGrid(vibrate)
        pygame.display.update()
        res = checkWon()
        if res < 9999:
            gameOver(res)
        clock.tick(20)
    
game2()