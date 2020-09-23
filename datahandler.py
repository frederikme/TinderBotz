from analytics import Analytics

analytics = Analytics(path_file='data/geomatches/geomatches.json')

print("You scraped {} profiles!".format(analytics.getAmountOfProfiles()))
print("The name {} occurred the most, namely {} times".format(analytics.getMostCommonName()[0], analytics.getMostCommonName()[1]))
print("The average age of the profiles is {}".format(analytics.getAverageAge()))
print("The average distance between you and the profiles is {} km".format(analytics.getAverageDistance()))
print("The average profile has {} images".format(analytics.getAverageAmountOfImages()))
