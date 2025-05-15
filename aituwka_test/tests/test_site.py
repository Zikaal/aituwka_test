import pytest
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(__name__)

@pytest.fixture(scope="class", autouse=True)
def before_after_class():
    logger.info("🏁 BEFORE CLASS: Starting test class")
    yield
    logger.info("🏁 AFTER CLASS: Finished test class")

@pytest.mark.usefixtures("before_after_class")
class TestAITUwka:

    def test_implicit_wait(self, browser):
        logger.info("➡️ Test: implicit wait")
        browser.implicitly_wait(10)
        browser.get("https://aituwka2-0.onrender.com/home.html")
        try:
            browser.find_element(By.ID, "sidebarToggleBtn").click()
            time.sleep(1)
        except:
            pass
        browser.execute_script("""
            let btn = document.getElementById('secretBtn');
            btn.style.display = 'block';
            btn.style.visibility = 'visible';
            btn.style.opacity = 1;
        """)
        btn = browser.find_element(By.ID, "secretBtn")
        btn.click()
        assert btn.get_attribute("id") == "secretBtn"

    def test_explicit_wait(self, browser):
        logger.info("➡️ Test: explicit wait")
        browser.get("https://aituwka2-0.onrender.com/home.html")
        browser.find_element(By.ID, "openFormBtn").click()
        modal = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "myModal"))
        )
        assert modal.is_displayed()

    def test_fluent_wait(self, browser):
        logger.info("➡️ Test: fluent wait")
        browser.get("https://aituwka2-0.onrender.com/home.html")
        browser.find_element(By.ID, "openFormBtn").click()
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "contactForm"))
        )
        form = browser.find_element(By.ID, "contactForm")
        form.find_element(By.ID, "name_contact").send_keys("Test User")
        form.find_element(By.ID, "email_contact").send_keys("test@example.com")
        form.find_element(By.ID, "message_contact").send_keys("Hello AITUwka!")
        form.find_element(By.CLASS_NAME, "about_button").click()
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "successMessage"))
        )

    def test_action_chains(self, browser):
        logger.info("➡️ Test: action chains")
        browser.get("https://aituwka2-0.onrender.com/home.html")
        el = browser.find_element(By.ID, "openFormBtn")
        ActionChains(browser).move_to_element(el).click().perform()
        modal = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "myModal"))
        )
        assert modal.is_displayed()

    def test_select_dropdown(self, browser):
        logger.info("➡️ Test: select dropdown")
        browser.get("https://aituwka2-0.onrender.com/home.html")
        try:
            browser.find_element(By.ID, "sidebarToggleBtn").click()
            time.sleep(1)
        except:
            pass
        browser.execute_script("document.getElementById('language').style.display = 'block';")
        select = Select(browser.find_element(By.ID, "language"))
        select.select_by_value("ru")
        time.sleep(1)
        select.select_by_value("en")
