
Bulk Part Scraper with Price Breaks
This Python script is designed to scrape electronic component data from multiple web pages using web scraping.

📌 Script Features:
Reads product links or part numbers from an Excel file (i.xlsx)

Opens each link and analyzes the page using SeleniumBase

Extracts detailed information about each product:

Part Number

Manufacturer

Stock Availability

Buy Now Link

Quantity Breaks and Corresponding Prices

Saves the results in a CSV file automatically generated with a timestamp in its name

📁 Project Contents:
IBS.py: The main script file

i.xlsx: Input Excel file containing product links or part numbers

*.csv: Output results file (automatically generated)

🧰 Requirements:
Make sure the following libraries are installed:

bash
نسخ
تحرير
pip install pandas openpyxl seleniumbase lxml

