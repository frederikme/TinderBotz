# TinderBot

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://user-images.githubusercontent.com/60892381/94200140-384a7f80-feba-11ea-8fcf-ec4507eda017.jpg">
    <img src="https://user-images.githubusercontent.com/60892381/94200140-384a7f80-feba-11ea-8fcf-ec4507eda017.jpg">
  </a>

  <h3 align="center">TINDERBOT AND ANALYSIS OF THEIR DATA</h3>

  <p align="center">
    Tinder web automation and scraper.
    <br />
    <a href="https://github.com/frederikme/TinderBot/blob/master/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#demo-of-tinderbot">View Demo</a>
    ·
    <a href="https://github.com/frederikme/TinderBot/issues/new">Report Bug</a>
    ·
    <a href="https://github.com/frederikme/TinderBot/issues/new">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage of Tinderbot](#usage-of-tinderbot)
  * [DEMO of Tinderbot](#demo-of-tinderbot)
* [Usage of Data Analysis](#usage-of-data-analysis)
  * [DEMO of Data Analysis](#demo-of-data-analysis)
* [Support the Repository](#support-the-repository)

<!-- ABOUT THE PROJECT -->
## About the Project
This project started with the motivation of learning web automation further and scraping with Python.</br>
After succesfully creating a bot that could:</br>

* Open a browser and login to Tinder.com
* Accept all notifications and dismiss pop-ups
* Swiping x amount of profiles left or right
* Scraping data of the profiles displayed, including, yet not limited to, name, age, bio, images, ...
* Sending personalized messages to your matches
* Sending you social media cards, like Instagram, Snapchat, Phonenumber and Facebook
* Sending GIFS and songs
* Unmatching

I decided to add some data analysis and plotting of data to the project. Star this project to keep up to date! :)

### Built with

* [Python](https://www.python.org/)
* [Selenium](https://selenium.dev)
* [Wordcloud](https://github.com/amueller/word_cloud)
* [Geoplotlib](https://github.com/andrea-cuttone/geoplotlib)

<!-- Getting Started -->
## Getting Started
### Prerequisites

- Environment running python 3.x
- Tinder account with Google or Facebook login enabled

### Installation
1. Clone or download the project
2. Install the required packages
```
pip3 install -r requirements.txt
```

## Usage of Tinderbot
Features of Tinderbot can be found here: [Tinderbot features](https://github.com/frederikme/TinderBot/blob/master/TINDERBOTDOC.md)</br>
Quickstart script can be found here: [quickstart_tinderbot.py](https://github.com/frederikme/TinderBot/blob/master/quickstart_tinderbot.py)

### DEMO of Tinderbot
TODO: Add demo video's and gifs :)

## Usage of Data Analysis
***Make sure you already scraped some data!***</br>
Features of the Data Analysis can be found here: [Analysis features](https://github.com/frederikme/TinderBot/blob/master/ANALYTICSDOC.md)</br>
Quickstart script can be found here: [quickstart_analytics.py](https://github.com/frederikme/TinderBot/blob/master/quickstart_analytics.py)

### DEMO of Data Analysis
#### Terminal as printout
<img src="https://user-images.githubusercontent.com/60892381/94479341-f03a9e00-01d4-11eb-9a10-70a8aa8208ea.png">

#### Wordcloud of most common names
<a href="https://github.com/frederikme/TinderBot/blob/master/data/geomatches/wordclouds/name_of_age_all.jpg">
    <img src="https://github.com/frederikme/TinderBot/blob/master/data/geomatches/wordclouds/name_of_age_all.jpg">
</a>

#### Heatmap of the geomatches location 
Locations of users is based on multiple scrapes from different locations by taking the intersections of the circles (based on the 'distance away').
<a href="https://github.com/frederikme/TinderBot/blob/master/data/geomatches/maps/Heatmap.png">
    <img src="https://github.com/frederikme/TinderBot/blob/master/data/geomatches/maps/Heatmap.png">
 </a>

## Support the Repository
Feel free to make a pull request and contribute to this project.</br>
If you feel like buying me a drink:
* [Paypal](https://paypal.me/frederikmees)

