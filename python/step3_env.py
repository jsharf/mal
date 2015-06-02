import fileinput
import sys
import reader
import printer
import env
import pdb
from optparse import OptionParser

verbosity = False

repl_env = env.Environment()
repl_env.set('+', lambda a,b: a+b)
repl_env.set('-', lambda a,b: a-b)
repl_env.set('*', lambda a,b: a*b)
repl_env.set('/', lambda a,b: int(a/b))

def verbosePrint(x):
    global verbosity
    if (verbosity):
        print(x)

class EvalError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class LookupError(EvalError):
    def __init__(self, value):
        super(LookupError, self).__init__(value)

def eval_ast(ast, e):
    if (isinstance(ast, reader.Symbol)):
        value = e.get(ast.name)
        if (value != None):
            return value
        else:
            raise LookupError("Symbol {0} is not in the environment".format(ast))
    elif (isinstance(ast, reader.GenericMap)):
        listtype = type(ast)
        return listtype(map(lambda x: EVAL(x, e), ast.items))
    else:
        return ast

def READ(x):
    return reader.read_str(x)

def EVAL(x, e):
    if (isinstance(x, reader.List)):
        head = x[0]
        if (head.name == 'def!'):
            value = EVAL(x[2], e)
            repl_env.set(x[1].name, value)
            verbosePrint("{0} : {1}".format(x[1], repl_env.get(x[1].name)))
            return value
        elif (head.name == 'let*'):
            if (len(x.items) != 3):
                raise EvalError("let* statement may only have 3 arguments. (let* (bindings-list) (body))")
            newenv = env.Environment(repl_env)
            for i in range(0, len(x[1].items), 2):
                newenv.set(x[1][i].name, EVAL(x[1][i+1], newenv))
            verbosePrint("Let statement env: {0}".format(newenv))
            return EVAL(x[2], newenv)
        else:
            evaluated_list = eval_ast(x, e)
            fun = evaluated_list[0]
            args = evaluated_list[1:]
            return fun(*args)
    else:
        return eval_ast(x, e)

def PRINT(x):
    return printer.pr_str(x)

def rep(x):
    return PRINT(EVAL(READ(x), repl_env))

def main():
    global verbosity
    parser = OptionParser()
    parser.add_option("-v", "--verbose",
            action="store_true", dest="verbose",
            default=False,
            help="print extra log messages to stdout")
    (options, args) = parser.parse_args()
    verbosity = options.verbose
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
        except:
            print("Unexpected error:", sys.exc_info()[0])
            pass

if __name__ == '__main__':
    main()
