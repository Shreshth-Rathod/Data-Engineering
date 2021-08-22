import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "rds_database", table_name = "ecommerce_database_uk_ecommerce_data", transformation_ctx = "DataSource0"]
## @return: DataSource0
## @inputs: []
DataSource0 = glueContext.create_dynamic_frame.from_catalog(database = "rds_database", table_name = "ecommerce_database_uk_ecommerce_data", transformation_ctx = "DataSource0")
## @type: ApplyMapping
## @args: [mappings = [("unitprice", "decimal", "unitprice", "decimal"), ("description", "string", "description", "string"), ("unique_id", "int", "unique_id", "int"), ("quantity", "int", "quantity", "int"), ("country", "string", "country", "string"), ("invoiceno", "string", "invoiceno", "string"), ("invoicedate", "timestamp", "invoicedate", "string"), ("customerid", "int", "customerid", "int"), ("stockcode", "string", "stockcode", "string")], transformation_ctx = "Transform0"]
## @return: Transform0
## @inputs: [frame = DataSource0]
Transform0 = ApplyMapping.apply(frame = DataSource0, mappings = [("unitprice", "decimal", "unitprice", "decimal"), ("description", "string", "description", "string"), ("unique_id", "int", "unique_id", "int"), ("quantity", "int", "quantity", "int"), ("country", "string", "country", "string"), ("invoiceno", "string", "invoiceno", "string"), ("invoicedate", "timestamp", "invoicedate", "string"), ("customerid", "int", "customerid", "int"), ("stockcode", "string", "stockcode", "string")], transformation_ctx = "Transform0")
## @type: DataSink
## @args: [connection_type = "s3", format = "csv", connection_options = {"path": "s3://uk-ecommerce-data-output/Output/", "partitionKeys": []}, transformation_ctx = "DataSink0"]
## @return: DataSink0
## @inputs: [frame = Transform0]
DataSink0 = glueContext.write_dynamic_frame.from_options(frame = Transform0, connection_type = "s3", format = "csv", connection_options = {"path": "s3://uk-ecommerce-data-output/Output/", "partitionKeys": []}, transformation_ctx = "DataSink0")
job.commit()