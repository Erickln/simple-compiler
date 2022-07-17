from ast import operator
from lib2to3.pgen2 import token
from lib2to3.pygram import Symbols
from Tokens import Tokens
from Node import Node

global content_index
global content
global symbols
global OPERATORS
global root

root = Node("prog")

OPERATORS = ('plus', 'minus', 'times', 'divide', 'mod', 'exp')

symbols = {}
content_index = 0

def peek():
    global content
    global content_index
    return content[content_index]

def advance():
    global content_index
    val = peek()
    content_index = content_index + 1
    return val

def eof():
    global content
    global content_index
    return content_index >= len(content)

def scan_digits():
    ans = {
        'val': ''
    }
    while peek() in '0123456789':
        ans['val'] = ans['val'] + advance()
    if peek() != '.':
        ans['type'] = 'inum'
    else: 
        ans['type'] = 'fnum'
        ans['val'] = ans['val'] + advance()
        while peek() in '0123456789':
            ans['val'] = ans['val'] + advance()
    return ans
        
def scanner():
    ans = {}
    while not eof() and (peek() == ' ' or peek() == '\n') : 
        advance()
    if eof():
        ans["type"] = '$'
    else:
        if peek() in '0123456789':
            ans = scan_digits()
        else:
            ch = advance()
            if ch in 'abcdeghjklmnoqrstuvwxyz':
                ans['type'] = 'id'
                ans['val'] = ch
            elif ch == 'f':
                ans['type'] = 'floatdcl'
            elif ch == 'i':
                ans['type'] = 'intdcl'
            elif ch == 'p':
                ans['type'] = 'print'
            elif ch == '=':
                ans['type'] = 'assign'
            elif ch == '+':
                ans['type'] = 'plus'
            elif ch == '-':
                ans['type'] = 'minus'
            else:
                print('error lexico')
                exit()
    return ans        


# ----------------------------------- Parser code 
def exp(pop):
    node = pop
    parent = Node(tokens.advance()['type'])
    parent.addChilds(node)
    # if tokens.peek()['type'] in OPERATORS:
    #     parent.addChilds(exp(tokens))
    if tokens.peek()['type'] in ('inum', 'fnum', 'id'):
        parent.addChilds(val(tokens))
        tokens.advance()
        if tokens.peek()['type'] in OPERATORS:
            parent.addChilds(exp(parent.pop()))
    else:
        print('error sintactico')
        exit()
    return [parent]

def val(tokens):
    token = tokens.peek()
    if token['type'] in ('inum', 'fnum', 'id'): 
        return [Node(token['type'], token['val'])]
    else:
        print('error sintactico')
        exit()

def stmt(tokens):
    if tokens.peek()['type'] == 'id':
        node = Node(tokens.peek()['type'], tokens.advance()['val'])
        if tokens.peek()['type'] == 'assign':
            parent = Node(tokens.advance()['type']) # create assign node as parent
            parent.addChilds(node)                  # add id node as child
            # if tokens.peek()['type'] in OPERATORS:
            #     parent.addChilds(exp(tokens.pop()))       # add exp node as child
            if tokens.peek()['type'] in ('inum', 'fnum', 'id', '$'):
                parent.addChilds(val(tokens))           # add val node as child
                tokens.advance()
                if tokens.peek()['type'] in OPERATORS:
                    parent.addChilds(exp(parent.pop()))
            else: 
                print('error sintactico')
                exit()
        else:   
            print('error sintactico')
            exit()
    elif tokens.peek()['type'] == 'print':
        node = Node(tokens.advance()['type'])
        if tokens.peek()['type'] == 'id':
            node.setVal(tokens.advance()['val'])
            return [node]
        else:
            print('error sintactico')
            exit()
    elif tokens.peek()['type'] == '$':
        return
    else:
        print('error sintactico')
        exit()
    return [parent]

def stmts(tokens):
    if (
        tokens.peek()['type'] == 'id'
        or tokens.peek()['type'] == 'print' 
    ):
        nodes = stmt(tokens)
        return nodes + stmts(tokens)
    return []

def dcl(tokens):
    if tokens.peek()['type'] == 'intdcl' or tokens.peek()['type'] == 'floatdcl':
        node = Node(tokens.advance()['type'])
        if tokens.peek()['type'] == 'id':
            node.setVal(tokens.advance()['val'])
            return [node]
        else:
            print('error sintactico')
            exit()
    return []


def dcls(tokens):
    if tokens.peek()['type'] == 'intdcl' or tokens.peek()['type'] == 'floatdcl':
        nodes = dcl(tokens)
        return nodes + dcls(tokens)
    return []

