import re
import json
import boto3
import requests
from time import time

class AWSCredentials:
    BUCKET_NAME = 'behance-alesia'
    S3_KEY = 'bot-data/'
    aws_access_key_id='AKIA6GBMF5BKU7MLRFNW' 
    aws_secret_access_key='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'
    

class LoadSubscribers(AWSCredentials):    
    JSON_DATA = {
    'query': '\n        query GetUserFollowers($username: String, $first: Int, $after: String) {\n          user(username: $username) {\n            followers(first: $first, after: $after) {\n              pageInfo {\n                endCursor\n                hasNextPage\n              }\n              nodes {\n                user {\n                  ...UserProfileRowFields\n                }\n              }\n            }\n          }\n        }\n        \n  fragment UserProfileRowFields on User {\n    username\n    displayName\n    creativeFields {\n      name\n      id\n      url\n    }\n    creatorPro {\n      initialSubscriptionDate\n      isActive\n    }\n    firstName\n    id\n    city\n    images {\n      size_50 {\n        url\n      }\n      size_100 {\n        url\n      }\n      size_115 {\n        url\n      }\n      size_230 {\n        url\n      }\n      size_138 {\n        url\n      }\n      size_276 {\n        url\n      }\n    }\n    url\n    location\n    locationUrl\n    isProfileOwner\n    isFollowing\n    hasPremiumAccess\n    bannerImageUrl\n    creativeFields {\n      name\n      id\n    }\n    stats {\n      appreciations\n      views\n    }\n    profileProjects {\n      nodes {\n        url\n        covers {\n          size_202 {\n            url\n          }\n          size_404 {\n            url\n          }\n          size_808 {\n            url\n          }\n        }\n      }\n    }\n  }\n\n      ',
    'variables': {
        'first': 1000,
        'username': 'beAlesia',
        },
    }
    
    HEADERS = {
        'authority': 'www.behance.net',
        'accept': '*/*',
        'accept-language': 'pl',
        'content-type': 'application/json',
        'origin': 'https://www.behance.net',
        'referer': 'https://www.behance.net/beAlesia/followers?background=/beAlesia',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-bcp': 'c14ed3b7-d4cc-4fcb-b45e-706162b5c685',
        'x-newrelic-id': 'VgUFVldbGwsFU1BRDwUBVw==',
        'x-requested-with': 'XMLHttpRequest',
        }
    
    COOKIES = {
        'gk_suid': '86456742',
        'gki': 'test_cross_auth: false, list_keyboard_nav: false, hire_filter_ab_test: false,',
        'originalReferrer': '',
        'ilo0': 'true',
        'bcp': 'c14ed3b7-d4cc-4fcb-b45e-706162b5c685',
        '_cs_mk_aa': '0.7878223133990943_1709908254779',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Mar+08+2024+15%3A30%3A54+GMT%2B0100+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202210.1.0&isIABGlobal=false&hosts=&consentId=5c3cbc40-5f60-4835-b5cb-9c988a5525ce&interactionCount=0&landingPath=https%3A%2F%2Fwww.behance.net%2FbeAlesia&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0',
        'kndctr_9E1005A551ED61CA0A490D45_AdobeOrg_cluster': 'irl1',
        'kndctr_9E1005A551ED61CA0A490D45_AdobeOrg_identity': 'CiYwODM3MDQyMzE0MDE2NjcwMDY4MTc3NTExMTg4MDE2ODk4ODc2NFITCMrC5fPhMRABGAEqBElSTDEwAPABysLl8-Ex',
        'AMCV_9E1005A551ED61CA0A490D45%40AdobeOrg': 'MCMID|08370423140166700681775111880168988764',
        'gpv': 'behance.net:profile:default',
        }
    def __init__(self, cookies=None, headers=None):
        self.s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)
        self.cookies = cookies or self.COOKIES
        self.headers = headers or self.HEADERS
    
    def load(self):
        return requests.post('https://www.behance.net/v3/graphql', cookies=self.cookies, headers=self.headers, json=self.JSON_DATA).json()
    
    def load_to_bucket(self):
        data =json.dumps( self.load())
        if int(['http_code']) != 200:
            raise Exception("Bad response.")
        self.s3.put_object(Bucket=self.BUCKET_NAME, Key=f"{self.S3_KEY}{int(time()*1000000)}.json", Body=data)
        return data
    

class CompareData(AWSCredentials):
    ID_PATTERN = re.compile(r'\/(\d+)\.')
    def __init__(self):
        self.s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)
    
    def bucket_file_names(self):
        response = self.s3.list_objects_v2(Bucket=self.BUCKET_NAME, Prefix=self.S3_KEY)
        file_names = {int(re.findall(self.ID_PATTERN, obj['Key'])[0]) : obj['Key'] 
                      for obj in response['Contents'] if len(re.findall(self.ID_PATTERN, obj['Key'])) !=0}
        return file_names
    
    def load_data(self):        
        file_names = self.bucket_file_names()
        return {key: {'file_name': file_names[key],'data':self.load_by_name(file_names[key])}    for key in file_names.keys() }
            
    def load_by_name(self, file_name):
        return json.loads(self.s3.get_object(Bucket=self.BUCKET_NAME, Key=file_name)['Body'].read().decode('utf-8'))
    
    def compare(self):
        data = self.load_data()
        min_date = min(data.keys())
        max_date = max(data.keys())
        older_sub =  self.create_user(data[max_date]['data']['data']['user']['followers']['nodes'])
        newest_sub = self.create_user(data[min_date]['data']['data']['user']['followers']['nodes'])
        unsubscriber = set(older_sub.keys()) - set(newest_sub.keys())
        self.s3.delete_object(Bucket=self.BUCKET_NAME, Key=data[min_date]['file_name'])
        return {user: older_sub[user] for user in unsubscriber}
        
    def create_user(self, users):
        return {user['user']['username']:user['user']['url']  for user in users}
    

class TelegramBot:
    BOT_TOKEN = '6616302606:AAHC4AlxSdkUcleWDNTeRpQjb9XBlgW0Rio'
    CHAT_ID = '334212836'

    def send_message(self, message):
        url = 'https://api.telegram.org/bot' +self.BOT_TOKEN + '/sendMessage?chat_id=' + self.CHAT_ID + \
                '&parse_mode=HTML&text=' + message
        return requests.get(url).text