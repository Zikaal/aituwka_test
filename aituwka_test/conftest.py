import pytest
import logging
import logging.config
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Загрузка логгера из logging.conf
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")

@pytest.fixture(scope="function")
def browser(request):
    logger.info("🧪 BEFORE METHOD: Launching browser")
    driver = webdriver.Chrome()
    driver.get("https://aituwka2-0.onrender.com/Login.html")

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "loginForm")))
    driver.find_element(By.ID, "email").send_keys("sasha@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Alikhan2301!")
    driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "sidebarToggleBtn")))

    yield driver

    # 💾 Скриншот после каждого теста (успех или ошибка)
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_dir = os.path.join("reports", "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(screenshot_path)
    logger.info(f"📸 Screenshot saved: {screenshot_path}")

    # ✅ Добавляем в html-отчёт
    if hasattr(request.node, "extra"):
        request.node.extra.append(pytest_html.extras.image(screenshot_path))
    else:
        request.node.extra = [pytest_html.extras.image(screenshot_path)]

    driver.quit()
    logger.info("🧹 AFTER METHOD: Browser closed")

# Хук для внедрения скриншота в отчёт
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    # Прикрепляем скриншот к HTML-отчёту
    if rep.when == "call":
        extra = getattr(rep, "extra", [])
        if hasattr(item, "extra"):
            extra.extend(item.extra)
        rep.extra = extra
