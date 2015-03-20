import reader

def pr_list(l):
    tokens = map(pr_str, l)
    return ' '.join(tokens)

def pr_str(ast, indent=0):
    if (isinstance(ast, list)):
        return '(' + pr_list(ast) + ')'
    elif (isinstance(ast, reader.GenericList)):
        (open_token, close_token) = ast.separators
        return open_token + pr_list(ast.items) + close_token
    elif (isinstance(ast, reader.Symbol)):
        return ast.name
    elif (isinstance(ast, reader.String)):
        return '"' + ast.val + '"'
    elif (isinstance(ast, bool)):
        return "true" if (ast) else "false"
    elif (isinstance(ast, reader.ReadError)):
        if (ast.message[1] == None):
            return '\t'*indent + ast.message[0]
        else:
            return '\t'*indent + ast.message[0] + "\n" + pr_str(ast.message[1], indent + 1)
    elif (ast == None):
        return "nil"
    else:
        return str(ast)
