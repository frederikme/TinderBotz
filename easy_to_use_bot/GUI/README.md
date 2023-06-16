# Tinder bot 

![Alt Text](photo.jpg)



##### Open Google Chrome and type chrome://version/ in the address bar.

##### Look for the "Profile Path" field in the displayed information.

##### On line 21 of the script file tinder_bot.py, enter your Chrome profile path as follows:


    juba.add_argument('--profile-directory=Your_Profile_Path')

##### On line 22, enter the path to your Chrome user data directory:

    juba.add_argument('--user-data-dir=Your_User_Data_Directory')


### example
    juba.add_argument('--profile-directory=Profile 3')
    juba.add_argument('--user-data-dir=/home/juba/.config/google-chrome/')

