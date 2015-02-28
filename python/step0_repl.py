import fileinput
import sys

def READ(x):
    return x

def EVAL(x):
    return x

def PRINT(x):
    return x

def rep(x):
    return PRINT(EVAL(READ(x)))

def main():
    try:
        while(True):
            line = raw_input("mal>>")
            sys.stdout.write(rep(line))
            sys.stdout.write("\n")
    except EOFError:
        sys.stdout.write("\n")
        sys.exit(0)

if __name__ == '__main__':
    main()
