from asyncore import loop
from math import *
import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

horizontal_blocks=11
vertical_blocks=6
blocks = 40
width = blocks*horizontal_blocks
height = blocks*vertical_blocks
display = pygame.display.set_mode((width, height))
d = blocks//2 - 2

# Colors
background = (21, 67, 96)
red = (231, 76, 60)
green = (88, 214, 141)
white = (255, 255, 255)
players = [red, green]
font = pygame.font.SysFont("Times New Roman", 20)

#title of the game window 
pygame.display.set_caption("Chain Reaction Player, Isis vs AI" )

def close():
    pygame.quit()
    sys.exit()

def drawGrid(currentIndex):
    r = 0
    c = 0
    for i in range(max(height,width)//blocks):
        r += blocks
        c += blocks
        pygame.draw.line(display, players[currentIndex], (c, 0), (c, height))
        pygame.draw.line(display, players[currentIndex], (0, r), (width, r))

# Draw the Present Situation of Grid
def showPresentGrid(grid, vibrate = 1):
    r = -blocks
    c = -blocks
    padding = 2
    for i in range(rows):
        r += blocks
        c = -blocks 
        for j in range(cols):
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
                    gameIA()

        text = font.render(f"Player {playerIndex} Won!" , True, white)
        text2 = font.render("Press \'r\' to Reset!", True, white)
        text3 = font.render("Press \'q\' to Quit!", True, white)

        display.blit(text, ((width-160)/2, height/3))
        display.blit(text2, ((width-160)/2, height/2 ))
        display.blit(text3, ((width-160)/2, height/2 ))

        pygame.display.update()
        clock.tick(60)

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
                    else None for i, op in enumerate(self.operators)]
        
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
        return (self.state==self.objetive.state)

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
        nextState=None

        #print('Estado antes de:')
        #printState(self.state)

        (x,y)=self.operators[index]

        #print(f'color en state{self.state[x][y].color} color player{self.player}')
        #print(f'NroAtoms {self.state[x][y].noAtoms}')

        if self.state[x][y].color == self.player or self.state[x][y].noAtoms == 0:
            nextState = []
            for i in range(len(self.state)):
                nextState.append([])
                for j in range(len(self.state[i])):
                    nextState[i].append(self.state[i][j].copy())

            nextState = nextState[x][y].addAtom(self.player, nextState)

            #print('Estado despues de')
            #printState(nextState)

        return nextState if self.state!=nextState else None

    #Costo acumulativo(valor 1 en cada nivel)
    def cost(self):
        return self.level

    ##Ver si el nodo es un nodo objetivo
    def isObjective(self):
        c = [f.copy() for f in self.state]
        r = 0 
        g = 0
        for f in c:
            for c in f:
                if c.color == (231, 76, 60):
                    r+=1
                    if g != 0:
                        return False
                elif c.color == (88, 214, 141):
                    g+=1
                    if r != 0:
                        return False
        if (r == 0 and g > 1) or (r > 1 and g == 0):
            return True
        return False

    def heuristic(self):
        # Creacion arreglo a de posibilidades
        h=0 
        
        #verdes a punto de estallar-rojas a punto de estallar
        for c in self.state:
            for f in c:
                if f.noAtoms == (len(f.neighbors) - 1):
                    if f.color == green:
                        h+=1
                    else:
                        h-=1
        """
        for c in self.state:
            for f in c:
                if f.color == (88, 214, 141) or f.color == None:
                    h+=1
                else:
                    h-=1

        """
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
        #print('En el metodo alphabeta')
        #print(f'Rectificando {player == (88, 214, 141)} de la var {player}')
        #print(f'Rectificando objetivo {node.isObjective()}')
        if depth == 0 or node.isObjective():
            node.v = node.heuristic()
            #print(f'{node.heuristic()} -> fin recursividad envia vh')
            return node.heuristic()
        if player == (88, 214, 141):
            value=float('-inf')
            children = node.getchildrens()
            #print(f'Juega maquina y genera hijos: {children}')
            for i,child in enumerate(children):
                if child is not None:
                    newChild=type(self.root)(value=node.value+'-'+str(i),state=child.copy(),operator=i,parent=node, operators=node.operators,player=(231, 76, 60))
                    newChild=node.add_node_child(newChild)
                    #print(f'{newChild} nuevo hijo')
                    value = max(value,self.alphabeta(newChild, depth-1, alpha,beta,(231, 76, 60)))
                    alpha = max(alpha,value)
                    if alpha>=beta:
                        break
        else:
            value=float('inf')
            children = node.getchildrens()
            #print(f'Juega add y genera hijos: {len(children)}')
            for i,child in enumerate(children):
                if child is not None:
                    newChild=type(self.root)(value=node.value+'-'+str(i),state=child.copy(),operator=i,parent=node, operators=node.operators,player=(88, 214, 141))
                    newChild=node.add_node_child(newChild)
                    #print(f'{str(newChild)} nuevo hijo')
                    value = min(value,self.alphabeta(newChild, depth-1, alpha,beta,(88, 214, 141)))
                    beta = min(beta,value)
                    if alpha>=beta:
                        break
        node.v = value
        #print ('valor' + str(value))
        return value 
    
    # Depth default en 2 por que con hojas queda analizando 4356 hojas
    # Si se agg depth++ se analizan 287496
    def sAlphaBeta(self, depth = 2):
        self.reinitRoot()
        #print('Inicio alphabeta')
        self.root.v= self.alphabeta(self.root, depth, float('-inf'), float('+inf'), (88, 214, 141))
        #print('Termino alphabeta')
        values=[c.v for c in self.root.children]
        maxvalue=max(values)
        index=values.index(maxvalue)
        return self.root.children[index] if not self.root.isObjective() else self.root

