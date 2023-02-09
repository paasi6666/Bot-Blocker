from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime

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
    global scanAccounts
    inp = input("Choose 1 to Block accounts\nChoose 2 to Block and Report accounts\n\n")
    if inp == "1":
        reportAndBlock = False
        scanAccounts = False
    elif inp == "2":
        reportAndBlock = True
        scanAccounts = False
    elif inp == "3":
        scanAccounts = True
    else:
        print("\n\n\n\nYou must choose between 1 or 3")
        return askForReportAndBlock()

def monthStringToInt(monthString):
    if monthString == "Jan":
        return 1
    elif monthString == "Feb":
        return 2
    elif monthString == "Mar":
        return 3
    elif monthString == "Apr":
        return 4
    elif monthString == "May":
        return 5
    elif monthString == "Jun":
        return 6
    elif monthString == "Jul":
        return 7
    elif monthString == "Aug":
        return 8
    elif monthString == "Sep":
        return 9
    elif monthString == "Oct":
        return 10
    elif monthString == "Nov":
        return 11
    elif monthString == "Dec":
        return 12
    else:
        return None

def postTimeToHour(value, unit):
    # return the time since post in hour
    if unit == "d":
        return int(value) * 24
    if unit == "h":
        return int(value)
    if unit == "m":
        return int(value) / 60

chooseBrowser()

if scanAccounts:
    driver.get("https://9gag.com/fresh")

    buffer = []
    posters = {}
    lastPostTime = None
    date = datetime.now()
    try:
        print("Scanning...You may now scroll to oblivion.\n")
        print("Warning:  Scanning might produce false positives if you can't see 1h old posts at least.")
        previous_stream = None
        # Loop to scan continuously while on 9gag.
        while EC.presence_of_element_located((By.CSS_SELECTOR, ".list-stream")):
            for stream in driver.find_elements(By.CSS_SELECTOR, ".list-stream"):
                # Prevent scaning all previous posts each frame.
                if stream.id != previous_stream:
                    if not stream.id in buffer:
                        buffer.append(stream.id)
                        previous_stream = stream.id
                        # Scan posts in curent stream.
                        post_list = stream.find_elements(By.CSS_SELECTOR, ".ui-post-creator")
                        for post in post_list:
                            try:
                                if not post.id in buffer:
                                    poster = post.find_element(By.CSS_SELECTOR, ".ui-post-creator__author")
                                    time = post.find_element(By.CSS_SELECTOR, ".ui-post-creator__creation")
                                    # print(poster.text, time.text)
                                    lastPostTime = time.text
                                    if not poster.text in posters.keys():
                                        posters[poster.text] = [time.text]
                                    else:
                                        posters[poster.text].append(time.text)
                                    buffer.append(post.id)
                            except:
                                # Promoted post or ad.
                                pass
    except:
        # Estimate the scrolled time span in fresh (take the oldest post)
        
        if len(lastPostTime) == 9:
            postYear = lastPostTime[-2:]
            postMonth = monthStringToInt(lastPostTime[3:5])
            postDay = lastPostTime[:1]

            postDate = datetime.strptime(20+postYear, postMonth, postDay, '%Y %m %d')
            scanDate = datetime.strptime(date.tm_year, date.tm_month, date.tm_day, '%Y %m %d')
            deltaDate = scanDate - postDate
            hoursElapsed = deltaDate.totalseconds() / 3600

        elif len(lastPostTime) == 6:
            postMonth = monthStringToInt(lastPostTime[3:5])
            postDay = lastPostTime[:1]

            postDate = datetime.strptime("2023", postMonth, postDay, '%Y %m %d')
            scanDate = datetime.strptime("2023", date.tm_month, date.tm_day, '%Y %m %d')
            deltaDate = scanDate - postDate
            hoursElapsed = deltaDate.totalseconds() / 3600

        elif len(lastPostTime) == 3:
            hoursElapsed = postTimeToHour(lastPostTime[:1], lastPostTime[-1])
        elif len(lastPostTime) == 2:
            hoursElapsed = postTimeToHour(lastPostTime[0], lastPostTime[-1])
        else:
            # error in date format or "Just Now"
            hoursElapsed = None

        existingBots = []
        bots = []       
        with open(os.path.realpath(os.path.dirname(__file__)) + os.sep + 'bots.txt', 'r') as file:
            for bot in file:
                existingBots.append(bot.strip())


        print("Elapsed time in scroll:", hoursElapsed)
        for poster, times in posters.items():
            if poster != "9GAGGER":
                # Estimate the average amount of posts per hour from this user.
                postPerHour = len(times) / hoursElapsed
                if postPerHour > 1:
                    if not poster in existingBots:
                        bots.append(poster)


        newBotsList = existingBots + bots
        print(newBotsList)
        newBotsList.sort()
        print(newBotsList)

        print("HERE ARE THE (IM)POSTERS FOUND")
        with open(os.path.realpath(os.path.dirname(__file__)) + os.sep + 'bots.txt', 'w') as file:
            for bot in newBotsList:
                file.write("\n" + bot)
                print(bot)

else:
    driver.get("https://9gag.com/login")
    input("Log into 9gag. Press ENTER after login.")

    with open(os.path.realpath(os.path.dirname(__file__)) + os.sep + 'bots.txt', 'r') as file:
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
