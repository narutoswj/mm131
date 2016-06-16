# -*- coding: utf-8 -*-
import pyquery
import pymongo
import datetime
import os
import sys
import urllib
import threading
from time import ctime,sleep


def download_20_pages(skip):
    # Connect MongoDB Server
    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    # Connect Database
    db = client.beauty
    # Use collection
    collection = db['mm131']
    docs = collection.find({"images_downloaded":None}).limit(20).skip(skip)
    for doc in docs:
        # print doc
        local_folder = doc["local_folder"]
        title = doc["title"]
        total_page = doc["total_page"]
        first_page = doc["first_page"]
        #print first_page
        #print total_page
        page_path = first_page.__str__().replace('1.jpg', '')
        #print page_path
        number = 1
        while int(number) <= int(total_page):
            url = page_path + number.__str__() + '.jpg'
            print(url)
            data = urllib.urlopen(url).read()
            path = local_folder + '/' + title + '_' + number.__str__() + '.jpg'
            f = file(path,"wb")
            f.write(data)
            f.flush()
            f.close()
            number = number + 1
        collection.update({"_id":doc["_id"]},{"$set":{"images_downloaded":1}})

# Connect MongoDB Server
client = pymongo.MongoClient(host="127.0.0.1", port=27017)
# Connect Database
db = client.beauty
# Use collection
collection = db['mm131']
count = collection.find({"images_downloaded":None}).count()

while count > 0:
    threads = []
    t1 = threading.Thread(target=download_20_pages,args=(0,))
    threads.append(t1)
    #t2 = threading.Thread(target=download_20_pages,args=(20,))
    #threads.append(t2)
    #t3 = threading.Thread(target=download_20_pages,args=(40,))
    #threads.append(t3)
    #t4 = threading.Thread(target=download_20_pages,args=(60,))
    #threads.append(t4)

    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    count = collection.find({"images_downloaded":None}).count()

