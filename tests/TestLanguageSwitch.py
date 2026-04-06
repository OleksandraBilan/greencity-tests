import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLanguageSwitch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.get("https://www.greencity.cx.ua/#/greenCity/events")

    def test_language_switch_filters_translation(self):
        driver = self.driver
        wait = self.wait

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

       
        ua_filters = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//mat-label"))
        )
        ua_texts = [f.text.strip() for f in ua_filters if f.text.strip()]

       
        lang_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Uk']"))
        )
        lang_button.click()

        en_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='En']"))
        )
        en_option.click()

      
        wait.until(
            lambda d: all(
                "Де" not in el.text and "Час" not in el.text
                for el in d.find_elements(By.XPATH, "//mat-label")
                if el.text.strip()
            )
        )

     
        en_filters = driver.find_elements(By.XPATH, "//mat-label")
        en_texts = [f.text.strip() for f in en_filters if f.text.strip()]

     
        expected_translation = {
            "Де?": "Where?",
            "Час події": "Event time",
            "Статус": "Status",
            "Тип події": "Event type",
            "Дати": "Dates"
        }


        for i in range(len(ua_texts)):
            ua = ua_texts[i]
            en = en_texts[i]

            if ua in expected_translation:
                expected_en = expected_translation[ua]

                self.assertEqual(
                    en,
                    expected_en,
                    f"Невірний переклад: '{ua}' → '{en}', очікується '{expected_en}'"
                )

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
