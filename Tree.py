import Node
import NodeChain
import numpy as np

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
        if depth == 0 or node.isObjective():
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
    
    def sAlphaBeta(self, depth = 6):
        self.reinitRoot()
        self.root.v= self.alphabeta(self.root, depth, float('-inf'), float('+inf'), (88, 214, 141))
        values=[c.v for c in self.root.children]
        maxvalue=max(values)
        index=values.index(maxvalue)
        return self.root.children[index] if not self.root.isObjective() else self.root
    