import os
import re
import time
import requests
import threading
from bs4 import BeautifulSoup

session_id = ""
getFaceBookUrls = ""
facebookURLS = []
isCounting = True
count = 0


def getSessionID(word, country):
    print("getting SessionID")

    global session_id

    headers = {
        'authority': 'www.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en;q=0.9,ar;q=0.8',
        'cache-control': 'max-age=0',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.199", "Google Chrome";v="114.0.5735.199"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36',
        'viewport-width': '1243',
    }

    response = requests.get(
        f'https://www.facebook.com/ads/library/?active_status=all&country={country}&q=%22{word}%22&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_exact_phrase&media_type=all',
        headers=headers,
    )

    response_text = response.text
    start_index = response_text.find('"sessionId":"') + len('"sessionId":"')
    end_index = response_text.find('"', start_index)
    session_id = response_text[start_index:end_index]

    print(f'Session ID: {session_id}')

    return session_id


def getFrontPageData():
    print("getting front page data")

    global getFaceBookUrls
    # cookies = {
    #     'sb': 'wF36Y4r2DrRKF3UAUfUi7xNV',
    #     'datr': 'wF36Ywi-tOF78ZxsmzlL5jgC',
    #     'c_user': '100080406882587',
    #     'xs': '49%3A4R_E-wI7UXYlDw%3A2%3A1688605020%3A-1%3A15183',
    #     'wd': '1243x961',
    # }
    #
    # headers = {
    #     'authority': 'www.facebook.com',
    #     'accept': '*/*',
    #     'accept-language': 'en-GB,en;q=0.9,ar;q=0.8',
    #     'content-type': 'application/x-www-form-urlencoded',
    #     'origin': 'https://www.facebook.com',
    #     'sec-ch-prefers-color-scheme': 'dark',
    #     'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    #     'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.199", "Google '
    #                                    'Chrome";v="114.0.5735.199"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-ch-ua-platform-version': '"15.0.0"',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-origin',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/114.0.0.0 Safari/537.36',
    #     'viewport-width': '1243',
    #     'x-asbd-id': '129477',
    # }
    #
    # data = {
    #     '__a': '1',
    #     '__req': '1',
    #     '__hs': '19544.BP:DEFAULT.2.0..0.0',
    #     'dpr': '1',
    #     '__ccg': 'MODERATE',
    #     '__csr': '',
    #     'fb_dtsg': 'NAcPZTU4OY4nYl_63_Iq2Tfl8aoYbJJtx1RzZ9cqZaoOZ3FcQkFEzLQ:49:1688605020',
    #     'jazoest': '25466',
    #     'lsd': 'CWOZew8DEz5jZtCyx9jM5a',
    #     '__spin_r': '1007793482',
    #     '__spin_b': 'trunk',
    #     '__spin_t': '1688608067',
    #     '__jssesw': '1',
    # }
    #
    # params = {
    #     'countries[0]': country,
    #     'count': '100',
    #     'is_mobile': 'false',
    #     'q': wordLookup,
    #     'session_id': session_id,
    #     'active_status': 'all',
    #     'ad_type': 'all',
    #     'media_type': 'all',
    #     'sort_data[direction]': 'desc',
    #     'sort_data[mode]': 'relevancy_monthly_grouped',
    #     'search_type': 'keyword_unordered'
    # }
    #
    # response = requests.post(
    #     f'https://www.facebook.com/ads/library/async/search_ads/?q={wordLookup}&session_id={session_id}&count=100&active_status=all&ad_type=all&countries[0]={country}&media_type=all&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered',
    #     cookies=cookies,
    #     headers=headers,
    #     data=data,
    #     params=params
    # )
    import requests

    cookies = {
        'datr': 'CAMCZeE7-YQj7QsVMgYWgWgi',
        'sb': 'CAMCZSE0Pca1LqE_bXgJeiBU',
        'fr': '0whW8Xs4vLLRNCnuK..BlAKp2.xS.AAA.0.0.BlAgML.AWXJffRsS6Q',
        'wd': '982x739',
    }

    headers = {
        'authority': 'www.facebook.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9,ar;q=0.8',
        'origin': 'https://www.facebook.com',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'x-asbd-id': '129477',
        'x-fb-lsd': 'AVpgUcCSck8',
    }

    data = {
        '__user': '0',
        '__a': '1',
        '__req': 'e',
        '__hs': '19614.BP:DEFAULT.2.0..0.0',
        'dpr': '1',
        '__ccg': 'EXCELLENT',
        '__rev': '1008635951',
        '__s': 'qhgqx1:kkza3s:aluixq',
        '__hsi': '7278712979755515907',
        '__csr': '',
        'lsd': 'AVpgUcCSck8',
        'jazoest': '2962',
        '__spin_r': '1008635951',
        '__spin_b': 'trunk',
        '__spin_t': '1694707428',
        '__jssesw': '1',
    }

    response = requests.post(
        f'https://www.facebook.com/ads/library/async/search_ads/?q={wordLookup}&session_id={session_id}&count=100&active_status=all&ad_type=all&countries[0]={country}&media_type=all&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    getFaceBookUrls = response.text

    return response


def counting():
    global isCounting
    global count

    while isCounting:
        time.sleep(1)
        os.system('cls')
        print("getting SessionID")
        print(f'Session ID: {session_id}')
        print("getting front page data")
        print("getting detailed data")
        print("getting profile urls")
        print('getting final data and saving it')
        print(f'time elapsed: {count}')
        count += 1
        counting()


def getDetailedData(content):
    print("getting detailed data")

    global facebookURLS

    urls = re.findall(r'"page_profile_uri":"([^"]+)"', content)

    for uri in urls:
        uri = str(uri).replace('\\', '')
        if uri not in facebookURLS:
            facebookURLS.append(uri)


def getProfileURL(name):
    print("getting profile urls")

    global facebookURLS
    global isCounting

    cookies = {
        'datr': 'CAMCZeE7-YQj7QsVMgYWgWgi',
        'sb': 'CAMCZSE0Pca1LqE_bXgJeiBU',
        'usida': 'eyJ2ZXIiOjEsImlkIjoiQXMwem55czFoem1icmciLCJ0aW1lIjoxNjk0NzE2OTQ4fQ%3D%3D',
        'dpr': '1.25',
        'fr': '0whW8Xs4vLLRNCnuK.AWWKi36XDne62fhZ3TG4kmxxkRA.BlAKp2.xS.AAA.0.0.BlA1SH.AWVwUwdr9r0',
        'wd': '982x739',
    }

    headers = {
        'authority': 'www.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en;q=0.9,ar;q=0.8',
        'cache-control': 'max-age=0',
        # 'cookie': 'datr=CAMCZeE7-YQj7QsVMgYWgWgi; sb=CAMCZSE0Pca1LqE_bXgJeiBU; usida=eyJ2ZXIiOjEsImlkIjoiQXMwem55czFoem1icmciLCJ0aW1lIjoxNjk0NzE2OTQ4fQ%3D%3D; dpr=1.25; fr=0whW8Xs4vLLRNCnuK.AWWKi36XDne62fhZ3TG4kmxxkRA.BlAKp2.xS.AAA.0.0.BlA1SH.AWVwUwdr9r0; wd=982x739',
        'dpr': '1.25',
        'referer': 'https://www.facebook.com/',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-full-version-list': '"Chromium";v="116.0.5845.188", "Not)A;Brand";v="24.0.0.0", "Google Chrome";v="116.0.5845.188"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'viewport-width': '981',
    }

    print('getting final data and saving it')

    # thread = threading.Thread(target=counting)
    # thread.start()
    dataFound = []
    processedData = []
    for profiles in facebookURLS:

        profiles = str(profiles).replace('https://facebook.com/', '')
        response = requests.get(f'https://www.facebook.com/{profiles}/about', cookies=cookies, headers=headers)
        matches = re.findall(r'"field_section_type":"([^"]+)",.*?"text":"([^"]+)"', response.text)
        # print(f'https://www.facebook.com/{profiles}/about')
        # matchRefined = str(matches[2][1]).replace('\\u0040', '@').replace('\\u00b7', '-').replace('\\', '')
        dataFound.append(matches)
    for i in dataFound:
        for j in i:
            for k in j:
                k = str(k.replace(r'\u0040', '@').replace(r'\u00b7', '-').replace('\\', ''))
                processedData.append(k)
    for i in processedData:
        print(i)


        with open(f'{name}.txt', 'a') as file:
            for match in matches:

                matchRefined = str(match[2][1]).replace('\\u0040', '@').replace('\\u00b7', '-').replace('\\', '')
                soup = BeautifulSoup(response.text, 'html.parser')
                print(matchRefined)

                span_element = soup.find('span', string=match[1])
                print(span_element)

                if span_element:
                    class_attribute = ' '.join(span_element.get('class'))
                    print(class_attribute)

                getAllData = soup.find_all('span', class_attribute)

                for data in getAllData:
                    refined = data.getText(strip=True)

                    finalRefined = refined.replace('·', '-')

                    if finalRefined not in dataFound:
                        dataFound.append(str(finalRefined))

                if matchRefined not in dataFound:
                    dataFound.append(matchRefined)
            print("size of array: " + len(dataFound))
            for toWrite in dataFound:
                file.write(toWrite + '\n')
                file.flush()
            file.write('\n')
            file.flush()

    isCounting = False
    # thread.join()


if __name__ == '__main__':
    wordLookup = input("Keyword: ")
    country = input("Country: ")

    formattedWordLookup = wordLookup.replace(' ', '+')
    country.replace(' ', '')

    os.system('cls')

    getSessionID(formattedWordLookup, country)
    getFrontPageData()
    getDetailedData(getFaceBookUrls)
    getProfileURL(wordLookup)
