
class Environment(object):
    def __init__(self, outer=None):
        self.data = {}
        self.outer = outer
    def clone(self):
        newenv = Environment()
        newenv.data = self.data
        if (self.outer) != None:
            newenv.outer = self.outer.clone()
        else:
            newenv.outer = None
        return newenv
    def set(self, symbol, value):
        self.data[symbol] = value
    def find(self, symbol):
        if (symbol in self.data):
            return self
        else:
            if (self.outer != None):
                return self.outer.find(symbol)
            else:
                return None
    def get(self, symbol):
        env = self.find(symbol)
        if (env == None):
            raise LookupError("Value {0} not found in current environment".format(symbol))
        return env.data[symbol]

Env = Environment()

