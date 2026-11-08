from pyspark import pipelines as dp
from pyspark.sql.functions import *

VOL_LOCATION = spark.conf.get('conv_loc')


@dp.table(
    name = "converions"
)
def converions():
    df=(
        spark.readStream
        .format("cloudfiles")
        .option("cloudFiles.format","json")
        .option('header','true')
        .option("multiLine","true")
        .load(VOL_LOCATION)
    )
    return df.drop('_rescued_data')