# this method is used to iterate the ast tree and make the semantic analysis
def visitNodes(root):
    for node in root.childs:
        visit(node)
        visitNodes(node)


        # if node.getType() == 'id':
        #     if node.getVal() not in symbols:
        #         symbols[node.getVal()] = 0
        #     else:
        #         print('error semantico')
        #         exit()
        # elif node.getType() == 'assign':
        #     if node.getChilds()[0].getVal() in symbols:
        #         symbols[node.getChilds()[0].getVal()] = node.getChilds()[1].getVal()
        #     else:
        #         print('error semantico')
        #         exit()
        # elif node.getType() == 'print':
        #     if node.getChilds()[0].getVal() in symbols:
        #         print(symbols[node.getChilds()[0].getVal()])
        #     else:
        #         print('error semantico')
        #         exit()
        # elif node.getType() == 'plus':
        #     if node.getChilds()[0].getVal() in symbols:
        #         symbols[node.getChilds()[0].getVal()] = symbols[node.getChilds()[0].getVal()] + node.getChilds()[1].getVal()
        #     else:
        #         print('error semantico')
        #         exit()
        # elif node.getType() == 'minus':
        #     if node.getChilds()[0].getVal() in symbols:
        #         symbols[node.getChilds()[0].getVal()] = symbols[node.getChilds()[0].getVal()] - node.getChilds()[1].getVal()
        #     else:
        #         print('error semantico')
        #         exit()
        # elif node.getType() == 'times':
        #     if node.getChilds()[0].getVal() in symbols:
        #         symbols[node.getChilds()[0].getVal()] = symbols[node.getChilds()[0].getVal()] * node.getChilds()[1].getVal()
        #     else:
        #         print('error semantico')
        #         exit()
        # elif node.getType() == 'divide':
        #     if node.getChilds()[0].getVal() in symbols:
        #         symbols[node.getChilds()[0].getVal()] = symbols[node.getChilds()[0].getVal()] / node.getChilds()[1].getVal()
        #     else:
        #         print('error semantico')
        #         exit()
        # elif node.getType() == 'inum':
        #     if node.getVal() in symbols:
        #         symbols[node.getVal()] = node.getVal()
        #     else:
        #         print('error semantico')
        #         exit()
        # elif node.getType() == 'fnum':
        #     if node.getVal() in symbols:
        #         symbols[node.getVal()] = node.getVal()
        #     else:
        #         print('error semantico')
        #         exit()
        # elif node.getType() == 'intdcl':
        #     if node.getVal() in symbols:
        #         print('error semantico')
        #         exit()
        #     else:
        #         symbols[node.getVal()] = 0
        # elif node.getType() == 'floatdcl':
        #     if node.getVal() in symbols:
        #         print('error semantico')
        #         exit()
        #     else:
        #         symbols[node.getVal()] = 0
        # elif node.getType() == '$':
        #     return
        # else:
        #     print('error sintactico')
        #     exit()




# ----------------------------------- Semantic analyzer code

def enterSymbol(name, type):
    if name in symbols:
        print('declaración duplicada')
        exit()
    else:
        symbols[name] = type

def lookupSymbol(name):
    if name in symbols:
        return symbols[name]
    else:
        print('símbolo no declarado')
        exit()

def convert(n: Node,t: Node):
    if isinstance(n, str):
        pass
    elif n.type == 'id':
        n = lookupSymbol(n.val)
    else: 
        n = n.type
    if isinstance(t, str):
        pass
    elif t.type == 'id':
        t = lookupSymbol(t.val)
    else:
        t = t.type
    if (n == 'fnum' and t == 'inum') or (n == 'float' and t == 'integer'):
        print('conversión ilegal')
        exit()
    else:
        if (n == 'inum' and t == 'fnum') or (n == 'integer' and t == 'float'):
            n.type = 'fnum'
            n['val'] = float(n['val']) # convert to float *-*
        else:
            return # no actions needed
    
def generalize(t1,t2): # returns type
    
    if t1 == 'fnum' or t2 == 'fnum' or t1 == 'float' or t2 == 'float':
        return 'fnum'
    else:
        return 'inum'

def consistent(c1: Node,c2: Node): # returns type
    if c1.type == 'id':
        c1.type = lookupSymbol(c1.val)
    if c2 == 'id':
        c2.type = lookupSymbol(c2.val)
    m = generalize(c1.type,c2.type)
    convert(c1,m)
    convert(c2,m)
    return m

def visit(n: Node):
    if n.NodeType == 'Computing': # generates code for plus and minus.
        n.type = consistent(n.child1(),n.child2())
    elif n.NodeType == 'Assigning': #  causes the expression to be evaluated
        n.type = convert(n.child1(),n.child2())
    elif n.NodeType == 'SymReferencing': # Symbol Reference. causes a value to be retrieved from the appropriate dc register and pushed onto the stack
        n.type = lookupSymbol(n.val)
    elif n.NodeType == 'IntConstant':
        n.type = 'inum'
    elif n.NodeType == 'FloatConstant':
        n.type = 'fnum'
    elif n.NodeType == 'SymDeclaring':
        if n.type == 'floatdcl':
            enterSymbol(n.val, 'float')
        elif n.type == 'intdcl':
            enterSymbol(n.val, 'integer')
        else:
            print('error semántico')
            exit()




def prog(tokens):
    root = Node("prog")
    root.addChilds(dcls(tokens))
    root.addChilds(stmts(tokens))
    visitNodes(root)
    return root


with open('input.txt') as f:
    content = f.read()
tokens = Tokens()
while not eof():
    tokens.append(scanner())
tokens.append(scanner())    
print(tokens)
root = prog(tokens)
print(str(root))
