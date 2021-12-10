#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: swaathi
"""
import requests
import json
import collections_dapps as cdapps
from pyspark.sql import SparkSession, functions, types
import sys
import keys as op
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+


def get_nfts(slug_name, offset):
    """
    get_nfts - retrieve nfts from Opensea API

    :param slug_name: name of the slug to retrieve from
    :param offset: position of data in API
    :return: describe what it returns
    """
    headers = {'X-API-KEY ':  op.API_KEY}
    url = f'https://api.opensea.io/api/v1/assets?order_by=sale_count&order_direction=desc&offset={offset}&limit=28&collection={slug_name}'
    response = requests.request('GET', url, headers=headers)

    if response.status_code != 200:
        if response.status_code == 404:
            # No data found for particular slug
            return None
        else:
            raise Exception('API Hit Failed', response)
    return response


def main():
    slug_names_list = cdapps.collection_slug_names
    response_list = []

    # call api for every slug name on the list
    for slug_name in slug_names_list:
        i = 0
        while(i < 150):
            response = get_nfts(slug_name, i)
            data = response.json()
            if(data['assets'] and len(data['assets']) > 0):
                response_list.append(data['assets'])
                json_rdd = sc.parallelize(data['assets'])
                json_rdd.map(json.dumps).saveAsTextFile(slug_name+str(i))
            i = i+28


if __name__ == '__main__':
    spark = SparkSession.builder.appName('Get NFTs').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()
