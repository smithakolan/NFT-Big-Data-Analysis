import json
from pyspark.sql import SparkSession, functions, types
import sys
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+


def get_cleaned_nft(nft_object):
    if(nft_object['last_sale'] != None):
        return True
    else:
        return False


def get_selective_fields(nft_object):
    if(nft_object != None):
        total_price = nft_object['last_sale']['total_price']
        decimal = nft_object['last_sale']['payment_token']['decimals']
        total_price = float(total_price) / float(pow(10, decimal))
        new_nft_object = {
            'id': nft_object['id'],
            'token_id': nft_object['token_id'],
            'num_sales': nft_object['num_sales'],
            'nft_name': nft_object['name'],
            'contract_address': nft_object['asset_contract']['address'],
            'contract_created_date': nft_object['asset_contract']['created_date'],
            'collection_name': nft_object['asset_contract']['name'],
            'nft_version': nft_object['asset_contract']['nft_version'],
            'collection_symbol': nft_object['asset_contract']['symbol'],
            'slug': nft_object['collection']['slug'],
            'traits': nft_object['traits'],
            'last_sale_payment_token_symbol': nft_object['last_sale']['payment_token']['symbol'],
            'last_sale_event_type': nft_object['last_sale']['event_type'],
            'last_sale_event_timestamp': nft_object['last_sale']['event_timestamp'],
            'last_sale_auction_type': nft_object['last_sale']['auction_type'],
            'last_sale_total_price': total_price

        }
        return new_nft_object


def main():
    nft_text = sc.textFile("rawnftdata/*")
    nft_json = nft_text.map(lambda line: json.loads(line))

    # cleaning NFT - remove NFTs that do not have last_sale value
    cleaned_NFT = nft_json.filter(get_cleaned_nft)
    # print(cleaned_NFT.take(1))

    # selecting required json fields for use cases
    nft_selected = cleaned_NFT.map(get_selective_fields)
    # print(nft_selected.take(1))

    jsonRDD = nft_selected.map(json.dumps)

    # reduce to one big string with one json on each line
    json_string = jsonRDD.reduce(lambda x, y: x + "\n" + y)

    # write your string to a file
    with open("/home/swaathi/bigdataproject/nfts.json", "wb") as f:
        f.write(json_string.encode("utf-8"))


if __name__ == '__main__':
    spark = SparkSession.builder.appName("Transform NFTs").getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()
