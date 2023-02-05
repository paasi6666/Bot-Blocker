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

        print("\n\n\n\n")
        askForReportAndBlock()
    elif inp == "2":
        print("You chose Chrome, installing driver..")

        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        options = webdriver.ChromeOptions() 
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
        
        print("\n\n\n\n")
        askForReportAndBlock()
    else:
        print("\n\n\n\nYou must choose between 1 or 2")
        return chooseBrowser()

def askForReportAndBlock():
    global reportAndBlock
    inp = input("Choose 1 to Block accounts\nChoose 2 to Block and Report accounts\n\n")
    if inp == "1":
        reportAndBlock = False
    elif inp == "2":
        reportAndBlock = True
    else:
        print("\n\n\n\nYou must choose between 1 or 2")
        return askForReportAndBlock()

chooseBrowser()

driver.get("https://9gag.com/login")
input("Log into 9gag. Press ENTER after login.")

with open('bots.txt', 'r') as file:
    for bot in file:
        bot = bot.strip()
        driver.get('https://9gag.com/u/'+bot)
        try:
            if(reportAndBlock):
                #Report User
                #Click Menu-Button
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".uikit-popup-menu a")))
                driver.find_element(By.CSS_SELECTOR, ".uikit-popup-menu a").click()

                #Click Report Button
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".uikit-popup-menu .menu ul li:nth-child(2) a")))
                driver.find_element(By.CSS_SELECTOR, ".uikit-popup-menu .menu ul li:nth-child(2) a").click()

                #Click Spam Button
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".report-type__type div:nth-child(2)")))
                driver.find_element(By.CSS_SELECTOR, ".report-type__type div:nth-child(2)").click()

                #Click Report Button
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".report-btn")))
                driver.find_element(By.CSS_SELECTOR, ".report-btn").click()
            
            #Block User
            #Click Menu-Button
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".uikit-popup-menu a")))
            driver.find_element(By.CSS_SELECTOR, ".uikit-popup-menu a").click()

            #Find Block-Button
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".uikit-popup-menu .menu ul li:nth-child(3) a")))
            blockButton = driver.find_element(By.CSS_SELECTOR, ".uikit-popup-menu .menu ul li:nth-child(3) a")
            print(blockButton.get_attribute('innerHTML'))

            #Check if User is already blocked or not
            if "Unblock" not in blockButton.get_attribute('innerHTML'):
                blockButton.click()

                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-dialog__actions button.btn-color-danger")))
                driver.find_element(By.CSS_SELECTOR, ".ui-dialog__actions button.btn-color-danger").click()
                print("User "+bot+" successfully blocked")
            else:
                driver.get("https://9gag.com")
                print("User "+bot+" was already blocked. Skipping...")
        except:
            print("User "+bot+" was already blocked. Skipping...")