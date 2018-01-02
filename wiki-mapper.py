#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#==============================================================================
#Load modules
from bs4 import BeautifulSoup
import requests
    
#==============================================================================
#Get links from article
def get_internal_links(article):
    links = [] #Initialize an empty list of links
    url = 'https://en.wikipedia.org/wiki/' + article
    #Build the BeautifulSoup item
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
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
    return links

#==============================================================================
#Crawl list of links

#Variables
article = 'Metallica' #Starting article
links = get_internal_links(article)
maxItems=1000 #Set a limit to the crawling
maxBreadth=1
itemCount = 0 #Initialize the item counter
network = {article:links} #Initialize the output dictionary
scraped = [] #List of fully scraped articles (all internal links have been scraped according to maxBreadth/Depth)

print('Variables declared: OK') #Temporary debug line


#Main program
if maxBreadth > 0:
    links = links[:maxBreadth]
        
#Repeat this step until we reach the maxItems threshold
while itemCount <= maxItems:
    #Iterate over the keys who aren't fully scraped according to maxBreadth
    keys = [k for k in network.keys() if k not in scraped]
    #We have scraped everything allowed by maxBreadth/Depth
    if len(keys)==0:
        break
    #Iterate over nodes that haven't been scraped
    for k in keys:
        print('key :', k) #Temp debug line
        #Iterate over the values (edges / relationships / internal links)
        for v in get_internal_links(k):
            print(k, '-', 'Item', itemCount, ':', v) #Temp debug line
            if v not in network.keys(): #Add them to the keys if not present
                links = get_internal_links(v) #Get the internal links
                if maxBreadth == 0: #Set the max breadth as large as possible
                    maxBreadth = len(links)
                    mB = maxBreadth
                else:
                    mB = maxBreadth
                #Add the edge entry as a node 
                network[v] = links[:mB] #Only assign links up to maxBreadth
                itemCount += 1

                #Exit if we have reached the max item threshold
                if itemCount >= maxItems:
                    break

        scraped.append(k) #The node doesn't have to be scraped again
        if itemCount >= maxItems:
            break