import os
import sys
import logging

from pyspark import StorageLevel
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def get_spark_session(appname):

    spark = (SparkSession.builder
             .appName(appname)
             .config("spark.network.timeout", "10000s")
             .getOrCreate())
    return spark

def raw_data_transforms(sdf):
    sdf = sdf.withColumn("ref_date", sdf["Date"].cast("date"))
    sdf = sdf.withColumnRenamed("Market Cap", "market_cap")
        
    sdf = sdf.select([F.col(x).alias(x.lower()) for x in sdf.columns])
    sdf = sdf.select(["ref_date", "open", "high", "low", "close", "volume", "market_cap"])
    
    return sdf

def extract_bitcoin_fact(sdf):
    # usd to euro
    sdf = sdf.withColumnRenamed("close", "close_usd")
    sdf = sdf.withColumn("close_euro", F.col("close_usd") * 1.1600)
    
    # extract euro_rolling_average for each date
    days = lambda i: i * 86400
    sdf = sdf.withColumn('ref_timestamp', sdf.ref_date.cast('timestamp'))
    w = (Window.orderBy(F.col("ref_timestamp").cast('long')).rangeBetween(-days(6), 0))
    sdf = sdf.withColumn('euro_rolling_average', F.avg("close_euro").over(w))
    sdf = sdf.select(["ref_date", "close_usd", "close_euro", "euro_rolling_average"])
    
    return sdf

def write_postgres(sdf, host, user, password, database, table, partition=16, mode="append"):    
    pg_properties = {
        "driver": "org.postgresql.Driver",
        "user": user,
        "password": password}
    pg_url = "jdbc:postgresql://{}:5432/{}".format(host, database)
    
    sdf = sdf.persist(StorageLevel.DISK_ONLY)
    
    (sdf.repartition(partition).sortWithinPartitions("ref_date")
    #  .sort("ref_date")
    #  .orderBy(["ref_date"], ascending=[1])
     .write.jdbc(url=pg_url, table=table, mode=mode, properties=pg_properties))
    
    sdf.unpersist()

def read_postgres(spark, host, user, password, database, table, cond=""):
    return (spark.read \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://{0}/{1}?user={2}&password={3}".format(host, database, user, password)) \
            .option("driver", "org.postgresql.Driver") \
            .option("query", f"SELECT * FROM {table} {cond} ORDER BY ref_date") \
            .load())