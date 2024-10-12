import os
import re
import requests
import json
import csv
import sys

import pandas as pd
import selenium.common
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if len(sys.argv) != 4:
    print("Usage: python main.py <countryCode> <query> <amount_of_ads_to_fetch>")
    exit(1)

countryCode = sys.argv[1]
query = sys.argv[2]
ads_to_fetch = int(sys.argv[3])
prev_ads_fetched = 0
total_ads_fetched = 0
base_url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={countryCode}&media_type=all&q={query}&search_type=keyword_unordered"


driver_path = 'chromedriver-win32/chromedriver.exe'
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-position=-2400,-2400")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get(base_url)
    # prints html content of entire page
    #print(driver.page_source)
    # finds all the page IDS on page CURRENT page.
    # regex pattern: "PERSON_PROFILE","page_id":"[0-9]{15}","page_is_deleted"

    #page_ids = re.findall(r'"PERSON_PROFILE","page_id":"[0-9]{15}","page_is_deleted"', page_source)
    # trimming the page_ids to only include the page_id
    #page_ids = [re.search(r'[0-9]{15}', page_id).group() for page_id in page_ids]

    element = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[4]/div[2]/div[2]/div[4]/div[1]'))
    )

    total_ads_fetched = int(len(re.findall(r'<hr class="[a-z0-9\s]+">', element.get_attribute('innerHTML'))))

    # keep scrolling until we have fetched the required number of ads
    while ads_to_fetch >= total_ads_fetched:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[4]/div[2]/div[2]/div[4]/div[1]'))
        )
        total_ads_fetched = int(len(re.findall(r'<hr class="[a-z0-9\s]+">', element.get_attribute('innerHTML'))))
        if total_ads_fetched != prev_ads_fetched:
            # don't print the same ads again
            print(total_ads_fetched)
            prev_ads_fetched = total_ads_fetched

    # ------------------------------------  MAIN PART  ---------------------------------------- #

    page_source = driver.page_source
    descriptions = re.findall(r'<div style="white-space: pre-wrap;">\s*<span>(.*?)</span>\s*</div>', page_source)
    # remove html tags.

    # clean up the descriptions
    descriptions = [re.sub(r'(<div style="white-space: pre-wrap;">|<span>|</span>|</div>)', '', description) for description in descriptions]
    descriptions = [re.sub(r'&amp;', '&', description) for description in descriptions]
    descriptions = [re.sub(r'&quot;', '"', description) for description in descriptions]
    descriptions = [re.sub(r'&gt;', '>', description) for description in descriptions]
    descriptions = [re.sub(r'&lt;', '<', description) for description in descriptions]
    descriptions = [re.sub(r'&nbsp;', ' ', description) for description in descriptions]
    descriptions = [re.sub(r'&apos;', "'", description) for description in descriptions]
    descriptions = [re.sub(r'&cent;', '¢', description) for description in descriptions]
    descriptions = [re.sub(r'&copy;', '©', description) for description in descriptions]
    descriptions = [re.sub(r'&reg;', '®', description) for description in descriptions]
    descriptions = [re.sub(r'&trade;', '™', description) for description in descriptions]
    descriptions = [re.sub(r'&euro;', '€', description) for description in descriptions]
    descriptions = [re.sub(r'&pound;', '£', description) for description in descriptions]
    descriptions = [re.sub(r'&yen;', '¥', description) for description in descriptions]
    descriptions = [re.sub(r'&mdash;', '—', description) for description in descriptions]
    descriptions = [re.sub(r'&ndash;', '–', description) for description in descriptions]
    descriptions = [re.sub(r'<br>', '\n', description) for description in descriptions]
    descriptions = ['N/A' if description == '' else description for description in descriptions]

    CTA = re.findall(r'<div class=".{92}">([^<]*)</div>', page_source)
    CTA = [re.sub(r'<div class=".{92}">', '', cta) for cta in CTA]
    CTA = [re.sub(r'</div>', '', cta) for cta in CTA]
    CTA.pop(0)


    page_ids = re.findall(r',"page_id":"[0-9]{15}","page_is_deleted"', page_source)
    page_ids = [re.search(r'[0-9]{15}', page_id).group() for page_id in page_ids]
    category = []
    links = []
    id_s = []
    best_description = []
    page_names = []
    profile_links = []

    for ids in page_ids:
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.facebook.com',
            'priority': 'u=1, i',
            'referer': 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&media_type=all&q=housing&search_type=keyword_unordered',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.90", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.90"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }

        data = {
            'variables': '{"pageID":"' + ids + '"}',
            'doc_id': '6453683764688391',
        }

        response = requests.post('https://www.facebook.com/api/graphql/', headers=headers, data=data)

        # print(response.text)

        compiled_data = json.loads(response.text)
        category.append(compiled_data['data']['page']['category_name'])
        links.append(compiled_data['data']['page']['websites'])
        id_s.append(compiled_data['data']['page']['id'])
        page_names.append(compiled_data['data']['page']['name'])
        profile_links.append(compiled_data['data']['page']['url'])


        if compiled_data['data']['page']['best_description'] is not None:
            best_description.append(compiled_data['data']['page']['best_description']['text'])
        else:
            best_description.append('N/A')

    # fill the rest of the unfound descriptions with 'N/A'
    while len(descriptions) < len(page_ids):
        descriptions.append('N/A')

    # sessionID = re.findall(',"sessionID":".{36}","', page_source)
    # sessionID = list(dict.fromkeys([re.search('".{36}"', sessionID).group() for sessionID in sessionID]))[0].replace('"', '')

    # write the collected data to a csv file
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Category', 'Page Names', 'Description', 'Best Description', 'Link', 'CTA', 'Profile Link'])
        for i in range(len(page_names)):
            writer.writerow([id_s[i], category[i], page_names[i], descriptions[i], best_description[i], links[i], CTA[i]])


    # get the profile data

    address = []
    mobile_number = []
    email = []
    websites_and_social_links = []
    index = 0

    for profile_link in profile_links:

        # check to see if the profile link is a facebook marketplace link
        if '/marketplace/profile/' in profile_link:
            # skip this link
            print(f"Skipping {profile_link} as it is a facebook marketplace link.")
            continue

        driver.get(f"{profile_link}/?sk=about")

        # waits for data to load
        loaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div'
                           '/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div'))
        )

        try:
            address.append(driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]'
                                                         '/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div'
                                                         '/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[2]'
                                                         '/div[1]/span').text)
        except selenium.common.NoSuchElementException as e:
            # address does not exist???
            address.append("N/A")
            pass

        try:
            mobile_number.append(driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div'
                                                               '/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div'
                                                               '/div/div/div/div[2]/div/div/div/div[2]/div/div[3]/div'
                                                               '/div/div[2]/ul/li/div/div/div[1]/span').text)
        except selenium.common.NoSuchElementException as e:
            # mobile number does not exist???
            mobile_number.append("N/A")
            pass

        try:
            email.append(driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]'
                                                       '/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]'
                                                       '/div/div/div/div[2]/div/div[4]/div/div/div[2]/ul/li/div/div'
                                                       '/div[1]/span').text)
        except selenium.common.NoSuchElementException as e:
            # email does not exist???
            email.append("N/A")
            pass

        try:
            websites_and_social_links.append(driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div'
                                                                           '/div[3]/div/div/div[1]/div[1]/div/div/div[4]'
                                                                           '/div/div/div/div[1]/div/div/div/div/div[2]'
                                                                           '/div/div/div/div[3]/div').text)
        except selenium.common.NoSuchElementException as e:
            # websites and social links do not exist???
            websites_and_social_links.append("N/A")
            pass

        print(f"processed {profile_link} out of {index + 1} out of {len(profile_links)}")
        index += 1

    # Read the existing CSV file
    existing_data = pd.read_csv('output.csv')

    # Create a new DataFrame with the new data
    new_data = pd.DataFrame({
        'Profile Link': profile_links,
        'Address': address,
        'Mobile Number': mobile_number,
        'Email': email,
        'Websites and Social Links': websites_and_social_links
    })

    # Write both DataFrames to the same CSV file, each in a separate sheet
    with pd.ExcelWriter('output_file.xlsx') as writer:
        existing_data.to_excel(writer, sheet_name='Ad Info', index=False)
        new_data.to_excel(writer, sheet_name='Account Info', index=False)

    os.system("pause")


except PermissionError as e:
    print("Please close the csv file before running the script.")
    print("An error occurred:", e)
    driver.quit()
    exit(1)
except Exception as e:
    print("An error occurred:", e)
finally:
    os.system('pause')
    driver.quit()
    exit(0)
