class Sample(object):

    def __init__(self, result, *args):
        self.result = result
        self.attri = []
        for arg in args:
            self.attri.append(arg)
        
    def print(self):
        print(self.result, self.attri)

    def getAttriNum(self):
        return self.attri.

    def getAttriOf(self, index):
        return self.attri[index]
