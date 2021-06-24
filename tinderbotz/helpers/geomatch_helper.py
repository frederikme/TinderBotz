from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
import time
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
                like_button = self.browser.find_element_by_xpath(xpath)

                like_button.click()

            else:
                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]'

                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                card = self.browser.find_element_by_xpath(xpath)

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

                dislike_button = self.browser.find_element_by_xpath(xpath)

                dislike_button.click()
            else:

                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]'

                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                card = self.browser.find_element_by_xpath(xpath)

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

                superlike_button = self.browser.find_element_by_xpath(xpath)

                superlike_button.click()

            else:
                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]'

                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                card = self.browser.find_element_by_xpath(xpath)

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
                    text_span = button.find_element_by_xpath('.//span').text
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
            xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div/h1'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            element = self.browser.find_element_by_xpath(xpath)
            return element.text
        except Exception as e:
            pass

    def get_age(self):
        if not self._is_profile_opened():
            self._open_profile()

        age = None

        try:
            xpath = '//span[@itemprop="age"]'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

            element = self.browser.find_element_by_xpath(xpath)
            try:
                age = int(element.text)
            except ValueError:
                age = None

        except:
            pass

        return age

    _WORK_SVG_PATH = "M7.15 3.434h5.7V1.452a.728.728 0 0 0-.724-.732H7.874a.737.737 0 0 0-.725.732v1.982z"
    _STUDYING_SVG_PATH = "M11.87 5.026L2.186 9.242c-.25.116-.25.589 0 .705l.474.204v2.622a.78.78 0 0 0-.344.657c0 .42.313.767.69.767.378 0 .692-.348.692-.767a.78.78 0 0 0-.345-.657v-2.322l2.097.921a.42.42 0 0 0-.022.144v3.83c0 .45.27.801.626 1.101.358.302.842.572 1.428.804 1.172.46 2.755.776 4.516.776 1.763 0 3.346-.317 4.518-.777.586-.23 1.07-.501 1.428-.803.355-.3.626-.65.626-1.1v-3.83a.456.456 0 0 0-.022-.145l3.264-1.425c.25-.116.25-.59 0-.705L12.13 5.025c-.082-.046-.22-.017-.26 0v.001zm.13.767l8.743 3.804L12 13.392 3.257 9.599l8.742-3.806zm-5.88 5.865l5.75 2.502a.319.319 0 0 0 .26 0l5.75-2.502v3.687c0 .077-.087.262-.358.491-.372.29-.788.52-1.232.68-1.078.426-2.604.743-4.29.743s-3.212-.317-4.29-.742c-.444-.161-.86-.39-1.232-.68-.273-.23-.358-.415-.358-.492v-3.687z"
    _HOME_SVG_PATH = "M19.695 9.518H4.427V21.15h15.268V9.52zM3.109 9.482h17.933L12.06 3.709 3.11 9.482z"
    _LOCATION_SVG_PATH = "M11.436 21.17l-.185-.165a35.36 35.36 0 0 1-3.615-3.801C5.222 14.244 4 11.658 4 9.524 4 5.305 7.267 2 11.436 2c4.168 0 7.437 3.305 7.437 7.524 0 4.903-6.953 11.214-7.237 11.48l-.2.167zm0-18.683c-3.869 0-6.9 3.091-6.9 7.037 0 4.401 5.771 9.927 6.897 10.972 1.12-1.054 6.902-6.694 6.902-10.95.001-3.968-3.03-7.059-6.9-7.059h.001z"

    def get_row_data(self):
        if not self._is_profile_opened():
            self._open_profile()

        rowdata = {}

        xpath = '//div[@class="Row"]'
        rows = self.browser.find_elements_by_xpath(xpath)

        for row in rows:
            svg = row.find_element_by_xpath(".//*[starts-with(@d, 'M')]").get_attribute('d')
            value = row.find_element_by_xpath(".//div[2]").text
            if svg == self._WORK_SVG_PATH:
                rowdata['work'] = value
            if svg == self._STUDYING_SVG_PATH:
                rowdata['study'] = value
            if svg == self._HOME_SVG_PATH:
                rowdata['home'] = value
            if svg == self._LOCATION_SVG_PATH:
                distance = value.split(' ')[0]
                try:
                    distance = int(distance)
                except TypeError:
                    # Means the text has a value of 'Less than 1 km away'
                    distance = 1
                rowdata['distance'] = distance

        return rowdata

    def get_passions(self):
        if not self._is_profile_opened():
            self._open_profile()

        passions = []

        xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[4]/div'
        elements = self.browser.find_elements_by_xpath(xpath)
        for el in elements:
            passions.append(el.text)

        return passions

    def get_bio(self):
        if not self._is_profile_opened():
            self._open_profile()

        try:
            xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div'
            return self.browser.find_element_by_xpath(xpath).text

        except Exception as e:
            return None

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
                element = self.browser.find_element_by_xpath("//div[@aria-label='Profile slider']")
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

    def _get_home_page(self):
        self.browser.get(self.HOME_URL)
        time.sleep(5)

    def _is_profile_opened(self):
        if '/profile' in self.browser.current_url:
            return True
        else:
            return False