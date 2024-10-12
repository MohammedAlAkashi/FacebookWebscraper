"""
Creative Commons Legal Code

CC0 1.0 Universal

    CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM AND DOES NOT PROVIDE
    LEGAL SERVICES. DISTRIBUTION OF THIS DOCUMENT DOES NOT CREATE AN
    ATTORNEY-CLIENT RELATIONSHIP. CREATIVE COMMONS PROVIDES THIS
    INFORMATION ON AN "AS-IS" BASIS. CREATIVE COMMONS MAKES NO WARRANTIES
    REGARDING THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS
    PROVIDED HEREUNDER, AND DISCLAIMS LIABILITY FOR DAMAGES RESULTING FROM
    THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS PROVIDED
    HEREUNDER.

Statement of Purpose

The laws of most jurisdictions throughout the world automatically confer
exclusive Copyright and Related Rights (defined below) upon the creator
and subsequent owner(s) (each and all, an "owner") of an original work of
authorship and/or a database (each, a "Work").

Certain owners wish to permanently relinquish those rights to a Work for
the purpose of contributing to a commons of creative, cultural and
scientific works ("Commons") that the public can reliably and without fear
of later claims of infringement build upon, modify, incorporate in other
works, reuse and redistribute as freely as possible in any form whatsoever
and for any purposes, including without limitation commercial purposes.
These owners may contribute to the Commons to promote the ideal of a free
culture and the further production of creative, cultural and scientific
works, or to gain reputation or greater distribution for their Work in
part through the use and efforts of others.

For these and/or other purposes and motivations, and without any
expectation of additional consideration or compensation, the person
associating CC0 with a Work (the "Affirmer"), to the extent that he or she
is an owner of Copyright and Related Rights in the Work, voluntarily
elects to apply CC0 to the Work and publicly distribute the Work under its
terms, with knowledge of his or her Copyright and Related Rights in the
Work and the meaning and intended legal effect of CC0 on those rights.

1. Copyright and Related Rights. A Work made available under CC0 may be
protected by copyright and related or neighboring rights ("Copyright and
Related Rights"). Copyright and Related Rights include, but are not
limited to, the following:

  i. the right to reproduce, adapt, distribute, perform, display,
     communicate, and translate a Work;
 ii. moral rights retained by the original author(s) and/or performer(s);
iii. publicity and privacy rights pertaining to a person's image or
     likeness depicted in a Work;
 iv. rights protecting against unfair competition in regards to a Work,
     subject to the limitations in paragraph 4(a), below;
  v. rights protecting the extraction, dissemination, use and reuse of data
     in a Work;
 vi. database rights (such as those arising under Directive 96/9/EC of the
     European Parliament and of the Council of 11 March 1996 on the legal
     protection of databases, and under any national implementation
     thereof, including any amended or successor version of such
     directive); and
vii. other similar, equivalent or corresponding rights throughout the
     world based on applicable law or treaty, and any national
     implementations thereof.

2. Waiver. To the greatest extent permitted by, but not in contravention
of, applicable law, Affirmer hereby overtly, fully, permanently,
irrevocably and unconditionally waives, abandons, and surrenders all of
Affirmer's Copyright and Related Rights and associated claims and causes
of action, whether now known or unknown (including existing as well as
future claims and causes of action), in the Work (i) in all territories
worldwide, (ii) for the maximum duration provided by applicable law or
treaty (including future time extensions), (iii) in any current or future
medium and for any number of copies, and (iv) for any purpose whatsoever,
including without limitation commercial, advertising or promotional
purposes (the "Waiver"). Affirmer makes the Waiver for the benefit of each
member of the public at large and to the detriment of Affirmer's heirs and
successors, fully intending that such Waiver shall not be subject to
revocation, rescission, cancellation, termination, or any other legal or
equitable action to disrupt the quiet enjoyment of the Work by the public
as contemplated by Affirmer's express Statement of Purpose.

3. Public License Fallback. Should any part of the Waiver for any reason
be judged legally invalid or ineffective under applicable law, then the
Waiver shall be preserved to the maximum extent permitted taking into
account Affirmer's express Statement of Purpose. In addition, to the
extent the Waiver is so judged Affirmer hereby grants to each affected
person a royalty-free, non transferable, non sublicensable, non exclusive,
irrevocable and unconditional license to exercise Affirmer's Copyright and
Related Rights in the Work (i) in all territories worldwide, (ii) for the
maximum duration provided by applicable law or treaty (including future
time extensions), (iii) in any current or future medium and for any number
of copies, and (iv) for any purpose whatsoever, including without
limitation commercial, advertising or promotional purposes (the
"License"). The License shall be deemed effective as of the date CC0 was
applied by Affirmer to the Work. Should any part of the License for any
reason be judged legally invalid or ineffective under applicable law, such
partial invalidity or ineffectiveness shall not invalidate the remainder
of the License, and in such case Affirmer hereby affirms that he or she
will not (i) exercise any of his or her remaining Copyright and Related
Rights in the Work or (ii) assert any associated claims and causes of
action with respect to the Work, in either case contrary to Affirmer's
express Statement of Purpose.

4. Limitations and Disclaimers.

 a. No trademark or patent rights held by Affirmer are waived, abandoned,
    surrendered, licensed or otherwise affected by this document.
 b. Affirmer offers the Work as-is and makes no representations or
    warranties of any kind concerning the Work, express, implied,
    statutory or otherwise, including without limitation warranties of
    title, merchantability, fitness for a particular purpose, non
    infringement, or the absence of latent or other defects, accuracy, or
    the present or absence of errors, whether or not discoverable, all to
    the greatest extent permissible under applicable law.
 c. Affirmer disclaims responsibility for clearing rights of other persons
    that may apply to the Work or any use thereof, including without
    limitation any person's Copyright and Related Rights in the Work.
    Further, Affirmer disclaims responsibility for obtaining any necessary
    consents, permissions or other rights required for any use of the
    Work.
"""


