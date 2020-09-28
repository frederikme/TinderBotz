import os, json, math
from wordcloud import WordCloud
import geoplotlib
from geoplotlib.utils import read_csv


class Analytics:

    main_directory = "../data/geomatches"
    location_data = "../data/locationdata.csv"

    def __init__(self, path_file):
        self.path_file = path_file
        with open(path_file) as f:
            self.data = json.load(f)

    def getAmountOfProfiles(self):
        return len(self.data)

    def getMostCommonName(self):
        temp_data = {}

        # count how many times the names occurs
        for id in self.data:
            name = self.data[id]["name"]
            if name in temp_data:
                temp_data[name] += 1
            else:
                temp_data[name] = 1

        sorted_data = sorted(temp_data.items(), key=lambda x: x[1], reverse=True)

        return sorted_data[0]

    def getAverageAge(self):
        age_counter = 0
        for id in self.data:
            age_counter += self.data[id]["age"]

        return age_counter/self.getAmountOfProfiles()

    def getAverageDistance(self):
        distance_counter = 0
        dont_count_profiles = 0
        for id in self.data:
            try:
                distance_counter += self.data[id]['distance']['radius']
            except:
                # age could not be converted to int"
                dont_count_profiles += 1

        return distance_counter / (self.getAmountOfProfiles() - dont_count_profiles)

    def getAverageAmountOfImages(self):
        amount = 0

        for id in self.data:
            amount += len(self.data[id]['images_by_hashes'])

        return amount / self.getAmountOfProfiles()

    def getWordCloudOfNames(self, age="all"):
        names = ""
        directory = '{}/wordclouds'.format(self.main_directory)

        if not os.path.exists(directory):
            os.makedirs(directory)

        # count how many times the names occurs
        for id in self.data:
            if isinstance(age, int):
                if not age == self.data[id]["age"]:
                    continue
            names += " {}".format(self.data[id]["name"])

        # Generate a word cloud image
        wordcloud = WordCloud().generate(names)

        # The pil way (if you don't have matplotlib)
        image = wordcloud.to_image()
        image.show()
        image.save("{}/{}/{}.jpg".format(os.getcwd(), directory, "name_of_age_{}".format(age)), "png")

    def getWordCloudOfBio(self, age="all"):
        bios = ""
        directory = '{}/wordclouds'.format(self.main_directory)

        ignore_list = ["een", "de", "le", "la", "het", "ben", "suis", "ook", "maar", "en", "et", "maar"]

        if not os.path.exists(directory):
            os.makedirs(directory)

        # count how many times the names occurs
        for id in self.data:
            if isinstance(age, int):
                if not age == self.data[id]["age"]:
                    continue

            bio = self.data[id]["bio"]

            if bio is None:
                continue

            bio = bio.lower()
            for element in ignore_list:
                bio = bio.replace(element, '')

            bios += " {}".format(bio)

        # Generate a word cloud image
        wordcloud = WordCloud().generate(bios)

        # The pil way (if you don't have matplotlib)
        image = wordcloud.to_image()
        image.show()
        image.save("{}/{}/{}.jpg".format(os.getcwd(), directory, "bio_of_age_{}".format(age)), "png")

    def getDotMapOfMatches(self):
        #self.updateLocationDataFile()

        data = read_csv(self.location_data)
        print(data)
        geoplotlib.dot(data)
        geoplotlib.show()

    def getHistogramOfMatches(self):
        #self.updateLocationDataFile()

        data = read_csv(self.location_data)
        print(data)

        geoplotlib.hist(data, colorscale='sqrt', binsize=8)
        geoplotlib.show()

    def getHeatmapOfMatches(self):
        #self.updateLocationDataFile()

        data = read_csv(self.location_data)
        print(data)

        geoplotlib.kde(data, bw=[5, 5])
        geoplotlib.show()

    def getDelaunayTriangulation(self):
        #self.updateLocationDataFile()

        data = read_csv(self.location_data)
        print(data)

        geoplotlib.delaunay(data, cmap='hot_r')
        geoplotlib.show()

    def updateLocationDataFile(self):
        '''
        import random

        with open(self.location_data, "w+") as locations_file:
            locations_file.write('name,lat,lon\n')

            # populate some higher
            for x in range(3000):
                lat = 50.87959 + random.random()
                lon = 4.70093 + (random.randint(-10000, 10000) / 10000)
                line = "Location,{},{}\n".format(lat, lon)
                locations_file.write(line)

            # populate some lower
            for x in range(1000):
                lat = 50.87959 - random.random()
                lon = 4.70093 + (random.randint(-10000, 10000) / 10000)
                line = "Location,{},{}\n".format(lat, lon)
                locations_file.write(line)

            locations_file.close()
        '''
        # look for two same users by comparing their image hashes
        # convert distance into a function of a circle
        
        # bad timecomplexity but will do in a minute or two, since data is not enormously large
        lines = self.crossMatchTest()
        with open(self.location_data, "w+") as locations_file:
            locations_file.write('name,lat,lon\n')

            for line in lines:
                locations_file.write(line)

            locations_file.close()

    def crossMatchTest(self):
        users = []
        lines = []

        # bad timecomplexity but will do in a minute or two, since data is not enormously large
        for index, id in enumerate(self.data):
            if index % 500 == 0:
                print("{} of the {}".format(index + 1, len(self.data)))
            user = self.data[id]
            hashes = user['images_by_hashes']
            for id_2 in self.data:
                if id != id_2:
                    user_2 = self.data[id_2]
                    hashes_2 = user_2['images_by_hashes']
                    if Analytics.haveCommonElement(hashes, hashes_2) is not None:
                        users.append((user, user_2))
                        # -> will return locations of intersections
                        intersections = Analytics.getIntersections(
                            x0=user['distance']['scrapers_latitude'], y0=user['distance']['scrapers_longitude'],
                            r0=user['distance']['radius'],
                            x1=user_2['distance']['scrapers_latitude'], y1=user_2['distance']['scrapers_longitude'],
                            r1=user_2['distance']['radius']
                        )
                        # add both intersections to the location file
                        # (we actually need 3 different scrapes of a user to determine their exact location)
                        if intersections is not None:

                            if Analytics.isValidLocation(intersections[0], intersections[1]):
                                line = "Location,{},{}\n".format(intersections[0], intersections[1])
                                lines.append(line)

                            if Analytics.isValidLocation(intersections[2], intersections[3]):
                                line2 = "Location,{},{}\n".format(intersections[2], intersections[3])
                                lines.append(line2)

        print(len(users))
        return lines

    '''
    def modify(self):
        for id in self.data:
            self.data[id]['distance']['radius'] = int(self.data[id]['distance']['radius'])

        with open(self.path_file, 'w') as f:
            json.dump(self.data, f)
    '''
    @staticmethod
    def haveCommonElement(list1, list2):
        # traverse in the 1st list
        for x in list1:
            # traverse in the 2nd list
            for y in list2:

                # if one common
                if x == y:
                    return x

        return None

    @staticmethod
    def isValidLocation(lat, long):
        if abs(lat) > 90 or abs(long) > 180:
            return False
        else:
            return True

    @staticmethod
    def getIntersections(x0, y0, r0, x1, y1, r1):
        # circle 1: (x0, y0), radius r0
        # circle 2: (x1, y1), radius r1
        try:
            d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

            # non intersecting
            if d > r0 + r1:
                return None
            # One circle within other
            if d < abs(r0 - r1):
                return None
            # coincident circles
            if d == 0 and r0 == r1:
                return None
            else:
                a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
                h = math.sqrt(r0 ** 2 - a ** 2)
                x2 = x0 + a * (x1 - x0) / d
                y2 = y0 + a * (y1 - y0) / d
                x3 = x2 + h * (y1 - y0) / d
                y3 = y2 - h * (x1 - x0) / d

                x4 = x2 - h * (y1 - y0) / d
                y4 = y2 + h * (x1 - x0) / d

                return (x3, y3, x4, y4)
        except:
            print(x0, y0, r0, x1, y1, r1)
            assert False