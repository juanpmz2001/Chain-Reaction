
from Node import Node
import numpy as np

def overFlow(cell, color):
    cell.noAtoms = 0
    for m in range(len(cell.neighbors)):
        cell.neighbors[m].noAtoms += 1
        cell.neighbors[m].color = color
        if cell.neighbors[m].noAtoms >= len(cell.neighbors[m].neighbors):
            overFlow(cell.neighbors[m], color)

def addAtom(i, j, color,grid):
    grid[int(i)][int(j)].noAtoms += 1
    grid[int(i)][int(j)].color = color
    if grid[int(i)][int(j)].noAtoms >= len(grid[int(i)][int(j)].neighbors):
        overFlow(grid[int(i)][int(j)], color)


class NodeChain(Node):
    ## Vamos a añadir el jugador, pues en dependencia del jugador se hace una cosa u otra.
    
    def __init__(self, player=True,**kwargs):
        super(NodeChain, self).__init__(**kwargs)
        self.player=player
        if player:
            self.v=float('-inf')
            player=(231, 76, 60)
        else:
            self.v=float('inf')
            player=(88, 214, 141)

    def getState(self, index):
        state=self.state
        nextState=None
        (x,y)=self.operators[index]
        if state[x][y].color == self.player or state[x][y].noAtoms == 0:
            nextState=state.copy()
            addAtom(x, y, self.player,nextState)

        return nextState if state!=nextState else None

    #Costo acumulativo(valor 1 en cada nivel)
    def cost(self):
        return self.level

    ##Ver si el nodo es un nodo objetivo
    def isObjective(self):
        c=[f.copy() for f in self.state]
        z= None
        for i,f in enumerate(c):
            a=0
            while (z==None or z==f[a].color) and a<len(f):
                a+=1
            if a<len(f):
                return False
        if z==None:
            return False
        return True

    ## Si es nodo objetivo, si X retornamos 1, si O -1 y si no 0

    def heuristic(self):
        # Creacion arreglo a de posibilidades
        h=0 
        """
        #verdes a punto de estallar-rojas a punto de estallar
        for c in self.state:
            for f in c:
                if f.sdc == len(f.neighbors-1):
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