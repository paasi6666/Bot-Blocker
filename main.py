from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
driver.get("https://9gag.com")
input("Log into 9gag. Press ENTER after login.")

with open('bots.txt', 'r') as file:
    for bot in file:
        driver.get('https://9gag.com/u/'+bot)

        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div/div/a")))
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div/div/a").click()

        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div/div[2]/ul/li[3]/a")))
        blockButton = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div/div[2]/ul/li[3]/a")
        if "Unblock" not in blockButton.get_attribute('innerHTML'):
            blockButton.click()

            WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div[2]/div/button[2]")))
            driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/button[2]").click()
            print("User "+bot+" successfully blocked")
        else:
            driver.get("https://9gag.com")
            print("User "+bot+" was already blocked. Skipping...")