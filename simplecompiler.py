import math
from numpy import mat
from Node import Node
from Tokens import Tokens

global content_index
global content
global tokens

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
    while peek().isdigit():
        ans['val'] = ans['val'] + advance()
    if peek() != '.':
        ans['type'] = 'inum'
    else: 
        ans['type'] = 'fnum'
        ans['val'] = ans['val'] + advance()
        while peek().isdigit():
            ans['val'] = ans['val'] + advance()
    return ans
        
def scanner():
    ans = {}
    while not eof() and (peek() == ' ' or peek() == '\n') : 
        advance()
    if eof():
        ans["type"] = '$'
    else:
        if peek().isdigit():
            ans = scan_digits()
        else:
            ch = advance()
            if ch.isalpha():
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

def match(ts,token):
    if ts.peek()['type'] == token:
        ts.advance()
    else:
        print('se esperaba un token')
        exit()

def Val(): 
    if tokens.peek()['type'] == 'inum':
        match(tokens,'inum')
    elif tokens.peek()['type'] == 'fnum':
        match(tokens,'fnum')
    else:
        print ('error semántico')
        exit()
    
def Expr():
    if tokens.peek()['type'] == 'id':
        match(tokens,'id')
        if tokens.peek()['type'] == 'plus':
            match(tokens,'plus')
            Expr()
            return
        elif tokens.peek()['type'] == 'minus':
            match(tokens,'minus')
            Expr()
            return
        else:
            return
    elif tokens.peek()['type'] in ('inum','fnum'):
        Val()
        if tokens.peek()['type'] == 'plus':
            match(tokens,'plus')
            Expr()
            return
        elif tokens.peek()['type'] == 'minus':
            match(tokens,'minus')
            Expr()
            return
        else:
            return
    else:
        print('error semántico')
        exit()
    
    


def dcl():
    match(tokens,'id')
    match(tokens,'id')

def dcls():
    # Dcls→Dcl Dcls
    # Dcls→ε
    if tokens.peek()['type'] == '$':
            match(tokens,'$')
            # print('$')
            exit()
    elif tokens.peek_front_behind()['type'] == 'assign':
        return
    elif tokens.peek()['type'] == 'id':
        dcl()
        dcls()
    else:
        print('error semántico')
        exit()


def stmt():
    # Stmt→id assign Expr

    
    # valid statements exmaples:
    # {'type': 'id', 'val': 'c'}, {'type': 'assign'}, {'type':  'id',           'val': 'a'},           {'type': 'plus'}, {'type': 'id', 'val': 'b'}
    # {'type': 'id', 'val': 'a'}, {'type': 'assign'}, {'val':   '3.1415929',    'type': 'fnum'}
    # {'type': 'id', 'val': 'b'}, {'type': 'assign'}, {'val':   '4',            'type': 'inum'}
    if tokens.peek()['val'] == 'p':
        match(tokens,'id')
        match(tokens,'id')
        return
    else:
        match(tokens,'id')
        match(tokens,'assign')

    if tokens.peek()['type'] in ('fnum', 'inum', 'id'):
        Expr()
    else:
        print('error semántico')
        exit()
    # print('stmt')

def stmts():
    # Stmts→Stmt Stmts
    # Stmts→ε
    if tokens.peek()['type'] in ('id', 'print'):
        stmt()
        stmts()
    else:
        if tokens.peek()['type'] == '$':
            match(tokens,'$')
            # print('$')
            exit()
        else:
            print('error semántico')
            exit()


        


# ----------------------------------- Parser code 
# def stmt():

# def stmts():

# def dcl(tokens):
#     if tokens.peek()['type'] == 'intdcl':
#         return intdcl(peek())
#     if tokens.peek()['type'] == 'floatdcl':
#         print('first')

# def intdcl():
#     advance()
#     return "intdcl" + peek()[] 

# def dcls(tokens):
#     dcl(tokens)
#     #dcls()

# def prog(tokens):
#     # root = prog
#     # root will be a tree of nodes
#     root = {}
#     root.append(dcls(tokens))
#     # root.append(stmts(tokens))


with open('input.txt') as f:
    content = f.read()
tokens = Tokens()

while not eof():
    tokens.append(scanner())
tokens.append(scanner())

# creating a array of arrays
# if the first token is an 'type' and the next token is an 'id' then create child node with the name of "[type] [id]"
print(tokens.myTokens())

def prog():
    dcls()
    stmts()

# def tree():
#     root = Node('root')

#     while tokens.peek_front_behind()['type'] != 'assign': 
#         root.add_child(Node(tokens.pop()['val'] + ' ' + tokens.pop()['val']))
    
#     return root

# print(tree().getNodes())

