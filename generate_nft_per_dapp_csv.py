#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 17:42:58 2021

@author: smithakolan
"""

import json
import csv
import pandas as pd
import collections_dapps as cdapps

with open('nfts.json') as f:
  data = json.load(f)
  

slugcountDF = pd.DataFrame(columns=['slug', 'NFTcount'])
slug_names_list = cdapps.collection_slug_names
  
print(data[201]["slug"])  
totalnft = 0
j = 0
for i in range(0,len(slug_names_list)):
    NFTcount = 0
    
    

    while j<len(data) and (data[j]["slug"] == slug_names_list[i]):
        NFTcount = NFTcount +1
        j = j+1
    
    totalnft = totalnft + NFTcount
    slugcountDF.loc[i] = [slug_names_list[i], NFTcount]
     
   
    
print(slugcountDF)  
slugcountDF.to_csv('nftperdapp.csv', index_label=False, )
"""
0-199
200-398
399-598
599-797

"""
   