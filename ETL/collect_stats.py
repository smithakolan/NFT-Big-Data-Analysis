#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Geethika
"""
import requests
import time
import json
import collection_dapps as cdapps
from pyspark.sql import SparkSession, functions, types
import sys
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+


def main():
    dapp_slug_names = cdapps.collection_slug_names

    response_list = []
    headers = {"Accept": "application/json"}

    params = (
        ('limit', '1'),
    )

    for slug in dapp_slug_names:
        slugStatsUrl = "https://api.opensea.io/api/v1/collection/" + slug + "/stats"

        response = requests.request(
            "GET", slugStatsUrl, headers=headers, params=params)

        if response.status_code == 404:
            print('Dapp Stats Not found for {0} '.format(slug))
        else:
            data = response.json()
            data['stats']['slug'] = slug
            response_list.append(data['stats'])

    json_rdd = sc.parallelize(response_list)
    json_rdd.map(json.dumps).saveAsTextFile("DAppStats")


if __name__ == '__main__':
    spark = SparkSession.builder.appName('Get Dapp stats').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()
