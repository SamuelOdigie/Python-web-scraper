import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import time

def check_price():
    URL = "https://www.amazon.co.uk/s?k=iphone+13&crid=2EZ3W7TJAHAZY&sprefix=iphone+13%2Ccaps%2C81&ref=nb_sb_noss_1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    price_element = soup.find("span", class_="a-price-whole")
    if price_element:
        price = float(price_element.get_text().replace(",", ""))
        if price < 600.0:
            send_notification(price)
    else:
        # Handle the case where the price element was not found
        print("Price element not found.")

def send_notification(price):
    # Replace the values of the following variables with your own information
    from_address = "your_email_address@example.com"
    to_address = "destination_email_address@example.com"
    password = "your_email_password"
    
    message = MIMEText(f"The price of iPhone 13 has dropped to £{price} on Amazon UK.")
    message["From"] = from_address
    message["To"] = to_address
    message["Subject"] = "Price drop alert: iPhone 13 on Amazon UK"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(from_address, password)
        server.send_message(message)

while True:
    check_price()
    time.sleep(60 * 60) # Check the price once an hour
