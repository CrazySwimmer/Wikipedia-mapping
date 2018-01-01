#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#==============================================================================
#Load modules
from bs4 import BeautifulSoup
import requests

#==============================================================================
#Variables
url = 'https://en.wikipedia.org/wiki/Metallica' #Full article URL
links = [] #Initialize an empty list of links
soup = BeautifulSoup(requests.get(url).content, 'lxml') #Build the BeautifulSoup item
    
#==============================================================================
#Get links from article

#Iterate over all links within the content of the wikipedia article
for a in soup.find('div', {'id': 'mw-content-text'}).findAll('a'):
    href = a.get('href')
    if href is None: #Some links have an empty href, skip them
        continue
    elif href[:6] == '/wiki/': #This is an internal link to an article
        #Links with ':' are special links such as Files or BookSources
        #Disambiguation links also cause problems
        if not (':' in href in href or href[6:] in links or '(disambiguation)' in href):
            if not 'List_of_' in href: #Comment out to keep Lists of () articles
                links.append(href[6:]) #Only append the name of the article

print(links)
                
