import pandas as pd
import os.path
from datetime import datetime
from seleniumbase import Driver
import time
import random
from lxml import etree

file_name = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '.csv'

driver = Driver(uc=True)
driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
    "origin": '*',
    "storageTypes": 'all',
})
counter=1
try:
    df = pd.read_excel('i2.xlsx', engine='openpyxl')
    print("Excel file loaded successfully")
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit()

header = ['Input_BuyNow', 'JSON']
for i in range(1, 10):
    header.extend([f'Break{i}', f'Price{i}'])

# Add columns for all additional data elements (up to 8 of each type)
for i in range(1, 9):
    header.extend([f'AdditionalData1_{i}', f'AdditionalData2_{i}'])

if not os.path.isfile(file_name):
    with open(file_name, mode='w', encoding='utf-8') as file:
        file.write('|'.join(header) + '\n')

for index, url in df['BuyNow'].items():
    print(f"Processing URL: {url}")
    
    try:
        driver.get(url)
        page_source = driver.page_source
        html_tree = etree.HTML(page_source)
        
        json_data = html_tree.xpath('//script[@type="application/ld+json"]/text()')
        json_str = json_data[0] if json_data else "NULL"
        
        breaks = html_tree.xpath('//div[@class="[ stack ]"]//span[@class="[ price-break-min ]"]/text()')
        prices = html_tree.xpath('//div[contains(@class,"price-break-row")]//span[contains(.,"$")]/text()')
        
        # Get all matching elements for both additional data types
        additional_data_1 = [x.strip() for x in html_tree.xpath('//div[@class="flex flex-col gap-1"]//div[contains(@class,"text-18")]/div[1]/text()')]
        additional_data_2 = [x.strip() for x in html_tree.xpath('//div[@class="flex flex-col gap-1"]//div[contains(@class,"text-18")]/div[2]/text()')]
        
        row_data = {
            'Input_BuyNow': url,
            'JSON': json_str.replace('\n', ' ').replace('|', ' ')
        }
        
        # Add breaks and prices
        for i in range(1, 10):
            row_data[f'Break{i}'] = breaks[i-1].strip() if i <= len(breaks) else "NULL"
            row_data[f'Price{i}'] = prices[i-1].strip() if i <= len(prices) else "NULL"
        
        # Add additional data (up to 8 of each type)
        for i in range(1, 9):
            row_data[f'AdditionalData1_{i}'] = additional_data_1[i-1] if i <= len(additional_data_1) else "NULL"
            row_data[f'AdditionalData2_{i}'] = additional_data_2[i-1] if i <= len(additional_data_2) else "NULL"
        
        with open(file_name, mode='a', encoding='utf-8') as file:
            file.write('|'.join([str(row_data.get(col, "NULL")) for col in header]) + '\n')
        print(counter)
        counter+=1
        print(f"Successfully processed: {url}")
        
    except Exception as e:
        print(f"Error processing {url}: {e}")
        with open(file_name, mode='a', encoding='utf-8') as file:
            file.write('|'.join([url, "ERROR"] + ["NULL"]*(len(header)-2)) + '\n')

driver.quit()
print("Processing completed successfully!")
