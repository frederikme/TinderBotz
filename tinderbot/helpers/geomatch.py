from tinderbot.helpers.storage_helper import StorageHelper

class Geomatch:

    def __init__(self, name, age, bio, distance, image_urls):
        self.name = name
        self.age = age
        self.bio = bio
        self.distance = distance
        self.image_urls = image_urls

        # create a unique chatid for this person
        self.id = "{}{}_{}".format(name, age, StorageHelper.id_generator(size=4))
        self.images_by_hashes = []

    def getName(self):
        return self.name

    def getAge(self):
        return self.age

    def getBio(self):
        return self.bio

    def getDistance(self):
        return self.distance

    def getImageURLS(self):
        return self.image_urls

    def getID(self):
        return self.id

    def getDictionary(self):
        data = {
            "name": self.getName(),
            "age": self.getAge(),
            "bio": self.getBio(),
            "distance": self.getDistance(),
            "image_urls": self.image_urls,
            "images_by_hashes": self.images_by_hashes,
        }
        return data