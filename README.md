# TinderBot

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://user-images.githubusercontent.com/60892381/94200140-384a7f80-feba-11ea-8fcf-ec4507eda017.jpg">
    <img src="https://user-images.githubusercontent.com/60892381/94200140-384a7f80-feba-11ea-8fcf-ec4507eda017.jpg">
  </a>

  <h3 align="center">TINDERBOT AND PROFILESCRAPER</h3>

  <p align="center">
    Tinder web automation and scraper.
    <br />
    <a href="https://github.com/frederikme/TinderBot/blob/master/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#demonstration">View Demo</a>
    ·
    <a href="https://github.com/frederikme/TinderBot/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
    ·
    <a href="https://github.com/frederikme/TinderBot/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage-of-tinderbot)
  * [Features](DOCUMENTATION.md)
  * [Demo](#demonstration)
* [Coming Soon Features](#coming-soon-features)
  * [Picture is Worth a Thousand Words](#a-picture-is-worth-a-thousand-words)
  * [Finally a Worthy Opponent](#finally-a-worthy-opponent)
  * [Integrating Scraping](#integrating-scraping-better)
  * [Statistics Overview](#because-we-all-like-some-juicy-statistics)
* [Support the Repository](#support-the-repository)

<!-- ABOUT THE PROJECT -->
## About the Project
**IMPORTANT: Starring the project indicates shows your appreciation and will result in new features being added!**</br>
</br>
This project started with the motivation of learning web automation further and scraping with Python.</br>
I managed to succesfully create a bot that could: </br>

* Open a browser and login to Tinder.com
* Setting a custom location for **FREE** (which is normally a paid-for-***Tinder Plus***-feature)
* Setting profile settings and preferences, such as distance radius, minimum and maximum age, sexuality.
* Accept all notifications and dismiss pop-ups
* Swiping x amount of profiles left or right
* Scraping data of the profiles displayed, including, yet not limited to, name, age, bio, images, ...
* Sending personalized messages to your matches
* Sending you social media cards, like Instagram, Snapchat, Phonenumber and Facebook
* Sending GIFS and songs
* Unmatching

If you feel like diving right in, the [quickstart.py](https://github.com/frederikme/TinderBot/blob/master/quickstart.py) will help you be right on track.</br>
*Feel free to make a pull request and contribute to this project!*</br>
</br>
***Enjoy! :)***</br>
</br>
**INFO: now also available as a PIP INSTALL as illustrated [here](#installation)**</br>

### Built with

* [Python](https://www.python.org/)
* [Selenium](https://selenium.dev)
* [LocationGuard](https://chrome.google.com/webstore/detail/location-guard/cfohepagpmnodfdmjliccbbigdkfcgia)

<!-- Getting Started -->
## Getting Started
### Prerequisites

- Environment running python 3.x
- Tinder account with Google or Facebook login enabled

### Installation
#### PyPi
You can now install the project as a pip package.
```
pip3 install tinderbotz
```
#### Github
1. Clone or download the project
2. Install the required packages
```
pip3 install -r requirements.txt
```

## Usage of Tinderbot
### Features
Features of Tinderbot as demonstrated belowed can be found here: **[Tinderbot features](https://github.com/frederikme/TinderBot/blob/master/DOCUMENTATION.md)**</br>

### Demonstration
#### Setting a custom location
<img src="https://user-images.githubusercontent.com/60892381/99286075-a8c9a900-2838-11eb-86b6-4b8c028bee63.gif"></src>

#### Setting some Profile settings
<img src="https://user-images.githubusercontent.com/60892381/99513887-682e7480-298b-11eb-810f-caae7424a792.gif"></src>

#### Liking 10 profiles in row + dismissing potential pop ups
<img src="https://user-images.githubusercontent.com/60892381/94987708-92a5a900-0568-11eb-88fc-f6be69354d73.gif"></src>

#### Scraping your matches (new matches + messaged matches)
<img src="https://user-images.githubusercontent.com/60892381/94995711-702f8200-05a0-11eb-9273-bfbb48ce168c.gif"></src>

#### Sending personalized messages to your matches
<img src="https://user-images.githubusercontent.com/60892381/94997724-43ce3280-05ad-11eb-8a94-0a66f0afbf93.gif"></src>

## Coming Soon Features
### A picture is worth a thousand words
Instead of just sending an email with 'you have a match', let's add an image so you know if it's worth opening the app manually.</br>

### Finally a worthy opponent
Integrating a face recognition tool that would rate an image of yourself and an image of the geomatch.</br>
Then only like those profiles that come womewhat close to your looks. </br>

### Integrating Scraping (better)
Find a cleaner way to scrape geomatches while liking or disliking.</br>
Then try to get some wordclouds out of most common names, bio's...</br>

### Because we all like some juicy statistics
When the script is done running, an overview must be shown with all the actions done.
1. Logged in
2. Set custom location to ...
3. Likes 45 geomatches
4. Dislikes 5 geomatches
...

## Support the Repository
Feel free to make a pull request and contribute to this project.</br>
If you feel like buying me a drink:
* [Paypal](https://paypal.me/frederikmees)

