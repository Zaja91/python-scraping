import requests
import smtplib
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome() # Instance of Chrome() class
driver.get('https://www.trovaprezzi.it/')

search_input = driver.find_element_by_xpath('//*[@id="libera"]')
search_input.send_keys('google pixel 4a')

search_button = driver.find_element_by_xpath('/html/body/header/div[2]/div/form/button')
search_button.click()