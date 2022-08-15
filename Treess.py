class Treesses():
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
    