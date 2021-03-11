import enum


# Using enum class create enumerations
class Socials(enum.Enum):
    SNAPCHAT = "snapchat"
    INSTAGRAM = "instagram"
    PHONENUMBER = "phone"
    FACEBOOK = "facebook"


class Sexuality(enum.Enum):
    MEN = "Men"
    WOMEN = "Women"
    EVERYONE = "Everyone"


class Language(enum.Enum):
    ENGLISH = "English"
    AFRIKAANS = "Afrikaans"
    ARABIC = "Arabic"
    BULGARIAN = "Bulgarian"
    BOSNIAN = "Bosnian"
    CROATIAN = "Croatian"
    CZECH = "Czech"
    DANISH = "Danish"
    DUTCH = "Dutch"
    ESTONIAN = "Estonian"
    FINNISH = "Finnish"
    FRENCH = "French"
    GEORGIAN = "Georgian"
    GERMAN = "German"
    GREEK = "Greek"
    HINDI = "Hindi"
    HUNGARIAN = "Hungarian"
    INDONESIAN = "Indonesian"
    ITALIAN = "Italian"
    JAPANESE = "Japanese"
    KOREAN = "Korean"
    LATVIAN = "Latvian"
    LITHUANIAN = "Lithuanian"
    MACEDONIAN = "Macedonian"
    MALAY = "Malay"
    POLISH = "Polish"
    PORTUGUESE = "Portuguese"
    ROMANIAN = "Romanian"
    RUSSIAN = "Russian"
    SERBIAN = "Serbian"
    SPANISH = "Spanish"
    SLOVAK = "Slovak"
    SLOVENIAN = "Slovenian"
    SWEDISH = "Swedish"
    TAMIL = "Tamil"
    THAI = "Thai"
    TURKISH = "Turkish"
    UKRAINIAN = "Ukrainian"
    VIETNAMESE = "Vietnamese"
   
class Printouts(enum.Enum):
    BANNER = ''' 
         _____ _           _           _           _       
        |_   _(_)_ __   __| | ___ _ __| |__   ___ | |_ ____
          | | | | '_ \ / _` |/ _ \ '__| '_ \ / _ \| __|_  /
          | | | | | | | (_| |  __/ |  | |_) | (_) | |_ / / 
          |_| |_|_| |_|\__,_|\___|_|  |_.__/ \___/ \__/___|
        ----------------------------------------------------'''
    
    EXPLANATION = '''
Hi guys,

This code is opensource and available on GitHub.
repository: https://github.com/frederikme/TinderBotz

If you find the code useful, it would mean a lot if you can star the repository to show your appreciation.
If you're interested in learning how to write these bots yourself,
I will be making tutorials about python selenium automation soon.

youtube_channel: https://www.youtube.com/channel/UC1i3N9R9XYxt5Imi-auLPuA
tutorials that will be coming:
1. Scraping news on websites -> For absolute beginners, as an intro to selenium 
2. A simplified Tinderbot -> For beginners
3. Writing an automated chess bot to play on Chess.com using stockfish (currently a private repository). -> Advanced

Have a nice day,
Frederikme
'''