import os
import re
import requests
import json
import csv
import sys
import logging

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

"""
USED FOR TEST CASES
countryCode = 'US'
query = 'housing' 
ads_to_fetch = 10
"""

prev_ads_fetched = 0
total_ads_fetched = 0
base_url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={countryCode}&media_type=all&q={query}&search_type=keyword_unordered"
driver_path = 'chromedriver-win32/chromedriver.exe'

options = Options()
options.add_argument("--log-level=3")  # Suppress console logs
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Set logging level to WARNING
logging.getLogger('selenium').setLevel(logging.WARNING)
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
        EC.presence_of_element_located((By.XPATH,
                                        '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[4]/div[2]/div[2]/div[4]/div[1]'))
    )
    # get the total number of ads fetched
    total_ads_fetched = int(len(re.findall(r'<hr class="[a-z0-9\s]+">', element.get_attribute('innerHTML'))))

    # we already have all the ads we need no need to scroll
    if total_ads_fetched >= ads_to_fetch:
        print(f"100% of ads fetched.")

    # keep scrolling until we have fetched the required number of ads
    while ads_to_fetch >= total_ads_fetched:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[4]/div[2]/div[2]/div[4]/div[1]'))
        )
        total_ads_fetched = int(len(re.findall(r'<hr class="[a-z0-9\s]+">', element.get_attribute('innerHTML'))))
        if total_ads_fetched != prev_ads_fetched:
            # don't print the same ads again
            # converts to a percentage
            print(f"{total_ads_fetched / ads_to_fetch * 100}% of ads fetched.")
            prev_ads_fetched = total_ads_fetched

    # ------------------------------------  MAIN PART  ---------------------------------------- #

    # get the page source
    page_source = driver.page_source

    # get the descriptions
    descriptions = re.findall(r'<div style="white-space: pre-wrap;">\s*<span>(.*?)</span>\s*</div>', page_source)

    # clean up the descriptions
    descriptions = [re.sub(r'(<div style="white-space: pre-wrap;">|<span>|</span>|</div>)', '', description) for
                    description in descriptions]
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

    # get the CTA
    CTA = re.findall(r'<div class=".{92}">([^<]*)</div>', page_source)
    CTA = [re.sub(r'<div class=".{92}">', '', cta) for cta in CTA]  # remove the div tag
    CTA = [re.sub(r'</div>', '', cta) for cta in CTA]  # remove the closing div tag
    CTA.pop(0)  # remove the first element as it is not a CTA

    # get the page ids
    page_ids = re.findall(r',"page_id":"[0-9]{15}","page_is_deleted"', page_source)
    page_ids = [re.search(r'[0-9]{15}', page_id).group() for page_id in
                page_ids]  # trimming the page_ids to only include the page_id

    # values to be collected
    category = []
    links = []
    id_s = []
    best_description = []
    page_names = []
    profile_links = []

    # go over each page id and get the required data...
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

        compiled_data = json.loads(response.text)  # convert the response to a json object
        category.append(compiled_data['data']['page']['category_name'])  # get the category
        links.append(compiled_data['data']['page']['websites'])  # get the links
        id_s.append(compiled_data['data']['page']['id'])  # get the id
        page_names.append(compiled_data['data']['page']['name'])  # get the page name
        profile_links.append(compiled_data['data']['page']['url'])  # get the profile link

        # get the best description
        if compiled_data['data']['page']['best_description'] is not None:
            best_description.append(compiled_data['data']['page']['best_description']['text'])
        else:
            best_description.append('N/A') # no best description found

    # fill the rest of the unfounded descriptions with "N/A"
    while len(descriptions) < len(page_ids):
        descriptions.append('N/A')

    # fill the rest of the un found CTA with 'N/A"
    while len(CTA) < len(page_ids):
        CTA.append('N/A')

    # uncomment the following code to get the sessionID
    # un needed at the moment but might get used later on.
    # sessionID = re.findall(',"sessionID":".{36}","', page_source)
    # sessionID = list(dict.fromkeys([re.search('".{36}"', sessionID).group() for sessionID in sessionID]))[0].replace('"', '')

    # write the collected data to a temp csv file
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['ID', 'Category', 'Page Names', 'Description', 'Best Description', 'Link', 'CTA', 'Profile Link'])
        for i in range(len(page_names)):
            writer.writerow(
                [id_s[i], category[i], page_names[i], descriptions[i], best_description[i], links[i], CTA[i]])

    # get the profile data
    # data from profile to be collected
    address = []
    mobile_number = []
    email = []
    websites_and_social_links = []
    index = 0
    previous_profile_links = []

    # iterate over each profile link and get the required data
    for profile_link in profile_links:

        # skip duplicate profile links to avoid unnecessary requests
        if profile_link in previous_profile_links:
            print(f"Skipping {profile_link} as it is a duplicate.")
            index += 1
            continue

        previous_profile_links.append(profile_link)  # add the profile link to the list of previous profile links

        # check to see if the profile link is a facebook marketplace link
        if '/marketplace/' in profile_link:
            # skip this link
            print(f"Skipping {profile_link} as it is a facebook marketplace link.")
            index += 1
            continue

        # go to the profile link as it is a valid link
        driver.get(f"{profile_link}/?sk=about")

        # wait for required data to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div'
                           '/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div'))
        )

        # get the address, mobile number, email, and websites and social links
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

        # print the progress
        print(f"processed {profile_link} out of {index + 1} out of {len(profile_links)}")
        index += 1

    # remove duplicate profile links.
    profile_links = list(dict.fromkeys(profile_links))

    # add N/A to the rest of the unfounded values
    while len(address) < len(profile_links):
        address.append('N/A')
    while len(mobile_number) < len(profile_links):
        mobile_number.append('N/A')
    while len(email) < len(profile_links):
        email.append('N/A')
    while len(websites_and_social_links) < len(profile_links):
        websites_and_social_links.append('N/A')

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

    # delete the now unneeded csv file
    os.remove('output.csv')


except PermissionError as e:
    print("Please close the csv file before running the script.")  # most likely the file is open
    print("An error occurred:", e)
    driver.quit()
    exit(1)
except Exception as e:
    print("An error occurred:", e)  # some other error that should not have occurred ( unless the code gets patched )
finally:
    os.system('pause') # pause the script to allow the user to see the output
    driver.quit()
    exit(0)
