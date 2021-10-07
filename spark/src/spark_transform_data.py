import os
import sys
import logging

from common import get_spark_session, write_postgres, read_postgres, extract_bitcoin_fact

# spark session
spark = get_spark_session("Raw Data")
# Set log4j
spark.sparkContext.setLogLevel("ERROR")
log4jLogger = spark._jvm.org.apache.log4j
logger = log4jLogger.LogManager.getLogger("LOGGER")
logger.setLevel(log4jLogger.Level.INFO)


def create_bitcoin_facts(pg_host, process_date=None, **kwargs):

    logger.info(f"bitcoin process for {process_date} is started")

    if process_date:
        cond = f"""where ref_date BETWEEN ('{process_date}'::date - '6 days'::INTERVAL) 
        AND '{process_date}'::date"""
    else:
        cond = ""
    sdf = read_postgres(spark, pg_host, "admin", "admin",
                        "bitcoin", "main_data", cond)
    sdf = extract_bitcoin_fact(sdf)
    if process_date:
        sdf = sdf.filter(sdf.ref_date == process_date)

    sdf.printSchema()
    sdf.orderBy("ref_date", ascending=True).show(3)

    write_postgres(sdf, pg_host, "admin", "admin",
                   "bitcoin", "fact_data", 1, "append")

    spark.stop()

    return "Done"


if __name__ == "__main__":

    if len(sys.argv) <= 2:
        pg_host = str(sys.argv[1])
        process_date = None
    else:
        pg_host = str(sys.argv[1])
        process_date = str(sys.argv[2])

    create_bitcoin_facts(pg_host, process_date)
