import fileinput
import sys
import reader
import printer

repl_env =  {
        '+': lambda a,b: a+b,
        '-': lambda a,b: a-b,
        '*': lambda a,b: a*b,
        '/': lambda a,b: int(a/b)
}

class EvalError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class LookupError(EvalError):
    def __init__(self, value):
        super(LookupError, self).__init__(value)

def eval_ast(ast, env):
    if (isinstance(ast, reader.Symbol)):
        if (ast.name in env):
            return env[ast.name]
        else:
            raise LookupError("Symbol {0} is not in the environment".format(ast))
    elif (isinstance(ast, reader.GenericMap)):
        listtype = type(ast)
        return listtype(map(lambda x: EVAL(x, env), ast.items))
    else:
        return ast

def READ(x):
    return reader.read_str(x)

def EVAL(x, env):
    if (isinstance(x, reader.List)):
        evaluated_list = eval_ast(x, env)
        fun = evaluated_list[0]
        args = evaluated_list[1:]
        return fun(*args)
    else:
        return eval_ast(x, env)

def PRINT(x):
    return printer.pr_str(x)

def rep(x):
    return PRINT(EVAL(READ(x), repl_env))

def main():
    while(True):
        try:
            line = raw_input("user> ")
            sys.stdout.write(rep(line))
            sys.stdout.write("\n")
        except EOFError:
            sys.stdout.write("\n")
            sys.exit(0)
        except EvalError as err:
            sys.stderr.write(str(err) + "\n")
            pass

if __name__ == '__main__':
    main()
