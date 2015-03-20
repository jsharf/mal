import re
import pdb

class Symbol:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return repr(self.name)

class String:
    def __init__(self, val):
        self.val = val

class Reader():
    def __init__(self, tokens):
        self.pos = 0
        self.tokens = tokens
    def next(self):
        if (self.pos >= len(self.tokens)):
            return None
        token = self.tokens[self.pos]
        self.pos += 1
        return token
    def peek(self):
        if (self.pos >= len(self.tokens)):
            return None
        return self.tokens[self.pos]

class ReadError():
    def __init__(self, msg, err=None):
        self.message = (msg, err) 

class GenericList(object):
    separators = (None, None)
    def __init__(self, l):
        self.items = l
    def __getitem__(self, key):
        return self.items[key]
    def __setitem__(self, key, val):
        self.items[key] = val
        return self.items[key]

class Vector(GenericList):
    separators = ('[', ']')
    def __init__(self, l):
        super(Vector, self).__init__(l)
class Hash(GenericList):
    separators = ('{', '}')
    def __init__(self, l):
        super(Hash, self).__init__(l)
class List(GenericList):
    separators = ('(', ')')
    def __init__(self, l):
        super(List, self).__init__(l)

LIST_TYPES = [Vector, Hash, List]

def isSeparatorOf(token, typelist):
    for typeI in typelist:
        if token == typeI.separators[0]:
            return typeI
    return False

class Comment(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def read_form(reader):
    token = reader.peek()
    if (isSeparatorOf(token, LIST_TYPES)):
        return read_list(reader)
    elif (token == "'"):
        reader.next()
        return ["quote",  read_form(reader)]
    elif (token == "`"):
        reader.next()
        return ["quasiquote",  read_form(reader)]
    elif (token == "~"):
        reader.next()
        return ["unquote",  read_form(reader)]
    elif (token == "~@"):
        reader.next()
        return ["splice-unquote",  read_form(reader)]
    elif (token == "@"):
        reader.next()
        return ["deref", read_form(reader)]
    elif (len(token) >= 1 and token[0] == ";"):
        raise Comment(token)
    else:
        return read_atom(reader)

def read_list(reader):
    # read the separator, use it to get the type of this list
    token = reader.next()
    classType = isSeparatorOf(token, LIST_TYPES)
    if (classType == False):
        return ReadError("Expected a list separator, got {0}".format(token))
    (open_token, close_token) = classType.separators
    lookahead = reader.peek()
    s_expr = []
    while lookahead != close_token:
        form = read_form(reader)
        if (isinstance(form, ReadError)):
            return ReadError(
                    "Error: expected s_expression element, received error", form)
        s_expr.append(form)
        lookahead = reader.peek()
        if (lookahead == None):
            return ReadError("Error: Expected {0}, got EOF".format(close_token))
    # burn the close_token
    reader.next()
    return classType(s_expr)

def read_atom(reader):
    token = reader.next()
    if token.isdigit():
        return int(token)
    elif token == "nil":
        return None
    elif token == "true":
        return True
    elif token == "false":
        return False
    elif len(token) > 0 and token[0] == "\"":
        return String(token[1:-1])
    else:
        return Symbol(token)

def tokenizer(string):
    regexp = r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)"""
    r = re.compile(regexp)
    return r.findall(string)

def read_str(string):
    try:
        tokens = tokenizer(string)
        malreader = Reader(tokens)
        return read_form(malreader)
    except Comment:
        return []

