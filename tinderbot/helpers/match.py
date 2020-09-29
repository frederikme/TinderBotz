from tinderbot.helpers.geomatch import Geomatch

# A match has the same information as a geomatch, except that you have a chatroom with an id
class Match(Geomatch):

    def __init__(self, name, chatid, age, bio, distance, image_urls, lat_scraper, long_scraper):

        self.chatid = chatid

        # invoking the __init__ of the parent class
        Geomatch.__init__(self, name, age, bio, distance, image_urls, lat_scraper=lat_scraper, long_scraper=long_scraper)

    def getChatID(self):
        return self.chatid

    def getDictionary(self):
        data = {
            "name": self.getName(),
            "age": self.getAge(),
            "bio": self.getBio(),
            "distance": self.getDistance(),
            "image_urls": self.image_urls,
            "images_by_hashes": self.images_by_hashes,
            "chatid": self.getChatID()
        }
        return data