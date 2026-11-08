from pyspark import pipelines as dp
from pyspark.sql.functions import *


@dp.table(
    name="02_silver.fact_conversions"
)
def fact_conversions():
    df = (
        spark.read.table('marketing_analytics_project.`01_bronze`.converions')
        .withColumn('date', to_date(col('date')))
        .withColumn('conversion', from_json(
            col('conversion'), "ARRAY<STRUCT<customer_id: STRING, conversion_type: STRING, revenue_usd: DOUBLE>>"
        ))
        .withColumn('conversion', explode(col('conversion')))
        .withColumn('revenue_usd', col('conversion.revenue_usd'))
        .withColumn('conversion_type', col('conversion.conversion_type'))
        .withColumn('customer_id', col('conversion.customer_id'))
        .drop('conversion')
        .select(
            "campaign_id",
            "customer_id",
            "date",
            "conversion_type",
            "revenue_usd"
        )
        .dropDuplicates(['campaign_id', 'customer_id', 'date', 'conversion_type'])
    )
    
    df_transpose = (  
        df 
        .withColumn('add_to_cart', when(col('conversion_type') == 'Add to Cart', 1).otherwise(0))
        .withColumn('Wishlist', when(col('conversion_type') == 'Wishlist', 1).otherwise(0))
        .withColumn('Purchase', when(col('conversion_type') == 'Buy', 1).otherwise(0))
        .groupBy(["campaign_id", "date", "customer_id"])
        .agg(
            sum("revenue_usd").alias('revenue_usd'),
            sum('add_to_cart').alias('add_to_cart'),
            sum('Wishlist').alias('Wishlist'),
            sum('Purchase').alias('purchase')
        )
        .orderBy('date')
    )
    
    return df_transpose