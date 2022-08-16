import Tree
import Node
import numpy as np

class NodeChain(Node):
    ## Vamos a añadir el jugador, pues en dependencia del jugador se hace una cosa u otra.
    
    def __init__(self, player=(88, 214, 141),**kwargs):
        super(NodeChain, self).__init__(**kwargs)
        self.player=player
        if player == (88, 214, 141):
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
            newCellsToExplote = 1
            while (newCellsToExplote>0):
                grid,newCellsToExplote = gridround(nextState)
                if checkwin(nextState):
                    break
        return nextState if state!=nextState else None

    #Costo acumulativo(valor 1 en cada nivel)
    def cost(self):
        return self.level

    ##Ver si el nodo es un nodo objetivo
    def isObjectiveC(self):
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
        if (r == 0 and g > 0) or (r > 0 and g == 0):
            return True
        return False

    ##Ver si el nodo es un nodo objetivo
    def isObjectiveM(self):
        c = [f.copy() for f in self.state]
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