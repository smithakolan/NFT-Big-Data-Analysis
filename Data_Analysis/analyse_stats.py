import json
from pyspark.sql import SparkSession, functions, types
from pyspark.sql.functions import round, when, lit
import sys
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+


def main():
    dapp_text = sc.textFile('DAppStats')
    dapp_json = dapp_text.map(lambda line: json.loads(line))
    dapp_df = dapp_json.toDF()
    
    dapp_df.coalesce(1).write.mode("overwrite").json("dapp_stats.json")

    
    dapp_stats_schema = types.StructType([
    types.StructField('one_day_volume', types.FloatType()),
    types.StructField('one_day_change', types.FloatType()),
    types.StructField('one_day_sales', types.FloatType()),
    types.StructField('one_day_average_price', types.FloatType()),
    types.StructField('seven_day_volume', types.FloatType()),
    types.StructField('seven_day_change', types.FloatType()),
    types.StructField('seven_day_sales', types.FloatType()),
    types.StructField('seven_day_average_price', types.FloatType()),
    types.StructField('thirty_day_volume', types.FloatType()),
    types.StructField('thirty_day_change', types.FloatType()),
    types.StructField('thirty_day_sales', types.FloatType()),
    types.StructField('thirty_day_average_price', types.FloatType()),
    types.StructField('total_volume', types.FloatType()),
    types.StructField('total_sales', types.FloatType()),
    types.StructField('total_supply', types.FloatType()),
    types.StructField('count', types.FloatType()),
    types.StructField('num_owners', types.FloatType()),
    types.StructField('average_price', types.FloatType()),
    types.StructField('num_reports', types.FloatType()),
    types.StructField('market_cap', types.FloatType()),
    types.StructField('floor_price', types.FloatType()),
    types.StructField('slug', types.StringType()),
    ])
    
    
    dapp_df_from_S3 = spark.read.json("dapp_stats.json", schema=dapp_stats_schema)
    dapp_df_from_S3.createOrReplaceTempView("dapp_df_from_S3")
    
    
    dapp_volume_view = spark.sql("select slug as dapp_name,round(d.one_day_volume,4) as one_day_volume,round(d.seven_day_volume,4) as seven_day_volume,round(d.thirty_day_volume,4) as thirty_day_volume FROM  dapp_df_from_S3 d order by total_sales desc")
    dapp_volume_view.createOrReplaceTempView("dapp_volume_view")
    
    #Trend 1 : Storing Dapp daily,weekly and monthly volumes
    dapp_top10_volume_view = spark.sql("select *  from dapp_volume_view limit 10")
    dapp_top10_volume_view.createOrReplaceTempView("dapp_top10_volume_view")
    dapp_top10_volume_view.coalesce(1).write.mode("overwrite").json("dapp_volume.json")
    
    dapp_ratio_view = spark.sql("select slug as dapp_name,round(d.market_cap,4) as market_cap,round(d.total_volume,4) as total_volume, round(d.market_cap,4)/round(d.total_volume,4) as ratio FROM  dapp_df_from_S3 d order by total_sales desc")
    dapp_market_cap_to_volume_ratio = dapp_ratio_view.withColumn("ratio", when((dapp_ratio_view.ratio < 1), lit("Sub-Optimal")).otherwise(lit("Optimal")))
    dapp_market_cap_to_volume_ratio.createOrReplaceTempView("dapp_market_cap_to_volume_ratio")
    
    #Trend 2 :Determinign Dapp Optimality and Storing
    dapp_optimality = spark.sql("select dapp_name,ratio from dapp_market_cap_to_volume_ratio")
    dapp_optimality.createOrReplaceTempView("dapp_optimality")
    dapp_optimality.coalesce(1).write.mode("overwrite").json("dapp_optimality.json")
    


if __name__ == '__main__':
    spark = SparkSession.builder.appName("Transform DApps").getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()