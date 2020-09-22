from helpers.storage_helper import StorageHelper


class Geomatch:

    is_match = False

    def __init__(self, name, age, bio, distance, image_urls):
        self.name = name
        self.age = age
        self.bio = bio
        self.distance = distance
        self.image_urls = image_urls

        # create a unique chatid for this person
        self.id = "{}{}_{}".format(name, age, StorageHelper.id_generator(size=4))
        self.images_by_ids = []

    def storeLocal(self):
        if self.is_match:
            filename = 'matches'
        else:
            filename = 'geomatches'

        # store its images
        for url in self.image_urls:
            hashed_image = StorageHelper.storeImageAs(url=url, directory='data/{}/images'.format(filename))
            self.images_by_ids.append(hashed_image)

        # store its userdata
        StorageHelper.storeMatch(match=self, directory='data/{}'.format(filename), filename=filename)

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
            "images_by_ids": self.images_by_ids,
        }
        return data