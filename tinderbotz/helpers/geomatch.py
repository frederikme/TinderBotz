from tinderbotz.helpers.storage_helper import StorageHelper

class Geomatch:

    def __init__(self, name, age, work, study, home, gender, bio, lifestyle, basics, anthem, looking_for = None, distance = None, passions = None, image_urls = None, instagram = None):
        self.name = name
        self.age = age
        self.work = work
        self.study = study
        self.home = home
        self.gender = gender
        self.passions = passions
        self.bio = bio
        self.lifestyle = lifestyle
        self.basics = basics
        self.anthem = anthem
        self.looking_for = looking_for
        self.distance = distance
        self.image_urls = image_urls
        self.instagram = instagram

        # create a unique id for this person
        self.id = "{}{}_{}".format(name, age, StorageHelper.id_generator(size=4))
        self.images_by_hashes = []

    def get_images_ai_data(self):
        images_ai_data = []
        for image in self.image_urls:
            for image_ai_data in self._get_image_ai_data(image):
                images_ai_data.append(image_ai_data)
        return images_ai_data

    def _get_image_ai_data(self, image_url):
        from PIL import Image
        from deepface import DeepFace
        from io import BytesIO
        import requests
        import cv2
        import numpy as np
        resp = requests.get(image_url, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return DeepFace.analyze(image, enforce_detection=False)

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_work(self):
        return self.work

    def get_study(self):
        return self.study

    def get_home(self):
        return self.home

    def get_gender(self):
        return self.gender

    def get_passions(self):
        return self.passions

    def get_bio(self):
        return self.bio

    def get_lifestyle(self):
        return self.lifestyle

    def get_basics(self):
        return self.basics

    def get_anthem(self):
        return self.anthem
    
    def get_looking_for(self):
        return self.looking_for

    def get_distance(self):
        return self.distance

    def get_image_urls(self):
        return self.image_urls

    def get_instagram(self):
        return self.instagram

    def get_id(self):
        return self.id

    def get_dictionary(self):
        data = {
            "name": self.get_name(),
            "age": self.get_age(),
            "work": self.get_work(),
            "study": self.get_study(),
            "home": self.get_home(),
            "gender": self.gender,
            "bio": self.get_bio(),
            "distance": self.get_distance(),
            "basics": self.get_basics(),
            "lifestyle": self.get_lifestyle(),
            "passions": self.get_passions(),
            "anthem": self.get_anthem(),
            "looking_for": self.get_looking_for(),
            "image_urls": self.image_urls,
            "images_by_hashes": self.images_by_hashes,
            "instagram": self.get_instagram(),
        }
        return data
