# NFT-Big-Data-Analysis

### Basic Setup

The local machine (Linux) requires JAVA, Hadoop and Spark to be installed and configured.

Add environment variables if not have been configured:

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_HOME=/home/{user}/spark-3.1.2-bin-hadoop3.2/
export PYSPARK_PYTHON=python3
```

Start the local ssh :

```bash
sudo service ssh start
```

Start NameNode daemon and DataNode daemon:

```bash
hadoop/hadoop-3.3.1/sbin/start-dfs.sh
```

Clone the project directory:

https://github.com/smithakolan/NFT-Big-Data-Analysis.git


## ETL 

#### Extraction of Collection Stats

Command to run file: ETL\collect_stats.py

```bash
time ${SPARK_HOME}/bin/spark-submit ETL\collect_stats.py
```

The program produces HDFS folder called DAppStats

<br /> <br />
#### Extraction of NFTs

Command to run file: ETL\getNFTs.py

```bash
time ${SPARK_HOME}/bin/spark-submit ETL\getNFTs.py
```

The program produces a HDFS folder called rawnftdata. The file from this folder is acquired and converted into a json file called stats.json


<br /><br />
#### Transformation of NFTs

Command to run file: ETL\transformNFT.py

```bash
time ${SPARK_HOME}/bin/spark-submit ETL\transformNFT.py
```

The program produces a file called nfts.json

<br /><br />
#### An AWS account has to be created and a Administrator User account should be created before proceeding to the next step. After creation, the AWS ACCESS_ID and ACCESS_KEY should be added to the ETL folder of the project as a python file.

#### Loading of Stats to Database

Command to run file: ETL\loadStats.py

```bash
time ${SPARK_HOME}/bin/spark-submit ETL\loadStats.py
```

After the Stats table creation and insertion:
![stat_table](https://user-images.githubusercontent.com/63001832/145521790-4b5d14cb-60a9-46b1-913a-72d7326d5516.jpg)

<br /><br />

#### Loading of NFTs to Database

Command to run file: ETL\loadNFT.py

```bash
time ${SPARK_HOME}/bin/spark-submit ETL\loadNFT.py
```


After the NFTs table creation and insertion:
![nft_table](https://user-images.githubusercontent.com/63001832/145521852-75b87dec-35af-454c-944b-f1115a5ed742.jpg)

<br /><br />
## Data Analysis

#### Dapp Trends

Command to run file: Data_Analysis\analyse_stats.py

```bash
time ${SPARK_HOME}/bin/spark-submit Data_Analysis\analyse_stats.py
```

The program produces two files as output which can be found on HDFS. <br />
dapp_volume.json - Contains 1 Day, 7 Days and 30 Days Volume of NFT sold for the top 10 NFTs with respect to each of the Dapps. <br />
dapp_optimality.json - Contains optimality score of Dapps 
<br /><br />
#### Rarity

1. Run [generate_nft_per_dapp_csv.py](https://github.com/smithakolan/NFT-Big-Data-Analysis/blob/main/Data_Analysis/generate_nft_per_dapp_csv.py) file in order to generate a csv file which will contain dapp names along with the number of NFTs in each dapp.
csv file generated: [nftperdapp.csv](https://github.com/smithakolan/NFT-Big-Data-Analysis/blob/main/Data_Analysis/nftperdapp.csv)
columns=['slug', 'NFTcount']

2. Run [RarityCalculator.py](https://github.com/smithakolan/NFT-Big-Data-Analysis/blob/main/Data_Analysis/RarityCalculator.py) which will calculate the rarity of each NFT. The output for this will be a csv file for each dapp in the nftperdapp.csv.

columns=['id','token_id', 'nft_name', 'image_url', 'slug', 'last_sale_total_price', 'rarity']

#### Top 5 NFTs Per Dapp

1. When runinng [RarityCalculator.py](https://github.com/smithakolan/NFT-Big-Data-Analysis/blob/main/Data_Analysis/RarityCalculator.py) an additional csv called [top5NFTs.csv](https://github.com/smithakolan/NFT-Big-Data-Analysis/blob/main/Datasets_for_visualization/top5NFTs.csv) is generated. It contains the top 5 NFTs per dapp.
<br /><br />
columns=['slug', 'NFTcount', 'image_1', nft1_id', 'image_2', nft2_id', 'image_3', nft3_id', 'image_4', nft4_id', 'image_5', nft5_id']

#### Price prediction of NFTs using Machine Learning

1. Run [NFTPriceRegression.py](https://github.com/smithakolan/NFT-Big-Data-Analysis/blob/main/Data_Analysis/NFTPriceRegression.py) which uses linear regression to generate the predicted price of each NFT within each dapp. This step makes use of the output generated from calculating the rarity in order to run.

<br /><br />
#### Correlation between the price of the NFT and the number of sales 

```bash
python3 Data_Analysis\nft_correlation_analysis.py
```
The program produces a file called nft_corr.csv
<br /><br />
## Visualization and Results
Tableau visualization workbooks are located in Visualization_Tableau_Workbooks. Tableau Desktop/ Public/Reader must be downloaded to view the workbooks. Otherwise, see the full visualization here: https://public.tableau.com/app/profile/ha.do1817

