#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 17:42:58 2021

@author: smithakolan
"""

import json
import pandas as pd
import collections_dapps as cdapps

with open('nfts.json') as f:
  data = json.load(f)

nftPerDapp = pd.read_csv('nftperdapp.csv') 


nftCount = 0
dappCount = 0


#Calculating rarity for each NFT

for dapp in nftPerDapp.iterrows():
    
    dfObj = pd.DataFrame(columns=['id','token_id', 'nft_name', 'image_url', 'slug', 'last_sale_total_price', 'rarity'])
    #print(nftCount)
    #print(dapp[1][1]+nftCount)
    for i in range(nftCount, dapp[1][1]+nftCount):
        
        numberOfTraits = len(data[i]["traits"])
        
        rarity = 0
        for j in range(0,numberOfTraits):
            
            traitCount = data[i]["traits"][j]['trait_count']
            if(traitCount != 0):
                rarity = rarity + 10000/(data[i]["traits"][j]['trait_count'])
        
        
        #print(i)    
        #rarity = rarity/numberOfTraits
        dfObj = dfObj.append({'id':data[i]["id"],'token_id':data[i]["token_id"], 'nft_name':data[i]["nft_name"], 'image_url':data[i]["image_url"], 'slug':data[i]["slug"], 'last_sale_total_price':data[i]["last_sale_total_price"], 'rarity':rarity}, ignore_index=True)
        data[i]["rarity"] = rarity
    
        
    filename = dapp[1][0] + '.csv'
    dfObj.to_csv(filename, index=False) 
    
    # Get top 5 rarity values
    dfObj.sort_values(by=['rarity'])
    nftPerDapp.loc[dappCount, 'image_1'] = dfObj['image_url'][0]
    nftPerDapp.loc[dappCount, 'nft1_id'] = dfObj['id'][0]
    nftPerDapp.loc[dappCount, 'image_2'] = dfObj['image_url'][1]
    nftPerDapp.loc[dappCount, 'nft2_id'] = dfObj['id'][1]
    nftPerDapp.loc[dappCount, 'image_3'] = dfObj['image_url'][2]
    nftPerDapp.loc[dappCount, 'nft3_id'] = dfObj['id'][2]
    nftPerDapp.loc[dappCount, 'image_4'] = dfObj['image_url'][3]
    nftPerDapp.loc[dappCount, 'nft4_id'] = dfObj['id'][3]
    nftPerDapp.loc[dappCount, 'image_5'] = dfObj['image_url'][4]
    nftPerDapp.loc[dappCount, 'nft5_id'] = dfObj['id'][4]
    dappCount = dappCount + 1
    nftCount = nftCount + dapp[1][1]
    

nftPerDapp.to_csv('top5NFTs.csv', index=False)
#Save data back to JSON
#Create dataframe for each dapp




