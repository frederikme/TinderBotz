import string
import random
import os
import json
import time

import urllib.request
from PIL import Image
import hashlib


class StorageHelper:

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    # Returns hash value of the image saved by the url given
    @staticmethod
    def store_image_as(url, directory, amount_of_attempts=1):
        if not os.path.exists(directory):
            os.makedirs(directory)

        # make 'undetectable' header to avoid being seen as scraper
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
            if amount_of_attempts < 20:
                sleepy_time = amount_of_attempts * 30
                print("Attempt number {}: sleeping for {} seconds ...".format(amount_of_attempts, sleepy_time))
                time.sleep(sleepy_time)
                return StorageHelper.store_image_as(url, directory, amount_of_attempts + 1)
            else:
                # Settle with the fact this one won't be stored
                error = "Amount of attempts exceeded in storage_helper\n" \
                        "attempting to get url: {}\n" \
                        "resulted in error: {}".format(url, e)
                print(error)
                return None

        temp_name = "temporary"

        if ".jpg" in url:
            f = open("{}/{}/{}.jpg".format(os.getcwd(), directory, temp_name), 'wb')
            f.write(response.read())
            f.close()

        elif '.webp' in url:
            # save as a temporary file
            f = open("{}.webp".format(temp_name), 'wb')
            f.write(response.read())
            f.close()

            # open the file and convert the file to jpeg
            im = Image.open("{}.webp".format(temp_name)).convert("RGB")
            # save the jpeg file in the directory it belongs
            im.save("{}/{}/{}.jpg".format(os.getcwd(), directory, temp_name), "jpeg")

            # remove the temporary file
            os.remove("{}.webp".format(temp_name))

        else:
            print("URL of image cannot be saved!")
            print("URL DOES NOT CONTAIN .JPG OR .WEBP EXTENSION")
            print(url)

            error = "URL DOES NOT CONTAIN .JPG OR .WEBP EXTENSION: {}\n" \
                    "Please add extension needed in storage_helper".format(url)
            print(error)

        # rename saved image to their hashvalue, so it's easy to compare (hashes of) images later on
        im = Image.open('{}/{}/{}.jpg'.format(os.getcwd(), directory, temp_name))
        hashvalue = hashlib.md5(im.tobytes()).hexdigest()

        # check if image already exists
        if not os.path.isfile('{}/{}/{}.jpg'.format(os.getcwd(), directory, hashvalue)):
            os.rename('{}/{}/{}.jpg'.format(os.getcwd(), directory, temp_name),
                      '{}/{}/{}.jpg'.format(os.getcwd(), directory, hashvalue))

        print("Image saved as {}/{}/{}.jpg".format(os.getcwd(), directory, hashvalue))

        return hashvalue

    @staticmethod
    def store_match(match, directory, filename):

        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = directory + "/{}.json".format(filename)

        try:
            with open(filepath, "r", encoding='utf-8') as fp:
                data = json.load(fp)
        except IOError:
            print("Could not read file, starting from scratch")
            data = {}

        data[match.get_id()] = match.get_dictionary()

        with open(filepath, 'w+', encoding="utf-8") as file:
            json.dump(data, file)
