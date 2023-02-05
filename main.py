from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def chooseBrowser():
    global driver
    inp = input("Choose 1 for Firefox\nChoose 2 for Chrome\n\n")
    if inp == "1":
        print("You chose Firefox, installing driver..")
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif inp == "2":
        print("You chose Chrome, installing driver..")
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager

        options = webdriver.ChromeOptions() 
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    else:
        print("You must choose between 1 or 2")
        return chooseBrowser()
chooseBrowser()

driver.get("https://9gag.com/login")
input("Log into 9gag. Press ENTER after login.")

with open('bots.txt', 'r') as file:
    for bot in file:
        bot = bot.strip()
        driver.get('https://9gag.com/u/'+bot)
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='profile-more'] div[class='uikit-popup-menu'] div a[class='button']")))
            driver.find_element(By.CSS_SELECTOR, "div[class='profile-more'] div[class='uikit-popup-menu'] div a[class='button']").click()

            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div/div[2]/ul/li[3]/a")))
            blockButton = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div/div[2]/ul/li[3]/a")
            if "Unblock" not in blockButton.get_attribute('innerHTML'):
                blockButton.click()

                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div[2]/div/button[2]")))
                driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/button[2]").click()
                print("User "+bot+" successfully blocked")
            else:
                driver.get("https://9gag.com")
                print("User "+bot+" was already blocked. Skipping...")
        except:
            print("User "+bot+" was already blocked. Skipping...")