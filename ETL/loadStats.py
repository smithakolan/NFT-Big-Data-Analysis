#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: swaathi
"""
import boto3
import json
import aws_key as aws_keys
from decimal import Decimal
import time
local_db_url = 'http://localhost:8000'
aws_db_url = 'https://dynamodb.us-west-2.amazonaws.com'
dynamodb = boto3.resource(
    'dynamodb', aws_access_key_id=aws_keys.ACCESS_ID,
    aws_secret_access_key=aws_keys.ACCESS_KEY, region_name='us-west-2', endpoint_url=aws_db_url)


def create_stats_table():
    """
    create_stats_table - creates stats table in Dyanmo DB
    :return: table status
    """
    table = dynamodb.create_table(
        TableName='Stats',
        KeySchema=[
            {
                'AttributeName': 'slug',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'slug',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


def insert_into_table(stats):
    """
    insert_into_table - inserts data into stats table
    :param stats: stats data
    """
    table = dynamodb.Table('Stats')
    for stat in stats:
        table.put_item(Item=stat)


if __name__ == '__main__':
    # Create Table
    stats_table = create_stats_table()

    # to wait for the table to get created
    time.sleep(60)

    # read json file
    with open("stats.json") as json_file:
        stats_list = json.load(json_file, parse_float=Decimal)

    # insert into table
    insert_into_table(stats_list)
