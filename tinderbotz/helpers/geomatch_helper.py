from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from tinderbotz.helpers.xpaths import content

class GeomatchHelper:

    delay = 5

    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self, browser):
        self.browser = browser
        if "/app/recs" not in self.browser.current_url:
            self._get_home_page()

    def like(self)->bool:
        try:
            # need to find better way
            if 'profile' in self.browser.current_url:
                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[4]/button'

                # wait for element to appear
                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                # locate like button
                like_button = self.browser.find_element(By.XPATH, xpath)

                like_button.click()

            else:
                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]'

                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                card = self.browser.find_element(By.XPATH, xpath)

                action = ActionChains(self.browser)
                action.drag_and_drop_by_offset(card, 200, 0).perform()

            time.sleep(1)
            return True

        except (TimeoutException, ElementClickInterceptedException):
            self._get_home_page()

        return False

    def dislike(self):
        try:
            if 'profile' in self.browser.current_url:
                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[2]/button'
                # wait for element to appear
                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                dislike_button = self.browser.find_element(By.XPATH, xpath)

                dislike_button.click()
            else:

                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]'

                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                card = self.browser.find_element(By.XPATH, xpath)

                action = ActionChains(self.browser)
                action.drag_and_drop_by_offset(card, -200, 0).perform()

            time.sleep(1)
        except (TimeoutException, ElementClickInterceptedException):
            self._get_home_page()

    def superlike(self):
        try:
            if 'profile' in self.browser.current_url:
                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/button'

                # wait for element to appear
                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                superlike_button = self.browser.find_element(By.XPATH, xpath)

                superlike_button.click()

            else:
                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]'

                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                card = self.browser.find_element(By.XPATH, xpath)

                action = ActionChains(self.browser)
                action.drag_and_drop_by_offset(card, 0, -200).perform()

            time.sleep(1)

        except (TimeoutException, ElementClickInterceptedException):
            self._get_home_page()

    def _open_profile(self, second_try=False):
        if self._is_profile_opened(): return;
        try:
            xpath = '//button'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))
            buttons = self.browser.find_elements_by_xpath(xpath)

            for button in buttons:
                # some buttons might not have a span as subelement
                try:
                    text_span = button.find_element(By.XPATH, './/span').text
                    if 'open profile' in text_span.lower():
                        button.click()
                        break
                except:
                    continue

            time.sleep(1)

        except (ElementClickInterceptedException, TimeoutException):
            if not second_try:
                print("Trying again to locate the profile info button in a few seconds")
                time.sleep(2)
                self._open_profile(second_try=True)
            else:
                self.browser.refresh()
        except:
            self.browser.get(self.HOME_URL)
            if not second_try:
                self._open_profile(second_try=True)

    def get_name(self):
        if not self._is_profile_opened():
            self._open_profile()

        try:
            xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/h1'
            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            element = self.browser.find_element(By.XPATH, xpath)

            name = element.text
            if not name:
                xpath2 = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/h1'
                element2 = self.browser.find_element(By.XPATH, xpath2)
                name = element2.text

            return name
        except Exception as e:
            pass

    def get_age(self):
        if not self._is_profile_opened():
            self._open_profile()

        age = None

        try:
            xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/span'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            element = self.browser.find_element(By.XPATH, xpath)
            try:
                age = int(element.text)
            except ValueError:
                age = None

        except:
            pass

        return age

    def is_verified(self):
        if not self._is_profile_opened():
            self._open_profile()

        xpath_badge = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]'
        try:
            self.browser.find_element(By.XPATH, xpath_badge)
            return True

        except:
            return False

    _WORK_SVG_PATH = "M7.15 3.434h5.7V1.452a.728.728 0 0 0-.724-.732H7.874a.737.737 0 0 0-.725.732v1.982z"
    _STUDYING_SVG_PATH = "M11.87 5.026L2.186 9.242c-.25.116-.25.589 0 .705l.474.204v2.622a.78.78 0 0 0-.344.657c0 .42.313.767.69.767.378 0 .692-.348.692-.767a.78.78 0 0 0-.345-.657v-2.322l2.097.921a.42.42 0 0 0-.022.144v3.83c0 .45.27.801.626 1.101.358.302.842.572 1.428.804 1.172.46 2.755.776 4.516.776 1.763 0 3.346-.317 4.518-.777.586-.23 1.07-.501 1.428-.803.355-.3.626-.65.626-1.1v-3.83a.456.456 0 0 0-.022-.145l3.264-1.425c.25-.116.25-.59 0-.705L12.13 5.025c-.082-.046-.22-.017-.26 0v.001zm.13.767l8.743 3.804L12 13.392 3.257 9.599l8.742-3.806zm-5.88 5.865l5.75 2.502a.319.319 0 0 0 .26 0l5.75-2.502v3.687c0 .077-.087.262-.358.491-.372.29-.788.52-1.232.68-1.078.426-2.604.743-4.29.743s-3.212-.317-4.29-.742c-.444-.161-.86-.39-1.232-.68-.273-.23-.358-.415-.358-.492v-3.687z"
    _HOME_SVG_PATH = "M19.695 9.518H4.427V21.15h15.268V9.52zM3.109 9.482h17.933L12.06 3.709 3.11 9.482z"
    _LOCATION_SVG_PATH = "M11.436 21.17l-.185-.165a35.36 35.36 0 0 1-3.615-3.801C5.222 14.244 4 11.658 4 9.524 4 5.305 7.267 2 11.436 2c4.168 0 7.437 3.305 7.437 7.524 0 4.903-6.953 11.214-7.237 11.48l-.2.167zm0-18.683c-3.869 0-6.9 3.091-6.9 7.037 0 4.401 5.771 9.927 6.897 10.972 1.12-1.054 6.902-6.694 6.902-10.95.001-3.968-3.03-7.059-6.9-7.059h.001z"
    _LOCATION_SVG_PATH_2 = "M11.445 12.5a2.945 2.945 0 0 1-2.721-1.855 3.04 3.04 0 0 1 .641-3.269 2.905 2.905 0 0 1 3.213-.645 3.003 3.003 0 0 1 1.813 2.776c-.006 1.653-1.322 2.991-2.946 2.993zm0-5.544c-1.378 0-2.496 1.139-2.498 2.542 0 1.404 1.115 2.544 2.495 2.546a2.52 2.52 0 0 0 2.502-2.535 2.527 2.527 0 0 0-2.499-2.545v-.008z"
    _GENDER_SVG_PATH = "M15.507 13.032c1.14-.952 1.862-2.656 1.862-5.592C17.37 4.436 14.9 2 11.855 2 8.81 2 6.34 4.436 6.34 7.44c0 3.07.786 4.8 2.02 5.726-2.586 1.768-5.054 4.62-4.18 6.204 1.88 3.406 14.28 3.606 15.726 0 .686-1.71-1.828-4.608-4.4-6.338"

    def get_row_data(self):
        if not self._is_profile_opened():
            self._open_profile()

        rowdata = {}

        xpath = '//div[@class="Row"]'
        rows = self.browser.find_elements(By.XPATH, xpath)

        for row in rows:
            svg = row.find_element(By.XPATH, ".//*[starts-with(@d, 'M')]").get_attribute('d')
            value = row.find_element(By.XPATH, ".//div[2]").text
            if svg == self._WORK_SVG_PATH:
                rowdata['work'] = value
            if svg == self._STUDYING_SVG_PATH:
                rowdata['study'] = value
            if svg == self._HOME_SVG_PATH:
                rowdata['home'] = value.split(' ')[-1]
            if svg == self._GENDER_SVG_PATH:
                rowdata['gender'] = value
            if svg == self._LOCATION_SVG_PATH or svg == self._LOCATION_SVG_PATH_2:
                distance = value.split(' ')[0]
                try:
                    distance = int(distance)
                except TypeError:
                    # Means the text has a value of 'Less than 1 km away'
                    distance = 1
                except ValueError:
                    distance = None

                rowdata['distance'] = distance

        return rowdata

    def get_bio_and_passions(self):
        if not self._is_profile_opened():
            self._open_profile()

        bio = None
        is_bio = True

        passions = []
        is_passions = True

        xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[3]/h2'
        passions_xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div'

        try:
            if not 'passions' in self.browser.find_element(By.XPATH, xpath).text.lower():

                xpath2 = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/h2'
                if not 'passions' in self.browser.find_element(By.XPATH, xpath2).text.lower():
                    is_passions = False
                else:
                    passions_xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div/div'
                    is_bio = False
        except:
            try:
                xpath2 = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/h2'
                if not 'passions' in self.browser.find_element(By.XPATH, xpath2).text.lower():
                    is_passions = False
                else:
                    passions_xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div/div'
                    is_bio = False
            except:
                passions_xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div/div'

        if is_bio:
            try:
                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div'

                bio = self.browser.find_element(By.XPATH, xpath).text
                if 'recent instagram photos' in bio.lower():
                    bio = None

            except Exception as e:
                pass

        if is_passions:
            try:
                elements = self.browser.find_elements(By.XPATH, passions_xpath)
                for el in elements:
                    passions.append(el.text)
            except Exception as e:
                pass

        return bio, passions

    def get_image_urls(self, quickload=True):
        if not self._is_profile_opened():
            self._open_profile()

        image_urls = []

        # only get url of first few images, and not click all bullets to get all image
        elements = self.browser.find_elements_by_xpath("//div[@aria-label='Profile slider']")
        for element in elements:
            image_url = element.value_of_css_property('background-image').split('\"')[1]
            if image_url not in image_urls:
                image_urls.append(image_url)

        # return image urls without opening all images
        if quickload:
            return image_urls

        try:
            # There are no bullets when there is only 1 image
            classname = 'bullet'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.CLASS_NAME, classname)))

            image_btns = self.browser.find_elements_by_class_name(classname)

            for btn in image_btns:
                btn.click()
                time.sleep(1)

                elements = self.browser.find_elements_by_xpath("//div[@aria-label='Profile slider']")
                for element in elements:
                    image_url = element.value_of_css_property('background-image').split('\"')[1]
                    if image_url not in image_urls:
                        image_urls.append(image_url)

        except StaleElementReferenceException:
            pass

        except TimeoutException:
            # there is only 1 image, so no bullets to iterate through
            try:
                element = self.browser.find_element(By.XPATH, "//div[@aria-label='Profile slider']")
                image_url = element.value_of_css_property('background-image').split('\"')[1]
                if image_url not in image_urls:
                    image_urls.append(image_url)

            except Exception as e:
                print("unhandled Exception when trying to store their only image")
                print(e)

        except Exception as e:
            print("unhandled exception getImageUrls in geomatch_helper")
            print(e)

        return image_urls

    @staticmethod
    def de_emojify(text):
        """Remove emojis from a string
        Args:
            text (string): string with emojis or not
        Returns:
            string: recompile string without emojis
        """
        regrex_pattern = re.compile(
            pattern="["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    "]+",
            flags=re.UNICODE,
        )
        return regrex_pattern.sub(r'', text)

    def get_insta(self, text):
        """Take the bio and read line by line to match if the description
        contain an instagram user.
        Args:
            text (string): string with emojis or not
        Returns:
            ig (string): return valid instagram user.
        """
        if not text:
            return None
        valid_pattern = [
            "@",
            "ig-",
            "ig",
            "ig:",
            "ing",
            "ing:",
            "instag",
            "instag:",
            "insta:",
            "insta",
            "inst",
            "inst:",
            "instagram",
            "instagram:",
        ]
        description = text.rstrip().lower().strip()
        description = description.split()
        for x in range(len(description)):
            ig = self.de_emojify(description[x])
            if '@' in ig:
                return ig.replace('@', '')
            elif ig in valid_pattern:
                if ':' in description[x + 1]:
                    return description[x + 2]
                else:
                    return description[x + 1]
            else:
                try:
                    ig = ig.split(':', 1)
                    if ig[0] in valid_pattern:
                        return ig[-1]
                except:
                    return None
        return None

    def _get_home_page(self):
        self.browser.get(self.HOME_URL)
        time.sleep(5)

    def _is_profile_opened(self):
        if '/profile' in self.browser.current_url:
            return True
        else:
            return False
