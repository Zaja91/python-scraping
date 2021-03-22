# Script shell che aggiunge la possibilita di tenere "d'occhio" il prezzo di un prodotto tramite trovaprezzi.it
import requests
import smtplib
import time
import sys
import webbrowser

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



# Ask User for product name
def ask_user_product():
    user_search = input("Inserisci l'articolo che stai cercando:")
    return user_search

# Search product on trovaprezzi.it
def search_product(name):
    driver = webdriver.Chrome() # Instance of Chrome() class
    driver.get('https://www.trovaprezzi.it/')
    search_input = driver.find_element_by_xpath('//*[@id="libera"]')
    search_input.send_keys(name)
    search_button = driver.find_element_by_xpath('/html/body/header/div[2]/div/form/button')
    search_button.click()
    return driver

# Extract the price tag from html elemente and transform pass it as int
def extract_price(s):
    return int(s.find(class_="price_range")
                 .get_text()
                 .replace('.', '')[13:-5]) 

# Ask User for the maximum price that he would like to pay for the product
def user_max_price():
    return int(input("Quale è il prezzo massimo che sei disposto a pagare per questo prodotto?"))

# Send email with link to the product page
def send_email(d):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('andrew.terni@gmail.com', 'dwjhemtfunoorpdq')

    subject = "Avviso prodotto sotto il prezzo da te indicato!!!"
    body = 'Il prodotto da te selezionato si trova a questo link:' + d.  current_url

    msg = f"Subject: {subject}\n\n {body}"
    server.sendmail(
        'andrew.terni@gmail.com',
        'yagos.terni@gmail.com',
        msg
    )
    server.quit()
    
# Check the price of item and compare it to what the User price tag is
def check_price(d):
    URL = driver.current_url
    
    headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    
    page = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    # Extract price from string and convert it to int
    current_price = extract_price(soup)
    
    # Ask user maximum price that he would be able to pay for the product
    # and compare it to the current price
    user_price = user_max_price()
    if (user_price <= current_price):
        send_email(d)
        print("Email has been sent")    
    else:
        print("Ti invieremo un email appena il prodotto scendera sotto il prezzo da te indicato.")


driver = search_product(ask_user_product())

# Run this script every hour
while(True):
    check_price(driver)
    time.sleep(3600)

