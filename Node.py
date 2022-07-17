from ast import NodeTransformer


class Node:
    val = None
    type = None    
    NodeType = None
    childs = None

    def __init__(self, type = None, val = None ):
        self.type = type
        self.val = val
        self.childs = []
        if type in ['floatdcl', 'intdcl']:
            self.NodeType = 'SymDeclaring'
        elif type == 'assign':
            self.NodeType = 'Assigning'
        elif type in ['plus', 'minus', 'times', 'divide']:
            self.NodeType = 'Computing'
        elif type == 'fnum':
            self.NodeType = 'FloatConsting'
        elif type == 'inum':
            self.NodeType = 'IntConsting'
        
        

    def child1(self):
        return self.childs[0]

    def child2(self):
        return self.childs[1]
    
    def setVal(self, val):
        self.val = val

    def setType(self, type):
        self.type = type

    def addChilds(self, nodes):
        if type(nodes) is list:
            for node in nodes:
                self.childs.append(node)
        else:
            self.childs.append(nodes)
        self.validation()

    def validation(self):
        if self.childs.__len__() == 1:
            if self.childs[0].type == 'id' and self.type in ['assign', 'plus', 'minus', 'times', 'divide']:
                self.childs[0].NodeType = 'SymReferencing'
        if self.childs.__len__() == 2:
            pass
            # if self.childs[1].type not in ['plus','minus'] and self.childs[1].type == 'id':
            #     self.childs[0].NodeType = 'SymDeclaring'
            #     self.childs[1].NodeType = 'SymDeclaring'

    def pop(self):
        return self.childs.pop()

    def __str__(self, level=0):
        if self.type == None:
            self.type = self.NodeType
        if self.val == None:
            self.val = ''
        ret = "\t"*level+(self.type + ':' + str(self.val))+"\n"
        for child in self.childs:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self, level=0):
        if self.type == None:
            self.type = ''
        if self.val == None:
            self.val = ''
        ret = "\t"*level+(self.type + ':' + str(self.val))+"\n"
        for child in self.childs:
            ret += child.__repr__(level+1)
        return ret