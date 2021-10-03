import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

# Extra import to get the current_date function
from pyspark.sql.functions import *

args = getResolvedOptions(sys.argv, ['TempDir','JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

DataSource0 = glueContext.create_dynamic_frame.from_catalog(database = "s3_database", table_name = "output", transformation_ctx = "DataSource0")

# The 2 extra lines below convert between the 
# original Glue Dataframe to a Spark Dataframe, add the new column
# then convert back again to a Glue Dataframe
# 
df=DataSource0.toDF().withColumn("invoicedate",to_timestamp(col("invoicedate"))).withColumn("year", date_format(col("invoicedate"), "Y")).withColumn("month", date_format(col("invoicedate"), "MMMMM")).withColumn("week_of_month", date_format(col("invoicedate"), "w")).withColumn("day", date_format(col("invoicedate"), "EEEE")).withColumn('quarter',quarter(col("invoicedate")))

# withColumn("quarter", date_format(col("invoicedate"), "Q"))

DataSource0 = DynamicFrame.fromDF(df, glueContext, "DataSource0") 

Apply_Mapping = ApplyMapping.apply(frame = DataSource0, 
	mappings = [("unique_id", "long", "unique_id", "long"), 
				("invoiceno", "string", "invoiceno", "string"), 
				("stockcode", "string", "stockcode", "string"), 
				("description", "string", "description", "string"), 
				("quantity", "long", "quantity", "long"), 
				("invoicedate", "string", "invoicedate", "timestamp"),
				("year", "long", "year", "long"),
				("month", "string", "month", "string"),
				("week_of_month", "long", "week_of_month", "long"),
				("day", "string", "day", "string"),
				("quarter", "long", "quarter", "long"),
				("unitprice", "double", "unitprice", "double"), 
				("customerid", "long", "customerid", "long"), 
				("country", "string", "country", "string")], 
				transformation_ctx = "Apply_Mapping")
resolvechoice = ResolveChoice.apply(frame = Apply_Mapping, choice = "make_cols", transformation_ctx = "resolvechoice") 
DataSink0 = glueContext.write_dynamic_frame.from_catalog(frame = resolvechoice, database = "redshift_database", redshift_tmp_dir = args["TempDir"], table_name = "dw_ecommerce_public_uk_ecommerce", transformation_ctx = "DataSink0", additional_options = {"aws_iam_role":"arn:aws:iam::221276599729:role/S3_Glue_Redshift_Cluster_Authorisation"})

job.commit()
 
