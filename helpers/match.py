class Match:

    def __init__(self, name, mref):
        self.name = name
        self.id = mref.split("/")[-1]
        self.mref = mref.split(".com")[-1]

    def getName(self):
        return self.name

    def getID(self):
        return self.id

    def getMRef(self):
        return self.mref

