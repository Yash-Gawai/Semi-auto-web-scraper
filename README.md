# Flipkart-semi-automated-web-scraper

Currently the URL points to boAt Rockerz 370 Bluetooth Headset  (Buoyant Black, On the Ear) on Flipkart

The script collects the product title, price, rating, number of reviews, number of ratings, the time when the script has updated and 2 sets of alerts.

Alert 1 is only shown when "Hurry only 1 item left!" is shown on the website.
Alert 2 is only shown when the item is out of stock for the default pincode that the browser autocompletes when you have signed in on Flipkart.

Both the alerts become None items when they are missing and the csv lists the field as "None".

When either one is present, the script notifies the user by mailing them.
