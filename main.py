# coding=utf-8
from selenium import webdriver
from time import sleep
import pandas as pd


from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import TimeoutException 



delay = 15 # seconds 

def waiting(driver):
  try: 
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'body'))) 
    print ("Page is ready!") 
  except TimeoutException: 
    print ("Loading took too much time!")



def testSearch(lagerPLZ):
    # Starten und HTLP übergehen
    driver = webdriver.Firefox()
    driver.get('https://www.flaschenpost.de')
    waiting(driver)
    zipcodeInput = driver.find_element_by_xpath('//*[@id="validZipcode"]')
    zipcodeInput.send_keys(lagerPLZ)

    zipcodeInputEnter = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/button')
    zipcodeInputEnter.click()
    waiting(driver)

    # csv einlesen (Suchbegriffe)
    top = pd.read_csv("testset.csv", header=0, usecols=['Suchbegriff'])
    print(top)

    # Suchen und Screenshots erstellen
    x = 1

    for i in top['Suchbegriff']:
        print(lagerPLZ + "_" + str(x) + "_" + i + '.png')
        searchIcon = driver.find_element_by_xpath('/html/body/div[1]/header/div[3]/div/div[2]/div[1]/div/div')
        searchTerm = driver.find_element_by_xpath('//*[@id="searchTerm"]')
        searchTermSubmit = driver.find_element_by_xpath('//*[@id="search-form-header"]/div[1]/button')
        sleep(1)
        searchIcon.click()
        sleep(1)
        searchTerm.send_keys(i)
        sleep(1)
        searchTermSubmit.click()
        sleep(2)
        body = driver.find_element_by_xpath('/html/body')
        sleep(3)
        element_png = body.screenshot_as_png
        sleep(3)
        with open(lagerPLZ + "_" + str(x) + "_" + i + ".png", "wb") as file:
            file.write(element_png)
            sleep(1)  # body.screenshot(i + '.png')
        x += 1


# checkEmpty("21", "38440")
testSearch("48151")
testSearch("50667")
testSearch("20249")