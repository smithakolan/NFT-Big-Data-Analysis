import collections_dapps as cdapps
import json
from pyspark.sql import SparkSession, functions, types
import sys
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+


def get_cleaned_nft(nft_object):
    """
    get_cleaned_nft - selects NFTS only with the last_sale value not none
    :param nft_object: single nft 
    :return: true or false
    """
    if(nft_object['last_sale'] != None):
        return True
    else:
        return False


def get_selective_fields(nft_object):
    """
    get_selective_fields - retrieves required fields from a nft object

    :param nft_object: single nft object
    :return: returns a new nft object with only required fields
    """
    if(nft_object != None):
        total_price = nft_object['last_sale']['total_price']
        decimal = nft_object['last_sale']['payment_token']['decimals']
        total_price = float(total_price) / float(pow(10, decimal))
        new_nft_object = {
            'id': nft_object['id'],
            'token_id': nft_object['token_id'],
            'num_sales': nft_object['num_sales'],
            'nft_name': nft_object['name'],
            'image_url': nft_object['image_url'],
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


def store_values(line):
    """
    store_values - selects only value part of <k,v>
    :param line: single nft object as <k=id,v =nft_object> 
    :return: nft object
    """
    k, v = line
    return v


def remove_duplicates(dappName):
    """
    remove_duplicates - removes duplicate nfts
    :param dappName: name of the nft collection 
    :return: nfts that do not have duplicates
    """
    nft_text = sc.textFile("rawnftdata/"+dappName+"*")
    nft_json = nft_text.map(lambda line: json.loads(line))
    nft_key_value = nft_json.map(lambda line: (line['id'], line))
    non_duplicate_nfts = nft_key_value.reduceByKey(lambda x, y: x)
    non_duplicate_nfts = non_duplicate_nfts.map(store_values)
    non_duplicate_nfts = non_duplicate_nfts.take(200)
    return non_duplicate_nfts


def main():
    # retrieve data for every dapp collection and remove duplicates
    complete_nft_list = []
    nfts_list = []
    for dapp in cdapps.collection_slug_names:
        nft_list = remove_duplicates(dapp)
        complete_nft_list.append(nft_list)

    for iterative_list in complete_nft_list:
        for record in iterative_list:
            nfts_list.append(record)

    # convert list to rdd
    nfts_rdd = sc.parallelize(nfts_list)

    # cleaning NFT - remove NFTs that do not have last_sale value
    cleaned_NFT = nfts_rdd.filter(get_cleaned_nft)

    # selecting required json fields for use cases
    nft_selected = cleaned_NFT.map(get_selective_fields)

    jsonRDD = nft_selected.map(json.dumps)
    json_string = jsonRDD.reduce(lambda x, y: x + ",\n" + y)

    # writing to a local file
    with open("/home/swaathi/bigdataproject/nfts.json", "wb") as f:
        f.write(json_string.encode("utf-8"))


if __name__ == '__main__':
    spark = SparkSession.builder.appName("Transform NFTs").getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()
