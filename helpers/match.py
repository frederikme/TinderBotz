class Match:

    def __init__(self, name, mref):
        self.name = name
        self.id = mref.split("/")[-1]
        self.mref = mref

    def getName(self):
        return self.name

    def getID(self):
        return self.id

    def getMessagesReference(self):
        return self.mref

    def getImages(self):
        return None

    def getMessages(self):
        message = Message(self, "hahaha")
        return [message]


class Message:
    def __init__(self, sender, message):
        self.sender = sender
        self.message = message