import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time

@pytest.fixture
def driver():
    d = webdriver.Chrome()
    yield d
    d.quit()

def test_empty_username(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(2)
    assert Alert(driver).text == "Username cannot be empty."

def test_empty_password(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("John")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(2)
    assert Alert(driver).text == "Password cannot be empty."

def test_short_password(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("Jane")
    driver.find_element(By.NAME, "pwd").send_keys("1234")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(2)
    assert Alert(driver).text == "Password must be at least 6 characters long."

def test_valid_input(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("Kuku")
    driver.find_element(By.NAME, "pwd").send_keys("123456")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(2)
    assert "Hello, Kuku!" in driver.find_element(By.TAG_NAME, "body").text