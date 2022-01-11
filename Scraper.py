# -*- coding: utf-8 -*-
# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import os

# The website categories
category = ['politics', 'Panorama', 'sport', 'business','technology', 'science', 'Culture', 'budget', 'inland', 'international']
# Create a dictionary for articles
my_dict={}
title=[]
summary = []
date = []
category_test = []

# Number of pages that will be scraped for every categotry
MAX_PAGES = 101
# Indexing the articles
article_num = 1

for cat in category:
    for page in tqdm(range(1,MAX_PAGES),  desc='{:>15}'.format(cat)): 
        url = "https://www.spiegel.de/{}/p{}".format(cat, page)
        #url = "https://www.bbc.com/".format(cat, page)
        #url = "https://edition.cnn.com/".format(cat, page)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        articles = soup.select('article') # select all articles
        for a in articles:
            # Select the articles' titles from attribute 'aria-label'
            title[article_num]={"title":a.get('aria-label')}.append(title)
            
            # Select the articles' summary from class 'leading-loose'
            y = summary[article_num].update({"summary":"".join([x.text.strip()
                                                            for x in a.select('.leading-loose')])
                                        })
            summary.append(y)
            # Select the articles' date from 'footer'
            z = date[article_num].update({"date":"".join([x.text.strip()
                                                            for x in a.select('footer')])
                                        })
            date.append(z)
            
            # Add the category
            a = category_test[article_num].update({"categoty":cat})
            
            category.append(a)
            
            # index' Increment  
            article_num +=1

dateset = pd.DataFrame({'Title':title,'Summary':summary,'Date':date,'Category':category_test})

dateset.to_csv('Datatry.csv', index=False, encoding = "ISO-8859-1")

if 'data' not in os.listdir():          
    # Create a folder !mkdir data
    #Convert my_dict to DataFrame
    df = pd.DataFrame.from_dict(data=my_dict, orient='index')
    # Drop duplicate articles
    df2 = df.drop_duplicates(subset='title', keep='first')
    # Save as csv as utf-16 due to spicial German charachters
    df2.to_csv('Dataset.csv', index=False, encoding = "ISO-8859-1")
