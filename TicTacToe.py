
import pydot
from IPython.display import Image, display
import queue
import numpy as np

class Node ():

    def __init__(self, state,value,operators = None,operator=None, parent=None,objective=None):
        self.state= state
        self.value = value
        self.children = []
        self.parent=parent
        self.operator=operator
        self.objective=objective
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

class Tree ():
    def __init__(self, root ,operators):
        self.root=root
        self.operators=operators

    def printPath(self,n):
        stack = n.pathObjective()
        path = stack.copy()
        while len(stack)!=0:
            node=stack.pop()
            if node.operator is not None:
                print(f'operador:  {self.operators[node.operator]} \t estado: {node.state}')
            else:
                print(f' {node.state}')
        return path

    def reinitRoot(self):
        self.root.operator=None
        self.root.parent=None
        self.root.objective=None
        self.root.children = []
        self.root.level=0

    def alphabeta(self, node, depth, alpha, beta, player):
        if depth == 0 or node.isObjective():
            node.v = node.heuristic()
            return node.heuristic()
        if player:
            value=float('-inf')
            children = node.getchildrens()
            for i,child in enumerate(children):
                if child is not None:
                    newChild=type(self.root)(value=node.value+'-'+str(i),state=child.copy(),operator=i,parent=node, operators=node.operators,player=False)
                    newChild=node.add_node_child(newChild)
                    value = max(value,self.alphabeta(newChild, depth-1, alpha,beta,False))
                    alpha = max(alpha,value)
                    if alpha>=beta:
                        break
        else:
            value=float('inf')
            children = node.getchildrens()
            for i,child in enumerate(children):
                if child is not None:
                    newChild=type(self.root)(value=node.value+'-'+str(i),state=child.copy(),operator=i,parent=node, operators=node.operators,player=True)
                    newChild=node.add_node_child(newChild)
                    value = min(value,self.alphabeta(newChild, depth-1, alpha,beta,True))
                    beta = min(beta,value)
                    if alpha>=beta:
                        break
        node.v = value
        return value 
    
    def sAlphaBeta(self, depth = 6):
        self.root.v= self.alphabeta(self.root, depth, float('-inf'), float('+inf'), True)
        values=[c.v for c in self.root.children]
        maxvalue=max(values)
        index=values.index(maxvalue)
        return self.root.children[index] if not self.root.isObjective() else self.root
        

    def draw(self,path):
        graph = pydot.Dot(graph_type='graph')
        nodeGraph=pydot.Node(str(self.root.state)+"-"+str(0),
                            label=str(self.root.state),shape ="circle", 
                            style="filled", fillcolor="red")
        graph.add_node(nodeGraph)
        path.pop()
        return self.drawTreeRec(self.root,nodeGraph,graph,0,path.pop(),path)
        
    def drawTreeRec(self,r,rootGraph,graph,i,topPath,path):
        if r is not None:
            children=r.children
            for j,child in enumerate(children):
                i=i+1
                color="white"
                if topPath.value==child.value:
                    if len(path)>0:topPath=path.pop()
                    color='red'
                c=pydot.Node(child.value,label=str(child.state)+r"\n"+r"\n"+"f="+str(child.f()), 
                            shape ="circle", style="filled", 
                            fillcolor=color)
                graph.add_node(c)
                graph.add_edge(pydot.Edge(rootGraph, c, 
                                        label=str(child.operator)+'('+str(child.cost())+')'))
                graph=self.drawTreeRec(child,c,graph,i,topPath,path)  # recursive call  u
            return graph
        else:
            return graph


class NodeTicTacToe(Node):
    ## Vamos a añadir el jugador, pues en dependencia del jugador se hace una cosa u otra.

    def __init__(self, player=True,**kwargs):
        super(NodeTicTacToe, self).__init__(**kwargs)
        self.player=player
        if player:
            self.v=float('-inf')
        else:
            self.v=float('inf')

    def getState(self, index):
        state=self.state
        nextState=None
        (x,y)=self.operators[index]
        if state[x][y]==' ':
            nextState= [f.copy() for f in state]
            if self.player==True: ## Si es maquina    
                nextState[x][y] = str('X')
            else: ## Si es persona
                nextState[x][y] = str('O')
        return nextState if state!=nextState else None

    #Costo acumulativo(valor 1 en cada nivel)
    def cost(self):
        return self.level

    ##Ver si el nodo es un nodo objetivo para O o para X, o hay empate
    def isObjective(self):
        a=[f.copy() for f in self.state]
        b=np.array(a).T
        a.append(np.diag(self.state))
        a.append(np.flipud(self.state).diagonal())
        a=np.array(a)
        c=np.concatenate((a,b),axis=0)
        for f in c:
            if f[0]!=' ' and all(x == f[0] for x in f):
                print(True)
                return True
            ### Empate
        if not np.in1d([' '], self.state):
            print(True)
            return True
        print(False)
        return False   

    ## Si es nodo objetivo, si X retornamos 1, si O -1 y si no 0

    def heuristic(self):
        # Creacion arreglo a de posibilidades
        a=[f.copy() for f in self.state]
        b=np.array(a).T
        a.append(np.diag(self.state.copy()))
        a.append(np.flipud(self.state.copy()).diagonal())
        a=np.array(a)
        c=np.concatenate((a,b),axis=0)
        h = 0

        for p in c:
            sumx = sum(np.char.count(p, 'X'))
            sumo = sum(np.char.count(p, 'O'))
            if sumx == 3:
                return 50
            elif sumo == 3:
                return -50
            else:
                if sumx != 0 and sumo == 0:
                    h += 1
                if sumo != 0 and sumx == 0:
                    h -= 1
        
        return h


def draw_board(current_state):
    for i in range(0, 3):
        for j in range(0, 3):
            print('{}|'.format(current_state[i][j]), end=" ")
        print()
    print()

def is_valid(px, py, current_state):
    if px < 0 or px > 2 or py < 0 or py > 2:
        return False
    elif current_state[px][py] != ' ':
        return False
    else:
        return True

def play():

    current_state = [[' ', ' ', ' '],
                    [' ', ' ', ' '],
                    [' ', ' ', ' ']]
        
    operators = [(i,j) for i,f in enumerate(current_state) for j,c in enumerate(f)]

    player_turn = 'X'

    node = NodeTicTacToe(True,value="inicio",state = current_state, operators= operators)
    
    while node.isObjective() == False:
        print(not node.isObjective())
        draw_board(current_state)

        # If it's player's turn
        if player_turn == 'O':

            while True:

                px = int(input('Insert the X coordinate: '))
                py = int(input('Insert the Y coordinate: '))

                if is_valid(px, py, current_state):
                    current_state[px][py] = 'O'
                    player_turn = 'X'
                    break
                else:
                    print('The move is not valid! Try again.')

        # If it's AI's turn
        else:
            node = NodeTicTacToe(True,value="inicio",state = current_state, operators= operators)
            tree = Tree(node, operators)
            current_state = tree.sAlphaBeta().state
            player_turn = 'O'