'''
블루리본 서베이의 음식점 정보의 필요한 변수를 가져오는 코드 (This code contains getting Blue Ribbon Sruvey Restaurant info)
링크 (Link) : https://www.bluer.co.kr/search?tabMode=single&searchMode=ribbonType&location=&ribbonType=&feature=
'''
# Necessary libraries
import requests
import pandas as pd

from tqdm import trange
from datetime import datetime

def blueribbon_crawling():
    # 블루리본 서베이 레스토랑 API 베이스 링크 (Base link)
    base_link = "https://www.bluer.co.kr/api/v1/restaurants?page=0"
    collected_data = list()

    response = requests.get(base_link)
    json_contents = response.json()

    for h in trange(json_contents['page']['totalPages']):
        needed_url = base_link + f"?page={h}"
        # 필요한 태그만 가져오기 (getting necessary tags from API)
        for i in range(len(json_contents)) :
            # 지정된 링크에서 json 형태로 내용 가져오기 (Getting contents as json format from link)

            response = requests.get(needed_url)
            json_contents = response.json()['_embedded']['restaurants']

            #필요한 데이터 변수
            needed_data = {
                'createdDate' :                 int(str(datetime.utcfromtimestamp(json_contents[0]['createdDate'] / 1000).year) + '0' + str(datetime.utcfromtimestamp(json_contents[0]['createdDate'] / 1000).month) + '0' +  str(datetime.utcfromtimestamp(json_contents[0]['createdDate'] / 1000).day)),
                'id':                           json_contents[i]['id'],
                'nameKR' :                      json_contents[i]['headerInfo']['nameKR'],
                'nameEN':                       json_contents[i]['headerInfo']['nameEN'],
                'nickname':                     json_contents[i]['headerInfo']['nickname'],
                'year':                         json_contents[i]['headerInfo']['year'],
                'bookYear':                     json_contents[i]['headerInfo']['bookYear'],
                'ribbonType':                   json_contents[i]['headerInfo']['ribbonType'],
                'chefName':                     json_contents[i]['defaultInfo']['chefName'],
                'website':                      json_contents[i]['defaultInfo']['website'],
                'websiteInstagram':             json_contents[i]['defaultInfo']['websiteInstagram'],
                'websiteFacebook':              json_contents[i]['defaultInfo']['websiteFacebook'],
                'phone':                        json_contents[i]['defaultInfo']['phone'],
                'openHours':                    json_contents[i]['defaultInfo']['openHours'],
                'closeHours':                   json_contents[i]['defaultInfo']['closeHours'],
                'openHoursWeekend':             json_contents[i]['defaultInfo']['openHoursWeekend'],
                'closeHoursWeekend':            json_contents[i]['defaultInfo']['closeHoursWeekend'],
                'dayOff':                       json_contents[i]['defaultInfo']['dayOff'],
                'storeType':                    json_contents[i]['statusInfo']['storeType'],
                'parking':                      json_contents[i]['statusInfo']['parking'],
                'creditCard':                   json_contents[i]['statusInfo']['creditCard'],
                'visit':                        json_contents[i]['statusInfo']['visit'],
                'menu':                         json_contents[i]['statusInfo']['menu'],
                'priceRange':                   json_contents[i]['statusInfo']['priceRange'],
                'openDate':                     json_contents[i]['statusInfo']['openDate'],
                'businessHours':                json_contents[i]['statusInfo']['businessHours'],
                'openEra':                      json_contents[i]['statusInfo']['openEra'],
                'newOpenDate':                  json_contents[i]['statusInfo']['newOpenDate'],
                'jibunAddr':                    json_contents[i]['juso']['jibunAddr'],
                'engAddr':                      json_contents[i]['juso']['engAddr'],
                'zipNo':                        json_contents[i]['juso']['zipNo'],
                'admCd':                        json_contents[i]['juso']['admCd'],
                'latitude':                     json_contents[i]['gps']['latitude'],
                'longitude':                    json_contents[i]['gps']['longitude'],
                'review':                       json_contents[i]['review']['review'],
                'readerAppraisal':              json_contents[i]['review']['readerAppraisal'],
                'readerReview':                 json_contents[i]['review']['readerReview'],
                'businessReview':               json_contents[i]['review']['businessReview'],
                'editorReview':                 json_contents[i]['review']['editorReview'],
                'reviewerRecommend':            json_contents[i]['etcInfo']['reviewerRecommend'],
                'history':                      json_contents[i]['etcInfo']['history'],
                'mainMemo':                     json_contents[i]['etcInfo']['mainMemo'],
                'status':                       json_contents[i]['status'],
                'bookStatus':                   json_contents[i]['bookStatus'],
                'firstImageurl':                "https://www.bluer.co.kr"+json_contents[i]['firstImage']['url'],
                'firstImagecreatedDate':        int(str(datetime.utcfromtimestamp(json_contents[i]['firstImage']['createdDate'] / 1000).year) + '0' + str(datetime.utcfromtimestamp(json_contents[i]['firstImage']['createdDate'] / 1000).month) + '0' +  str(datetime.utcfromtimestamp(json_contents[i]['firstImage']['createdDate'] / 1000).day)),
                'brandBranches':                json_contents[i]['brandBranches'],
                'foodTypes' :                   json_contents[i]['foodTypes'],
                'selflink':                     json_contents[i]['_links']['self']['href'],
                'restaurantlink':               json_contents[i]['_links']['restaurant']['href'],
                'reportslink':                  json_contents[i]['_links']['reports']['href'],
                'parentRestaurantlink':         json_contents[i]['_links']['parentRestaurant']['href'],
                'foodTypeCategorieslink':       json_contents[i]['_links']['foodTypeCategories']['href'],
                'childrenRestaurantslink':      json_contents[i]['_links']['childrenRestaurants']['href'],
                'relativeWriterlink':           json_contents[i]['_links']['relativeWriter']['href'],
                'restaurantFeatureslink':       json_contents[i]['_links']['restaurantFeatures']['href'],
                'relativeBusinessOrderlink':    json_contents[i]['_links']['relativeBusinessOrder']['href'],
                'evaluateslink':                json_contents[i]['_links']['evaluates']['href'],

            }

            collected_data.append(needed_data)

            a = 1

    # 데이터프레임으로 만들기 (Making jsonified contents as dataframe)
    blueribbon_dataframe = pd.DataFrame(collected_data)
    # 첫 이미지 주소에 head를 붙여서 url화
    blueribbon_dataframe['firstImageurl'] = blueribbon_dataframe['firstImageurl'].map('https://www.bluer.co.kr{}'.format,
                          na_action = 'ignore')
    
    # csv 파일로 저장
    blueribbon_dataframe.to_csv("./result.csv", encoding="utf-8-sig")

    return blueribbon_dataframe

# 출력
blueribbon_df_result = blueribbon_crawling()

print(blueribbon_df_result)
