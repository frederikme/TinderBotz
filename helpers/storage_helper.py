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
            sleepy_time = amount_of_attempts*30
            print("Will sleep for now try again in {} seconds".format(sleepy_time))
            time.sleep(sleepy_time)
            if amount_of_attempts < 5:
                return StorageHelper.storeImageAs(url, image_name, directory, amount_of_attempts+1)
            else:
                # Settle with the fact this one won't be stored
                error = "Amount of attempts exceeded in storage_helper\n" \
                        "attempting to get url: {}\n" \
                        "resulted in error: {}".format(url, e)
                StorageHelper.logError(error)
                return

        if ".jpg" in url:
            f = open("{}/{}/{}.jpg".format(os.getcwd(), directory, image_name), 'wb')
            f.write(response.read())
            f.close()

        elif '.webp' in url:
            # save as a temporary file
            f = open("{}.webp".format(image_name), 'wb')
            f.write(response.read())
            f.close()

            # open the file and convert the file to jpeg
            im = Image.open("{}.webp".format(image_name)).convert("RGB")
            # save the jpeg file in the directory it belongs
            im.save("{}/{}/{}.jpg".format(os.getcwd(), directory, image_name), "jpeg")

            # remove the temporary file
            os.remove("{}.webp".format(image_name))

        else:
            print("URL of image cannot be saved!")
            print("URL DOES NOT CONTAIN .JPG OR .WEBP EXTENSION")
            print(url)

            error = "URL DOES NOT CONTAIN .JPG OR .WEBP EXTENSION: {}\n" \
                    "Please add extension needed in storage_helper".format(url)

            StorageHelper.logError(error)

    @staticmethod
    def storeMatch(match, directory, filename):

        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = directory + "/{}.json".format(filename)

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

    @staticmethod
    def logError(error):
        # write to error logfile
        with open("ERRORS.txt", "w+") as text_file:
            text_file.write(error)