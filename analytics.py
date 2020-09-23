import json


class Analytics:

    def __init__(self, path_file):
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
        #print(sorted_data)

        # check which one is most common
        most_common = None
        amount = None
        for name in temp_data:
            if most_common is None:
                most_common = name
            else:
                if temp_data[name] > temp_data[most_common]:
                    most_common = name
                    amount = temp_data[name]

        return most_common, amount

    def getAverageAge(self):
        age_counter = 0
        dont_count_profiles = 0
        for id in self.data:
            try:
                age_counter += int(self.data[id]["age"])
            except:
                # age could not be converted to int"
                dont_count_profiles += 1

        return age_counter/(self.getAmountOfProfiles()-dont_count_profiles)

    def getAverageDistance(self):
        distance_counter = 0
        dont_count_profiles = 0
        for id in self.data:
            try:
                distance_counter += int(self.data[id]["distance"])
            except:
                # age could not be converted to int"
                dont_count_profiles += 1

        return distance_counter / (self.getAmountOfProfiles() - dont_count_profiles)

    def getAverageAmountOfImages(self):
        amount = 0

        for id in self.data:
            amount += len(self.data[id]['images_by_hashes'])

        return amount / self.getAmountOfProfiles()