class Spot():
    def __init__(self, index, color=None, neighbords = None, nroAtoms = 0):
        self.color = color
        self.neighbors = []
        self.noAtoms = nroAtoms
        self.index = index
        if neighbords == None:
            self.neighbors = self.addNeighbors(index)
        else: 
            self.neighbors = neighbords

    def addNeighbors(self, index):
        adj = []
        if index == (0, 0) or index == (10, 0) or index == (0, 5) or index == (10, 5):
            if index == (0, 0):
                adj = [(0, 1), (1, 0)]
            elif index == (10, 0):
                adj = [(9, 0), (10, 1)]
            elif index == (0, 5):
                adj = [(0, 4), (1, 5)]
            elif index == (10, 5):
                adj = [(10, 4), (9, 5)]
        elif index[0] == 0 or index[1] == 0 or index[0] == 10 or index[1] == 5:
            if index[0] == 0:
                adj.append((index[0], index[1] - 1))
                adj.append((index[0], index[1] + 1))
                adj.append((index[0] + 1, index[1]))
            elif index[0] == 10:
                adj.append((index[0], index[1] - 1))
                adj.append((index[0], index[1] + 1))
                adj.append((index[0] - 1, index[1]))
            elif index[1] == 0:
                adj.append((index[0] - 1, index[1]))
                adj.append((index[0] + 1, index[1]))
                adj.append((index[0], index[1] + 1))
            elif index[1] == 5:
                adj.append((index[0] - 1, index[1]))
                adj.append((index[0] + 1, index[1]))
                adj.append((index[0], index[1] - 1))
        else:
            adj.append((index[0] - 1, index[1]))
            adj.append((index[0] + 1, index[1]))
            adj.append((index[0], index[1] - 1))
            adj.append((index[0], index[1] + 1))
        
        return adj

    def addAtom(self, color, state):
        self.noAtoms += 1
        self.color = color
        if self.noAtoms >= len(self.neighbors):
            self.color = None
            self.noAtoms = 0
            #print(len(self.neighbors))
            for p in self.neighbors:
                state = state[p[0]][p[1]].addAtom(color, state)
                
        return state

    def copy(self):
        return Spot(index = self.index, color = self.color, neighbords = self.neighbors.copy(), nroAtoms = self.noAtoms)

    def __str__(self):
        return f"{self.color}: {self.noAtoms}"

def printState(state):
    x = ''
    for row in state:
        for con in row:
            x += str(con) + ' '
        print(x)
        x = ''
    print(' ')

def checkwin(gride, turns):
    firstcolor=None

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

cols = 6
rows = 11
red = (231, 76, 60)
green = (88, 214, 141)

def gameIA():
    
    vibrate = .5
    current_state = []
    for i in range(rows):
        current_state.append([])
        for j in range(cols):
            current_state[i].append(Spot((i, j)))

    operators = [(i,j) for i,f in enumerate(current_state) for j,c in enumerate(f)]
    node = NodeChain(green,value="inicio",state = current_state, operators= operators)

    player_turn = True
    printState(current_state)
    turns = -10
    display.fill(background)
    # Vibrate the Atoms in their Cells
    vibrate *= -1
    drawGrid(int(1) if player_turn else int(0))
    showPresentGrid(current_state,vibrate)
    pygame.display.update()
    while not checkwin(current_state, turns):
        if player_turn:
            loop=True
            while loop:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        close()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            close()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        px = int(x/blocks)
                        py = int(y/blocks)
                        if current_state[px][py].color == red or current_state[px][py].color == None:
                            current_state = current_state[px][py].addAtom(red, current_state)
                        player_turn = False
                        loop = False
                
        else:
            node = NodeChain(green,value="inicio",state = current_state, operators= operators)
            tree = Tree(node, operators)
            current_state = tree.sAlphaBeta().state
            player_turn = True

        display.fill(background)
        # Vibrate the Atoms in their Cells
        vibrate *= -1
        drawGrid(int(1) if player_turn else int(0))
        showPresentGrid(current_state,vibrate)
        pygame.display.update()
        turns += 1
        clock.tick(20)
        printState(current_state)

    if player_turn:
        gameOver("Green")
    else:
        gameOver("Red")
gameIA()