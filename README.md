# NFT-Big-Data-Analysis

### Basic Setup

The local machine (Linux) requires JAVA, Hadoop and Spark to be installed and configured.

Add environment variables if not have been configured:

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_HOME=/home/swaathi/spark-3.1.2-bin-hadoop3.2/
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

<br /><br /><br />
### An AWS account has to be created and a Administrator User account should be created before proceeding to the next step. After creation, the AWS ACCESS_ID and ACCESS_KEY should be added to the ETL folder of the project as a python file.

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

#### Trend - 1 Geethika
<br /><br />
#### Rarity
<br /><br />

1. run generate_nft_per_dapp_csv.py file in order to generate a csv file which will contain dapp names along with 
the number of NFTs in each dapp.

Header of csv generated: 

2. Run RarityCalculator.py which will calculate the rarity of each NFT. The output for this script will be a csv 
file for each dapp as well as csv which will contains top 5 NFTs per dapp.

4. Run NFTPriceRegression.py which does linear regression on rarity on each NFT in order to generate the predicted price

#### Top 5 NFTs Per Dapp
<br /><br />
#### Price prediction of NFTs using Machine Learning
<br /><br />
#### Correlation between the price of the NFT and the number of sales 

```bash
python3 Data_Analysis\nft_correlation_analysis.py
```
The program produces a file called nft_corr.csv
<br /><br />
## Visualization and Results

-- Ha Do
