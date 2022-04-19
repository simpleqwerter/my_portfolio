import threading
from time import sleep, time
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from app_main._skillbox_token import login, password

SIGN_IN_URL = 'https://go.skillbox.ru/auth/sign-in'
BASIC_COURSE_URL = 'https://go.skillbox.ru/profession/profession-python/python-razrabotchik-s-nulya'
DJANGO_URL = 'https://go.skillbox.ru/profession/profession-python/django-framework'
ADVANCED_URL = 'https://go.skillbox.ru/profession/profession-python/python-advanced'
URLS = [BASIC_COURSE_URL, DJANGO_URL, ADVANCED_URL]


class Parser:
    def __init__(self):
        options = ChromeOptions()
        options.add_argument("--headless")
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def sign_in(self):
        self.driver.get(SIGN_IN_URL)
        self.driver.implicitly_wait(15)
        login_box = self.driver.find_element(By.XPATH, "//input[@autocomplete='username']")
        password_box = self.driver.find_element(By.XPATH, "//input[@autocomplete='current-password']")
        send_button = self.driver.find_element(By.XPATH, "//button[@data-e2e='auth__login__enter-button']")
        login_box.send_keys(login + Keys.RETURN)
        password_box.send_keys(password + Keys.RETURN)
        if send_button.is_enabled():
            send_button.click()
        try:
            WebDriverWait(self.driver, 10).until(EC.title_contains("Мое обучение — Skillbox"))
            # WebDriverWait(driver, 10).until(EC.title_contains("Обучающая онлайн-платформа Skillbox"))
        except TimeoutException:
            title = self.driver.find_element(By.TAG_NAME, "title").text
            print(title)
        finally:
            return True

    def get_lessons_with_status(self, data_bank):
        for i, url in enumerate(URLS):
            self.driver.execute_script(f'''window.open("{url}", "_blank");''')
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            main_page = self.driver.page_source
            # driver.implicitly_wait(5)
            name = self.driver.find_element(By.CSS_SELECTOR, "div.course-header-card__title").text
            # print(name)
            lesson_names = self.driver.find_elements(By.CSS_SELECTOR, "span.accordion-title__text")  #class='accordion-title__text'
            lesson_names = [lesson.text for lesson in lesson_names]
            icons = self.driver.find_elements(By.CSS_SELECTOR, "svg-icon.status__icon-action")   # 'status__icon--XXXXXX'
            icons = ['success' if 'success' in icon.get_attribute('class') else '' for icon in icons]

            lesson_with_status = list(zip(lesson_names, icons))   # [(), (), ()]
            # print(lesson_with_status)
            data_bank[name] = lesson_with_status
        print(data_bank)

    def go(self):
        start = time()
        self.sign_in()
        self.data_bank = {}
        self.get_lessons_with_status(self.data_bank)
        self.driver.quit()
        print(f"запрос к скиллбокс выполнялся {time() - start} секунд")
        return self.data_bank


if __name__ == "__main__":
    parser = Parser()
    parser.go()

