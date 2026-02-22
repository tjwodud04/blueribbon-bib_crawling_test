'''
블루리본 서베이의 음식점 정보를 가져오는 코드 (This code contains getting Blue Ribbon Sruvey Restaurant info)
링크 (Link) : https://www.bluer.co.kr/search?tabMode=single&searchMode=ribbonType&location=&ribbonType=&feature=
'''
# Necessary libraries
import requests
import pandas as pd
import time

from tqdm import trange
from datetime import datetime

def blueribbon_crawling():
    extracted_list = list()
    # 블루리본 서베이 레스토랑 API 베이스 링크 (Base link)
    base_link = "https://www.bluer.co.kr/api/v1/restaurants"

    response = requests.get(base_link, timeout=10)
    json_contents = response.json()

    for i in trange(json_contents['page']['totalPages']):
        needed_url = base_link + f"?page={i}"
        # 지정된 링크에서 json 형태로 내용 가져오기 (Getting contents as json format from link)
        response = requests.get(needed_url, timeout=10)
        json_contents = response.json()['_embedded']['restaurants']

        for j in range(len(json_contents)):
            try:
                variable_createdate = datetime.utcfromtimestamp(json_contents[j]['createdDate'] / 1000)
                variable_imagedate = datetime.utcfromtimestamp(json_contents[j]['firstImage']['createdDate'] / 1000)

                # 유닉스표현 시간 변환 (Unix time change)
                if (len(str(variable_createdate.month)) == 1) and (len(str(variable_createdate.day)) == 1):
                    json_contents[j]['createdDate'] = int(str(variable_createdate.year) +  '0' + str(variable_createdate.month) + '0' + str(variable_createdate.day))

                elif (len(str(variable_createdate.month)) > 1) and (len(str(variable_createdate.day)) == 1):
                    json_contents[j]['createdDate'] = int(str(variable_createdate.year) +  str(variable_createdate.month) +  '0' + str(variable_createdate.day))

                elif (len(str(variable_createdate.month)) == 1) and (len(str(variable_createdate.day)) > 1):
                    json_contents[j]['createdDate'] = int(str(variable_createdate.year) +  '0' + str(variable_createdate.month) +  str(variable_createdate.day))

                elif (len(str(variable_createdate.month)) > 1) and (len(str(variable_createdate.day)) > 1):
                    json_contents[j]['createdDate'] = int(str(variable_createdate.year) +  str(variable_createdate.month) +  str(variable_createdate.day))

                if (len(str(variable_imagedate.month)) == 1) and (len(str(variable_imagedate.day)) == 1):
                    json_contents[j]['firstImage']['createdDate'] = int(str(variable_imagedate.year) +  '0' + str(variable_imagedate.month) + '0' + str(variable_imagedate.day))

                elif (len(str(variable_imagedate.month)) > 1) and (len(str(variable_imagedate.day)) == 1):
                    json_contents[j]['firstImage']['createdDate'] = int(
                        str(variable_imagedate.year) + str(variable_imagedate.month) + '0' + str(variable_imagedate.day))

                elif (len(str(variable_imagedate.month)) == 1) and (len(str(variable_imagedate.day)) > 1):
                    json_contents[j]['firstImage']['createdDate'] = int(
                        str(variable_imagedate.year) + '0' + str(variable_imagedate.month) + str(variable_imagedate.day))

                elif (len(str(variable_imagedate.month)) > 1) and (len(str(variable_imagedate.day)) > 1):
                    json_contents[j]['firstImage']['createdDate'] = int(
                        str(variable_imagedate.year) + str(variable_imagedate.month) + str(variable_imagedate.day))

            except Exception:
                pass

        # Like Human
        time.sleep(5)

        # 데이터프레임으로 만들기 (Making jsonified contents as dataframe)
        blueribbon_dataframe = pd.json_normalize(json_contents)
        blueribbon_dataframe.columns = blueribbon_dataframe.columns.str.replace('_links', 'links')
        blueribbon_dataframe.columns = blueribbon_dataframe.columns.str.replace('.', '_')
        blueribbon_dataframe['firstImage_url'] = blueribbon_dataframe['firstImage_url'].map(
            'https://www.bluer.co.kr{}'.format, na_action='ignore')

        # csv 파일로 저장
        if i == 0 :
            blueribbon_dataframe.to_csv("./raw_data.csv", mode="w", encoding="utf-8-sig", index = False)
        if i > 0 :
            blueribbon_dataframe.to_csv("./raw_data.csv", mode="a", encoding="utf-8-sig", header=None, index = False)

    return blueribbon_dataframe

# 출력
blueribbon_df_result = blueribbon_crawling()
