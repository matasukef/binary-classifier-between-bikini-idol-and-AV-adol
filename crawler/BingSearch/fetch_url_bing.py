import http.client
import requests
import base64
import json
import os
import csv
import time

import settings
import cmd_options

#bing search api url
BASE_URL = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search'

#set api key
API_KEY = settings.BING_SEARCH_API_KEY

#wait time to sent next request
TIME_OUT = 1


class downloadImgs():
    
    def __init__(self, querry, count=50, offset=0, mkt='ja-JP', safeSearch='Off'):
        self.headers = {
            'Ocp-Apim-Subscription-Key': API_KEY
            }
        self.params = {
                'q': querry,
                'count': count,
                'offset': offset,
                'mkt': mkt,
                'safeSearch': safeSearch,
                }
        self.list = []

        self.querry = querry
        self.start = offset

    def _createList(self):
        r = requests.get(BASE_URL, params=self.params, headers=self.headers).json()
        self.params['offset'] += self.params['count']
        for i in range(0, self.params['count']):
            name = r['value'][i]['name']
            url = r['value'][i]['contentUrl']
            print(name, url)
            self.list.append([name, url])
    
    def createLists(self, iteration=1):
        for i in range(0, iteration):
            self._createList()
            self.params['offset'] += self.params['count']
            time.sleep(TIME_OUT)
            print(self.list)

    def saveList(self, saveFile='download_list.csv'):
        with open(saveFile, 'a') as f:
            writer = csv.writer(f, lineterminator='/n')
            #for i in range(0, len(self.list)):
            #    writer.writerow(self.list[i])
            writer.writerows(self.list)

if __name__ == '__main__':
    args = cmd_options.get_arguments()
    querry = args.search_word
    count = args.count
    offset = args.offset
    mkt = args.mkt
    safeSearch = args.safeSearch
    saveFile = args.saveFile
    iterate = args.iterate

    bing = downloadImgs(querry, count, offset, mkt, safeSearch)
    bing.createLists(iterate)
    bing.saveList(saveFile)
