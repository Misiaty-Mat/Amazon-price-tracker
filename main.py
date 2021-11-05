from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import lxml
import smtplib
import os


# Give value to the variables bellow
SMTP_SERVER = "smtp.gmail.com"  # SMTP server on which your e-mail is hosted
EMAIL_RECIVER = "m.a.s.m@interia.pl"  # To who is e-mail supposed to go

# URL to Amazon product to watch for
URL = ""

# When price of the product is below target price e-mail will be sended
TARGET_PRICE = 600

# Loading enviroment from .env file
load_dotenv()

# Getting high value variables from enviromen
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

USER_AGENT = os.environ.get("USER_AGENT")
ACCEPT_LANGUAGE = os.environ.get("ACCEPT_LANGUAGE")

# Setting headers to Amazon webside
headers = {"User-Agent": SMTP_SERVER, "Accept-Language": ACCEPT_LANGUAGE}

# Getting response from product webside
response = requests.get(url=URL, headers=headers)
response.raise_for_status()

# Product webside code
product_web_page = response.text

# Starting soup
amazon_soup = BeautifulSoup(product_web_page, "lxml")

# Title of the product from webside
product_title_tag = amazon_soup.find(name="span", id="productTitle")
product_title = product_title_tag.get_text().strip()

# Price of the product on webside
product_price_tag = amazon_soup.find(name="span", class_="a-offscreen")
product_price_string = product_price_tag.text

# Cutting "product_price_string" itno 2 variables
# "currency" - string of the currency user have on his Amazon product webpage
# "no_currency_list" - pure price nubers list to convert
currency = ""
no_currency_list = []
for char in product_price_string:
    if char.isnumeric():
        no_currency_list.append(char)
    else:
        currency += char

# Converting price to float
price_no_currency = "".join(no_currency_list)
price_no_currency = price_no_currency[:-2] + "." + price_no_currency[-2:]

price = float(price_no_currency)


# Formating currency to look better in e-mail
currency = currency.replace(",", "")
currency = currency.replace("\xa0", "")
currency = currency.replace("\u0142", "l")


# Sending e-mail on price bellow target
if price <= TARGET_PRICE:
    msg = f"Subject:Amazon low price alert!\n\n{product_title} is currently below your target price.\nPrice: {price_no_currency} {currency}"

    with smtplib.SMTP(SMTP_SERVER) as connection:
        connection.starttls()
        connection.login(user=EMAIL_SENDER, password=EMAIL_PASSWORD)
        connection.sendmail(from_addr=EMAIL_SENDER, to_addrs=EMAIL_RECIVER, msg=msg)
        print("E-mail sended")
