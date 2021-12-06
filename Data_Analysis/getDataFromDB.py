import boto3
import aws_key as aws_keys

local_db_url = 'http://localhost:8000'
aws_db_url = 'https://dynamodb.us-west-2.amazonaws.com'
dynamodb = boto3.resource(
    'dynamodb', aws_access_key_id=aws_keys.ACCESS_ID,
    aws_secret_access_key=aws_keys.ACCESS_KEY, region_name='us-west-2', endpoint_url=aws_db_url)

table_name = 'NFTs'


def scan_dynamodb(table_name):
    table = dynamodb.Table(table_name)
    nfts = []
    scan_kwargs = {}
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        nft_data = response.get('Items', [])
        nfts.append(nft_data)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

    nfts_list = []
    for iterative_list in nfts:
        for record in iterative_list:
            nfts_list.append(record)
    return nfts_list


if __name__ == '__main__':
    nft_records = scan_dynamodb(table_name)
