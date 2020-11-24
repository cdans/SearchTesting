from selenium import webdriver
from time import sleep
import pandas as pd
import os


def testSearch(lagerPLZ):

  # Hauptordner erstellen, falls der noch nicht existiert
  path = "Fotos_der_Suche"
  try:
    os.mkdir(path)
  except OSError:
    print ("Creation of the directory %s failed" % path)
  else:
    print ("Successfully created the directory %s " % path)

  # Subordner pro PLZ erstellen, falls der noch nicht existiert
  try:
    os.mkdir(path + "/" + lagerPLZ)
  except OSError:
    print ("Creation of the directory %s failed" % (path + "/" + lagerPLZ))
  else:
    print ("Successfully created the directory %s " % (path + "/" + lagerPLZ))

  # Starten und HTLP bearbeiten
  driver = webdriver.Firefox()
  driver.get('https://www.flaschenpost.de')
  zipcodeInput = driver.find_element_by_xpath('//*[@id="validZipcode"]')
  zipcodeInput.send_keys(lagerPLZ)
  zipcodeInputEnter = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/button')
  zipcodeInputEnter.click()

  # csv 'testset.csv' einlesen (Test-Suchbegriffe)
  top = pd.read_csv("testset.csv", header=0, usecols=['Suchbegriff'])
  print(top)

  #Variabel zur Nummerierung der Fotos je Lager
  x = 1

  # Suchen und Screenshots erstellen
  for i in top['Suchbegriff']:
    print(lagerPLZ + "_" + str(x) + "_" + i + '.png')
    # Zusammensuchen der Objekte die benötigt werden
    searchIcon = driver.find_element_by_xpath('/html/body/div[1]/header/div[3]/div/div[2]/div[1]/div/div')
    searchTerm = driver.find_element_by_xpath('//*[@id="searchTerm"]')
    searchTermSubmit = driver.find_element_by_xpath('//*[@id="search-form-header"]/div[1]/button')
    sleep(1)
    # Suche öffnen
    searchIcon.click()
    sleep(1)
    # Suchbegriff übergeben
    searchTerm.send_keys(i)
    sleep(1)
    # Suche ausführen
    searchTermSubmit.click()
    sleep(5)
    # Part zum Screenshot suchen
    body = driver.find_element_by_xpath('/html/body')
    sleep(4)
    # Screensjot ausführen
    element_png = body.screenshot_as_png
    sleep(3)
    #Screenshot speichern
    with open(path + "/" + lagerPLZ + "/" + lagerPLZ + "_" + str(x) + "_" + i + ".png", "wb") as file:
      file.write(element_png)
      sleep(1)  # body.screenshot(i + '.png')
    # Nummer des Screenshots inkrementieren
    x += 1

#Suche für alle 3 Standorte laufen lassen
#testSearch("48151")
sleep(1)
#testSearch("50667")
sleep(1)
testSearch("20249")