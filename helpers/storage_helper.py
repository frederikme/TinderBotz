import string
import random
import os
import json
import time

import urllib.request
from PIL import Image

class StorageHelper:

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def storeImageAs(url, image_name, directory, amount_of_attempts=1):
        if not os.path.exists(directory):
            os.makedirs(directory)

        # make 'undetectable' header, doesnt completly work
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        try:
            request_ = urllib.request.Request(url, None, headers)  # The assembled request
            response = urllib.request.urlopen(request_)  # store the response

        except Exception as e:
            print(e)
            sleepy_time = amount_of_attempts*20
            print("Will sleep for now try again in {} seconds".format(sleepy_time))
            time.sleep(sleepy_time)
            return StorageHelper.storeImageAs(url, image_name, directory, amount_of_attempts+1)

        f = open("{}.webp".format(os.getcwd(), directory, image_name), 'wb')
        f.write(response.read())
        f.close()

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
        except IOError:
            print("Could not read file, starting from scratch")
            data = {}

        # Add some data
        data[match.getID()] = match.getDictionary()

        with open(filepath, 'w+') as file:
            json.dump(data, file)