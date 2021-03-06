'''S dot Pratap at liverpool dot ac dot uk | Surya Pratap'''
'''This code is to extract reviews and related details of a single hotel from tripadvisor.com, all you need to change is link @line22.
Also, make sure to change url from "https://" upto ".html"
NOTE: There is "{}" available inside the url, please make sure to write your URL same as this way. Example: Reviews-or{}-'''

'''importing libraries'''
from bs4 import BeautifulSoup
import os
from requests_html import HTMLSession
from lxml import html
import requests
import time
import pandas as pd
global reviewcount
import re
names = []
title = []
review = []
date = []
rating = []
# List the first page of the reviews (ends with "#REVIEWS") (you can change this website as per your requirement but make sure in the link there is "or{}").
WebSites = ("https://www.tripadvisor.co.uk/Hotel_Review-g186338-d188961-Reviews-or{}-Hotel_41-London_England.html#REVIEWS".format(i) for i in range(0, 250, 5))
# looping through each site until it hits a break
for theurl in WebSites:
    time.sleep(1)
    session = HTMLSession()
    response = session.get(theurl)
    page = requests.get(theurl)
    tree = html.fromstring(page.content)
    soup = BeautifulSoup(response.content, "html.parser")
    totalreview = tree.xpath("//*[@id='ABOUT_TAB']/div/div[1]/div[1]/a/span[2]/text()")
    total_rating = tree.xpath("//*[@id='ABOUT_TAB']/div/div[1]/div[1]/span/text()")
    hotel_name = tree.xpath("//*[@id='HEADING']/text()")
    for bubble_rating in soup.findAll(attrs={"class": "location-review-review-list-parts-RatingLine__bubbles--GcJvM"}):     #to scrap bubble rating using its classname
        Rating = bubble_rating.select_one('span.ui_bubble_rating')['class']
        Rating = Rating[1].split('_')[-1]
        rating.append(Rating[0])

    for x in range(3, 8):
        ii = 2
        Reviewer = tree.xpath("//*[@id='component_15']/div/div[3]/div[%d]/div[1]/div/div[2]/span/a/text()"%x)   #reviewer name
        Reviewer = ''.join(Reviewer)
        Review = tree.xpath("//*[@id='component_15']/div/div[3]/div[%d]/div[%d]/div[3]/div[1]/div[1]/q/span/text()"%(x, ii))
        Review = ''.join(Review)
        ReviewTitle = tree.xpath("//*[@id='component_15']/div/div[3]/div[%d]/div[%d]/div[2]/a/span/span/text()"%(x,ii))
        ReviewTitle = ''.join(ReviewTitle)
        RatingDate = tree.xpath("//*[@id='component_15']/div/div[3]/div[%d]/div[1]/div/div[2]/span/text()"%x)
        RatingDate = ''.join(RatingDate)
        if Review == []:        #if the list is empty
            ii+=1
            full_review = tree.xpath("//*[@id='component_15']/div/div[3]/div[%d]/div[%d]/div[3]/div[1]/div[1]/q/span/text()" %(x, ii))
        ii = 2
        if ReviewTitle == []:
            ii+=1
            ReviewTitle = tree.xpath("//*[@id='component_15']/div/div[3]/div[%d]/div[%d]/div[2]/a/span/span/text()" % (x, ii))
        names.append(Reviewer)
        review.append(Review)
        title.append(ReviewTitle)
        date.append(RatingDate.replace("wrote a review", ""))

    # print("Hotel Name = " + ''.join(hotel_name),"\nTotal Reviews = " + ''.join(totalreview),"\nOverall Rating = " + ''.join(total_rating))
df = pd.DataFrame({"Reviewer":names, "Review Date":date, "Review Rating":rating, "Review Title":title, "Review":review})    #list to csv columns
df.dropna(how="all", inplace=True)      #remove blank rows
df.to_csv('output.csv',index=False, encoding="utf-8")      #save data to csv



