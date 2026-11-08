from pyspark import pipelines as dp
from pyspark.sql.functions import *

VOL_LOCATION = spark.conf.get('ad_per_loc')

SCHEMA = """ 
    campaign_id STRING,
    date DATE,
    impressions LONG,
    clicks LONG,
    spend DOUBLE,
    device STRING
"""

@dp.table(
    name = "ad_performance"
)
def ad_performance():
    df=(
        spark.readStream
        .format("cloudfiles")
        .option("cloudFiles.format","csv")
        .option('header','true')
        .schema(SCHEMA)
        .load(VOL_LOCATION)
    )
    return df.drop('_rescued_data')