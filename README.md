# Tinderbotz
**Consider giving a ⭐ if you like the project!**
## Project
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
    <a href="https://github.com/frederikme/TinderBot/blob/master/DOCUMENTATION.md"><strong>Explore the docs »</strong></a>
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
  * [Breaking Record](#breaking-record)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage-of-tinderbot)
  * [Documentation](DOCUMENTATION.md)
  * [Demo](#demonstration)
* [Example Data Analysis](#example-data-analysis)
* [Avoiding the Ban](#how-to-avoid-the-ban)
* [Support the Repository](#support-the-repository)
* [Other Tinder Repositories](#other-tinder-repositories)
* [Disclaimer](#disclaimer)

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
* Swiping x number of profiles left or right
* Scraping data of the profiles displayed, including, yet not limited to, name, age, bio, images, ...
* Sending personalized messages to your matches
* Sending you social media cards, like Instagram, Snapchat, Phonenumber and Facebook
* Sending GIFS and songs
* Unmatching

If you feel like diving right in, the [quickstart.py](https://github.com/frederikme/TinderBot/blob/master/quickstart.py) will help you be right on track.</br>
If you're new to coding and just want the script to automatically like, the [auto_swipe.py](https://github.com/frederikme/TinderBot/blob/master/auto_swipe.py) would be what you're looking for!</br>
*Feel free to make a pull request and contribute to this project!*</br>
</br>
***Enjoy! :)***</br>

***Youtube Video***
[![Getting +1000 Matches on Tinder in 24 Hours by Building a Tinderbot!](https://img.youtube.com/vi/qCgKlCi6YRI/0.jpg)](https://www.youtube.com/watch?v=qCgKlCi6YRI)

### Built with

* [Python](https://www.python.org/)
* [Selenium](https://selenium.dev)
* [Undetected-Chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)

### Breaking Record
**I broke the world record most matches using this script!**</br>
Reached 1000 matches in the first 24hours.</br>
Currently at 30000 matches!</br>

<p align="left">
  <a href="https://user-images.githubusercontent.com/60892381/104088880-2d014100-526a-11eb-8b6d-ad1da6567778.jpg">
    <img src="https://user-images.githubusercontent.com/60892381/104088880-2d014100-526a-11eb-8b6d-ad1da6567778.jpg" width="250">
  </a>
</p>

<!-- Getting Started -->
## Getting Started
### Prerequisites

- Environment running python 3.x
- Tinder account with Google or Facebook login enabled

### Installation
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
#### Setting some Profile settings
<img src="https://user-images.githubusercontent.com/60892381/99513887-682e7480-298b-11eb-810f-caae7424a792.gif"></src>

#### Liking 10 profiles in row + dismissing potential pop ups
<img src="https://user-images.githubusercontent.com/60892381/94987708-92a5a900-0568-11eb-88fc-f6be69354d73.gif"></src>

#### Scraping your matches (new matches + messaged matches)
<img src="https://user-images.githubusercontent.com/60892381/94995711-702f8200-05a0-11eb-9273-bfbb48ce168c.gif"></src>

#### Sending personalized messages to your matches
<img src="https://user-images.githubusercontent.com/60892381/94997724-43ce3280-05ad-11eb-8a94-0a66f0afbf93.gif"></src>

## Example Data Analysis
When scraping geomatches or your own matches, you can start doing some pretty cool stuff with that data.
A few examples are: 

#### Worldclouds
You can create wordclouds to visualise data such as the most popular names, or most occuring words in a bio.
<img src="https://user-images.githubusercontent.com/60892381/110502983-02adf180-80fc-11eb-85c4-a0cee0dd63f1.jpg"></src>
<img src="https://user-images.githubusercontent.com/60892381/110502986-03df1e80-80fc-11eb-9d86-c3cb38a553e5.jpg"></src>

#### The 'Average' Person
You can also start calculating what an 'average' tinderprofile would look like.</br>
You can for example check the average number of words a bio consists of or the average number of images a user has.
<img src="https://user-images.githubusercontent.com/60892381/94479341-f03a9e00-01d4-11eb-9a10-70a8aa8208ea.png"></src>

## How to Avoid the Ban
This small section will explain how their bot detection works and how you can avoid getting banned.</br>

### 1) Go easy with newly created profiles
Newly created profiles are much more likely to get banned than long-existing ones.</br>
*So be extra cautious!*</br>

### 2) Avoid the usage of URLS!
This one is very lethal for your accounts. Avoid sending urls to people in messages and **DO NOT** place any url in your bio!</br>

### 3) Avoid running the code overnight
Try to use the code when you can see it running. In case you need to handle something (like a captcha or anything) you can immediatly respond to it.
I've heard some people had to prove they were not bots by doing some captcha and this could age very poorly when you run it overnight. Myself however, I haven't yet had 'the honour' to be redirected to such a captcha. So if you play it safe, there would be no need to panic.

### 4) Implement sleeps between swipes 
This might sounds ridiculous, but most people take a look at the profile before they swipe it. Therefore instantly swiping right on every profile puts you in a 'non humanlike behaviour'-zone, which should be tried to be avoided. Adding a sleep between swipes can be done as described [here](https://github.com/frederikme/TinderBotz/blob/master/DOCUMENTATION.md#liking-geomatches). It is recommended to sleep at least 1 second between every swipe. If you have a rather new profile, then make it 2 or 3 (float numbers like 1.5 are also allowed).

### 5) Implement randomness in your liking and disliking
Same applies as above; most people dislike some profiles and like others. Not liking EVERY profile could help you stay under the radar.
Example of how to do so can be found [here](https://github.com/frederikme/TinderBotz/blob/master/DOCUMENTATION.md#liking-geomatches).

### 6) Make your profile look as real as possible
Your profile cannot look in any way like those spambots. Therefore a few things can be done.

#### 6.1) Verify your profile with the blue badge to prove it's really you
#### 6.2) Link your Instagram/Spotify/Facebook and verify your email
#### 6.3) Write a good bio, preferably with a minimum of 100 characters
#### 6.4) Add at least 3-4 images, preferably more

## Support the Repository
Feel free to make a pull request and contribute to this project.</br>
If you feel like buying me a drink:
* [Paypal](https://paypal.me/frederikmees)
* [Patreon](https://www.patreon.com/frederikme)
* [Buy Me A Coffee](https://www.buymeacoffee.com/frederikme)

## Other Tinder Repositories
![Imgur](https://imgur.com/hSVjccD.jpg)
- [Analysis of Tinder Likes from "Likes Sent"](https://github.com/acarter881/tinder_likes_data) <br>
This repository uses Selenium, pandas, BeautifulSoup, Excel, and more to glean meaningful insights from Tinder profile cards.

## Disclaimer
Using automated software on Tinder is against community guidelines and might get your account banned.</br>

Also for the section **data mining**: scraping profiles is not only against Tinder's policies, but it's also against the law in many places.</br>
People on Tinder did not give their permission to be stored by any other entity than Tinder itself and people have the right to be forgotten. (see: [GDPR in Europe](https://ec.europa.eu/info/law/law-topic/data-protection/data-protection-eu_en))</br>

So here's a reminder that this software is for **educational purposes only** and it cannot be held accountable for any consequences you may face by having used this tool. Neither personal (banned account) nor judicial (lawsuits for privacy violations).

