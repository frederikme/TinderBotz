from helpers.geomatch import Geomatch

# A match has the same information as a potential match, except that you have a chatroom with an id together
class Match(Geomatch):

    def __init__(self, name, chatid, age, bio, distance, image_urls):

        self.chatid = chatid
        self.is_match = True

        # invoking the __init__ of the parent class
        Geomatch.__init__(self, name, age, bio, distance, image_urls)

    def getChatID(self):
        return self.chatid

    def getDictionary(self):
        data = {
            "name": self.getName(),
            "age": self.getAge(),
            "bio": self.getBio(),
            "distance": self.getDistance(),
            "image_urls": self.image_urls,
            "images_by_ids": self.images_by_ids,
            "chatid": self.chatid
        }
        return data