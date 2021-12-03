import json
from pyspark.sql import SparkSession, functions, types
import sys
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+


def main():
    nft_text = sc.textFile('rawnftdata/cryptokitties*')
    nft_json = nft_text.map(lambda line: json.loads(line))
    nft_json.take(5)
    print(nft_json.take(1))


if __name__ == '__main__':
    spark = SparkSession.builder.appName("Transform NFTs").getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()
