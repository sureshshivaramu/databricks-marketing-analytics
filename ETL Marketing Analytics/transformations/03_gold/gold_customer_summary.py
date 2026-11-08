
from pyspark import pipelines as dp
from pyspark.sql.functions import *

@dp.table(
    name= "03_gold.mv_gold_customer_summary"
)
def mv_gold_customer_summary():
    df_conv =(
        spark.read.table('marketing_analytics_project.`02_silver`.fact_conversions')
        .groupBy('customer_id')
        .agg(
            sum('revenue_usd').alias('revenue_usd'),
            sum('add_to_cart').alias('add_to_cart'),
            sum('Wishlist').alias('Wishlist'),
            sum('purchase').alias('purchase'),
            sum(col('add_to_cart') + col('Wishlist') + col('purchase')).alias('total_no_of_conversions')
        )
        .withColumn('revenue_usd', round(col('revenue_usd'), 2))
    )

    df_cust = spark.read.table('marketing_analytics_project.`02_silver`.dim_customer')

    df_join = (
        df_conv
        .join(df_cust, 'customer_id','left')
        .withColumn('customer_tier',expr("CASE WHEN revenue_usd < 100 OR total_no_of_conversions < 10 THEN 'Bronze' WHEN revenue_usd >=500 OR total_no_of_conversions >=15 THEN 'Gold' ELSE 'Silver' END"))
        .select('customer_id','region','customer_tier','revenue_usd','add_to_cart','Wishlist','purchase','total_no_of_conversions')
        .orderBy('customer_id')
    )
    return(df_join)
