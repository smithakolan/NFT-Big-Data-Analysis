import boto3
import json
import aws_key as aws_keys
from decimal import Decimal

local_db_url = 'http://localhost:8000'
aws_db_url = 'https://dynamodb.us-west-2.amazonaws.com'
dynamodb = boto3.resource(
    'dynamodb', aws_access_key_id=aws_keys.ACCESS_ID,
    aws_secret_access_key=aws_keys.ACCESS_KEY, region_name='us-west-2', endpoint_url=aws_db_url)


def create_nft_table():

    table = dynamodb.create_table(
        TableName='NFTs',
        KeySchema=[
            {
                'AttributeName': 'slug',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'token_id',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'token_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'slug',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


def insert_into_table(nfts):
    table = dynamodb.Table('NFTs')
    for nft in nfts:
        slug = nft['slug']
        token_id = nft['token_id']
        print("Adding NFT:", slug, token_id)
        table.put_item(Item=nft)


if __name__ == '__main__':
    # Create Table
    nft_table = create_nft_table()
    print("Table status:", nft_table.table_status)

    # read json file
    with open("nfts.json") as json_file:
        movie_list = json.load(json_file, parse_float=Decimal)

    # insert into table
    insert_into_table(movie_list)
