#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 13:02:36 2021

@author: smithakolan
"""


import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split


dapps = pd.read_csv('nftperdapp.csv')
print(dapps['slug'][0])

for i in range(0,len(dapps)):
    dataset = pd.read_csv('Rarity-Price-Data/'+dapps['slug'][i]+'.csv')
    
    sns.pairplot(dataset[['rarity','last_sale_total_price']], diag_kind='kde')
    
    dataset.describe().transpose()

    x = dataset['rarity'].values.reshape(-1, 1)
    print(x.shape)
    y = dataset['last_sale_total_price'].values.reshape(-1, 1)
    print(y.shape)
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
    model = LinearRegression()
    model.fit(x_train, y_train)
    print(model.coef_)
    
    predictions = model.predict(x_test)
    
    plt.scatter(y_test, predictions)
    
    plt.hist(y_test - predictions)
    
    metrics.mean_absolute_error(y_test, predictions)
    
    totalPred = model.predict(x)
    
    dataset['predicted_price'] = totalPred
    
    #display(dataset)
    
    dataset.to_csv('Rarity-Price-Data/'+dapps['slug'][i]+'.csv', index=False)
    

