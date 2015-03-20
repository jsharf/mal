import fileinput
import sys
import reader
import printer

def READ(x):
    return reader.read_str(x)

def EVAL(x):
    return x

def PRINT(x):
    return printer.pr_str(x)

def rep(x):
    return PRINT(EVAL(READ(x)))

def main():
    while(True):
        try:
            line = raw_input("user> ")
            sys.stdout.write(rep(line))
            sys.stdout.write("\n")
        except EOFError:
            sys.stdout.write("\n")
            sys.exit(0)

if __name__ == '__main__':
    main()
