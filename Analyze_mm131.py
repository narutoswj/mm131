# -*- coding: utf-8 -*-
import pyquery
import pymongo
import datetime
import os
import sys

def Get_Max_page(url):
    from pyquery import PyQuery as pq
    #print url
    page = pq(url=url)
    #print page.html()
    #print page('.page')
    lastpage = page('.page')(':last').attr('href').__str__()
    #print lastpage
    replace1 = lastpage[lastpage.index('_')+1:lastpage.__len__()]
    replace2 = replace1[replace1.index('_') + 1:replace1.__len__()]
    maxpage = replace2.replace('.html','')
    return int(maxpage)

def Get_Page_Reference(url):
    from pyquery import PyQuery as pq
    page = pq(url=url)
    lastpage = page('.page')(':last').attr('href').__str__()
    replace1 = lastpage[lastpage.index('_') + 1:lastpage.__len__()]
    return int(replace1[0:1])

def Get_Subpage_List(root_folder,url):
    # Connect MongoDB Server
    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    # Connect Database
    db = client.beauty

    # Use collection
    collection = db['mm131']
    collection_log = db['mm131_log']
    try:
        root = root_folder
        root_url = url
        from pyquery import PyQuery as pq
        print "Starting Analysis: " + root_url
        page = pq(url=root_url) #Process url html
        container = page('.list-left')  #Get container
        slice = container('dd') #Get sub-container slice
        #print slice.html()
        for i in slice:
            element = pq(i)
            #print element.html()
            if not (element.has_class('page')): #Check if is NOT the page nav
                element = element('a')
                print element
                name = element.text()   #Get title
                try:
                    print "Starting: " + name
                    folder = root + name    #Make folder path
                    print folder
                    cover_image = element('img').attr('src')    #Small image url
                    print cover_image
                    link_url = element.attr('href')     #Detail page url
                    detail_page = pq(url=link_url)
                    first_image_url = detail_page('.content-pic')('img').attr('src')
                    total_image_count = detail_page('.content-page')('span').html()
                    total_image_count = total_image_count[1:total_image_count.__len__() - 1]
                    if not (os.path.exists(folder)):  # Create folder if not existed
                        os.makedirs(folder)
                except Exception, e:
                    print e
                    collection_log.inset({"Error": link_url })
                print "First image: " + first_image_url
                print "Total page: " + total_image_count
                count = collection.find({"first_page":first_image_url}).count()
                if count < 1:
                    collection.insert({"title":name,"cover_image":cover_image,"total_page":total_image_count,"first_page":first_image_url,"local_folder":folder})
                # print name
                # print cover_image
                # print link_url

        print "Finished Analysis: " + root_url
        print "..............." + count.__str__()
        if count == 0:
            return True
        else:
            return False
    except Exception,e:
        print Exception, ":", e
        collection_log.insert({"URL":url})
        return True

#Parameters#
print "start"
local_folder = 'D:/Image/mm131.com/'
first_page = 'http://www.mm131.com/mingxing/'
first_page_list = ['http://www.mm131.com/xinggan/',
                   'http://www.mm131.com/qingchun/',
                   'http://www.mm131.com/xiaohua/',
                   'http://www.mm131.com/chemo/',
                   'http://www.mm131.com/qipao/']
#maxPageNumber = Get_Max_page(first_page_list[5])
#referenceNumber = Get_Page_Reference(first_page_list[5])
#print referenceNumber
#print maxPageNumber

for page in first_page_list:
    folder = local_folder + page.replace('http://www.mm131.com/','')
    print local_folder
    maxPageNumber = Get_Max_page(page)
    referenceNumber = Get_Page_Reference(page)
    print "Page: " + page
    print "Reference Number: " + referenceNumber.__str__()
    print "Max Page Numer: " + maxPageNumber.__str__()
    load = Get_Subpage_List(folder,page)
    pagenumber = 2
    if load:
        while (pagenumber <= maxPageNumber):
            current_page = page + "list_" + referenceNumber.__str__() + "_" + pagenumber.__str__() + ".html"
            print current_page
            load = Get_Subpage_List(folder, current_page)
            pagenumber = pagenumber + 1
            if load == False:
                pagenumber = maxPageNumber + 1

#Get_Subpage_List('D:/Image/mm131.com/','http://www.mm131.com/xinggan/list_6_6.html')