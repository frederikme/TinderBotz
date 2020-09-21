import string
import random
import os
import json

import urllib.request
from PIL import Image


class StorageHelper:

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def storeImageAs(url, image_name, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

        urllib.request.urlretrieve(url, "{}.webp".format(image_name))

        im = Image.open("{}.webp".format(image_name)).convert("RGB")
        im.save("{}/{}/{}.jpg".format(os.getcwd(), directory, image_name), "jpeg")

        os.remove("{}.webp".format(image_name))

    @staticmethod
    def storeMatch(match, directory, filename):

        if not os.path.exists(directory):
            os.makedirs(directory)


        filepath = directory + "/{}.json".format(filename)

        print("Reading %s" % filepath)
        try:
            with open(filepath, "r") as fp:
                data = json.load(fp)
            print("Data: %s" % data)
        except IOError:
            print("Could not read file, starting from scratch")
            data = {}

        # Add some data
        data[match.getID()] = match.getDictionary()

        with open(filepath, 'w+') as file:
            json.dump(data, file)
