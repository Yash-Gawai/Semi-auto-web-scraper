from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv
import time
import smtplib
from email.message import EmailMessage
import os

URL = "https://www.flipkart.com/boat-rockerz-370-bluetooth-headset/p/itm89f0396e15fef?pid=ACCFPDSFAZ8DG43U&lid=LSTACCFPDSFAZ8DG43UBEH7VL&marketplace=FLIPKART&q=headphones&store=0pm%2Ffcn&srno=s_6_226&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&fm=search-autosuggest&iid=fbb06042-8245-47d3-b9e4-8363bb21c593.ACCFPDSFAZ8DG43U.SEARCH&ppt=sp&ppn=sp&ssid=jxaq4z3ofk0000001651221211476&qH=edd443896ef5dbfc"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"}

page = requests.get(URL, headers = headers)
soup1 = BeautifulSoup(page.content, "html.parser")
soup2 = BeautifulSoup(soup1.prettify(),"html.parser")
title = soup2.find(class_ = "B_NuCI").get_text().strip().split("\n")
#print(title[0]+""+title[-1].strip())
price = soup2.find(class_ = "_30jeq3 _16Jk6d").get_text().strip()
price = int(price[1:].replace(",",""))
#print(price)
alert1 = soup2.find(class_ = "_2JC05C") # hurry only 1 left alert ->becomes a None object when the alert isn't there
#print(type(alert1))
if alert1!=None:
    alert1 = alert1.get_text().strip()
else:
    alert1 = "None"
#print(type(alert1))
alert2 = soup2.find(class_ = "_1NQ_ER") # out of stock in the pincode ->becomes a None object when item is in stock
if alert2 != None:
    alert2 = alert2.get_text().strip()
else:
    alert2 = "None"
star_rating = soup2.find(class_ = "_3LWZlK").get_text().strip()
#print(star_rating + " stars")
rating_numbers = soup2.find(class_ = "_2_R_DZ").get_text().strip().split("\n")
# print(rating_numbers[0])
# print(rating_numbers[6].strip())
number_of_ratings = rating_numbers[0]
number_of_reviews = rating_numbers[-1].strip()
today1 = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")

# print(today1)
# Header and data are the columns in the csv file
header = ["title","price in Rupees","star_rating","Number of ratings","Number of reviews","date","alert1","alert2"]
data = [title[0]+""+title[-1].strip(),price,star_rating,int(number_of_ratings[:-8].replace(",","")),int(number_of_reviews[:-8].replace(",","")),today1,alert1,alert2]

with open("Flipkart_data.csv","w",newline = "",encoding="UTF8") as f: # Writing the data to a csv file
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)

# For mailing on having alert
email_id = os.environ.get("----------------")
email_pswd = os.environ.get("-----------------")
def mailing_service(alert,URL):
    msg = EmailMessage()
    msg["Subject"] = "{}".format(alert)
    msg["From"] = email_id
    msg["To"] = "-----------------"
    msg.set_content("Check the item at {}".format(URL))

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        smtp.login(email_id,email_pswd)
        smtp.send_message(msg)


# Function is called for updating the existing values at specified times
def data_collection():
    title = soup2.find(class_ = "B_NuCI").get_text().strip().split("\n")
    price = soup2.find(class_ = "_30jeq3 _16Jk6d").get_text().strip()
    price = int(price[1:].replace(",",""))
    alert1 = soup2.find(class_ = "_2JC05C") # hurry only 1 left alert ->disappears if not there
    if alert1!=None:
        alert1 = alert1.get_text().strip()
        mailing_service(alert1,URL)
    else:
        alert1 = "None"
    alert2 = soup2.find(class_ = "_1NQ_ER") # out of stock in the pincode ->disappears if not there
    if alert2 != None:
        alert2 = alert2.get_text().strip()
        mailing_service(alert2,URL)
    else:
        alert2 = "None"
    star_rating = soup2.find(class_ = "_3LWZlK").get_text().strip()
    rating_numbers = soup2.find(class_ = "_2_R_DZ").get_text().strip().split("\n")
    number_of_ratings = rating_numbers[0]
    number_of_reviews = rating_numbers[-1].strip()
    today1 = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")


    data = [title[0]+""+title[-1].strip(),price,star_rating,int(number_of_ratings[:-8].replace(",","")),int(number_of_reviews[:-8].replace(",","")),today1,alert1,alert2]
    with open("Flipkart_data.csv","a+",newline = "",encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(data)

# Running the program for specified time or forever
count = 0 # Comment this out to run this indefinitely
while True:
    data_collection()
    time.sleep(5) # x seconds delay in running the script. 1 day = 86400 seconds
    count+=1 # Comment this out to run this indefinitely
    if count >= 10: # Comment this out to run this indefinitely
        break # Comment this out to run this indefinitely