# Data-Engineering with E-Commerce Dataset

## INSERT AN IMAGE FOR THE SERVICES USED OVER HERE

# Introduction & Goals

- In this project, I have applied Data Modeling with MySQL and build an ETL pipeline using Python. A startup wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. Currently, they are collecting data in json format and the analytics team is particularly interested in understanding what songs users are listening to.
- In this project, I have applied various data engineering principles from ingestion of data to visualise the data for business goals on an E-commerce dataset from Kaggle.
- The tools I have used are AWS services: S3, Lambda function, MySQL RDS database, Glue with PySpark, Athena, Redshift, VPC, IAM, CloudWatch.
- Apart from AWS services, other tools used were as follow: MySQL Workbench, DataGrip, Tableau.

# Contents

- [The Data Set](#the-data-set)
- [Used Tools](#used-tools)
  - [Setup](#setup)
  - [Connect](#connect)
  - [Processing](#processing)
  - [Storage](#storage)
  - [Visualization](#visualization)
  - [Visualizations](#visualizations)
- [Conclusion](#conclusion)
- [Follow Me On](#follow-me-on)


# The Data Set

- The E-commerce dataset consists of approximately 540K rows, which had features like InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, and Country.
- The dataset had columns with a clear descripton of products and the Invoice Date which can be used to visualise the data on timely basis e.g. weekly sales, monthly sales, and quaterly sales.
- My goal with this dataset was to find which product had the most sales according to the season cycle and what was the revenue generated on monthly and quaterly basis?

# Used Tools

- The tools used in this project were as follow:
  - S3: Worked as a Data Source.
  - Lambda function: It was configured to be triggered whenever there was a PUT call in S3.
  - MySQL RDS database: Lambda funcion would load the data from S3 to MySQL RDS Database.
  - MySQL Workbench: This was used for creating the database and table on RDS Instance.
  - Glue with PySpark: This tool was used as ETL with PySpark for distributed processing of data.
  - Athena: It was used for checking the data availability in S3 (staging table).
  - Redshift: This was the final stage where the data was stored after transformation in accordance with business requirements.
  - DataGrip: It was connected with Redshift to create the database and table in the cluster.
  - VPC: Security purpose to keep the services bound to a network.
  - IAM: Roles were created to give access to the services and call them on behalf of the the user.
  - CloudWatch: To keep a track on all the services with the help of logs stored in the cloudwatch dashboard. 
  - Tableau: It was connected to Redshift for visualising the historic data trends.

## Setup

### 1. AWS S3 bucket
- Create two Buckets
    - Data that is stored from local machine: uk-ecommerce-data-Input 
    - Data that is stored from RDS using Glue: uk-ecommerce-data-Output 
    - Select the region : US East(Ohio) us-east-2.
    - Unblock all public access.
    - Disable Bucket Versioning, Server Side Encryption and Object lock.

DO NOT FORGET TO STOP THE INSTANCE OF RDS DB!!!

### 2. AWS RDS
- Create a Database.
- Select Easy Create.
- Select MySQL Server
- Select Free tier (If you don’t want to get charged and the size of the data is small - project purpose)
    - db.t2.micro
    - 1 vCPUs
    - 1 GiB RAM
    - 20 GiB
    - 0.020 USD/hour
- Name the DB instance identifier: data-engineering-aws
- Create a master username: ******
- Create a password : ******
- Click on create Database and wait for few minutes to launch the instance.
- Click on the DB instance and click the Modify Button on top Left in the AWS RDS dashboard.
    - Check the DB Engine Version : MySQL 5.7.30
    - Directly scroll down to Connectivity
        - Enable the public access
        - Database Port is ******
    - Go into the Additional Configuration
        - Backup Retention Period: 0 Days
- Apply these changes immediately.

### 3. MySQL Workbench (If you don’t have SQL Workbench, install it with MySQL and Java 8+)
- Click on the + sign to add a connection.
- A new window will open
    - Give the connection a name: AWS_Data_Engineering
    - Go to RDS dashboard, click the identifier and go to “Connectivity & Security”, copy the “Endpoint” and paste it into MySQL Workbench Hostname: ******
    - Port: ******
    - Username: ****** (the master username of the RDS instance)
    - Click the test button and enter the password: ******
    - This will connect the workbench with AWS RDS instance.
    - If you have problems connecting with the database, go to RDS dashboard -> security groups -> Inbound rules -> add new rule -> type: All traffic & source: Anywhere.
- Create a database named as ECommerce_Database
    - Create tables according to the ER-Diagram of your data

### 4. AWS IAM Role creation
- Click on IAM from AWS Console
- Select Roles from left column
- Click the Create role button
    - Select the type of trusted entity: AWS services
    - Choose a use case: Lambda
    - Click on Next : Permissions
    - Search for as shown below:
        - CloudWatchFullaccess
        - S3Fullaccess
        - RDSFullaccess
    - Click on Next: Tags
    - Click on Next: Review
        - Enter a role name: ******
    - Click the Create role button and the role is created.

- Again click the Create role button
    - Select the type of trusted entity: AWS services
    - Choose a use case: Glue
    - Click on Next : Permissions
    - Search for as shown below:
        - CloudWatchFullaccess
        - S3Fullaccess
        - RDSFullaccess
        - GlueServiceRole
        - AmazonRedshiftFullAccess
    - Click on Next: Tags
    - Click on Next: Review
        - Enter a role name: ******
    - Click the Create role button and the role is created.


WHEN EXECUTING THE LAMBDA FUNCTION, MAKE SURE YOU FIRST DEPLOY IT THEN EXECUTE THE FUNCTION.

### 5. AWS Lambda Function
- Go to Lambda
- Repeat these steps for all the lambda functions.
    - Click on Create function
        - Select Author from Scratch.
        - Give function a name (same as bucket names just append _Reader at the end)
        - Runtime environment: Python 3.8
        - Go in the Permission section 
            - Execution Role: Use an existing role (the role that was created before in IAM section)
    - Go to one of the lambda functions and Add Trigger.
        - Select S3
        - Select Bucket name that matches with the lambda function name (it is not necessary to have the same names, it is for my convenience)
        - Event type : All object create events
        - Leave the prefix section as blank if you don’t have any subfolders in the bucket
        - Enter .csv in the suffix section if the files processed are csv files.

- Refer this for Lambda Layer which is used for more functionalities to be added to the lambda function, reason behind creating the layer is, Mysql connector is not supported by lambda function, so external package is required to be loaded in the lambda function and that is done with the help of lambda layers.

https://www.youtube.com/watch?v=5llBuFMegO0&list=PLcw5TTdQlsECxTYzc0o5AK-t-reDBzI3k&index=5

### 6. AWS Lambda Layer
- Refer the above two screenshots
- After completing the procedure from the 1st screenshot, zip the python folder that is inside the build folder, DO NOT ZIP THE BUILD FOLDER!
- Now go to the lambda function and click on the layers from the left column in the dashboard.
    - Click on Create Layer
    - Give a name to the layer: mysql-lambda-layer
    - Select Upload a .zip file
    - Select the Runtime: Python 3.8
    - Click the create button at the end and the layer will be created.
- Repeat these steps for all the lambda functions.
    - Click on one of the Lambda functions from the dashboard.
    - Click on Layers.
    - It will direct to the end of the page and find a button Add a layer.
        - Select Custom Layers
        - Choose layer:  mysql-lambda-layer
        - Choose Version: 1
- Reason behind creating the layer is, Mysql connector is not supported by lambda function, so external package is required to be loaded in the lambda function and that is done with the help of lambda layers.


- AWS GLUE Tutorial:

https://www.youtube.com/watch?v=UUoQAe_NzaA&list=PL7bE4nSzLSWfYAc3q1vEYFi145Mt_DLcF&index=3

https://dev.to/amree/exporting-data-from-rds-to-s3-using-aws-glue-mai


### 7. AWS Glue
- Go into the Glue console.
- On your left column, you can see Databases, click on it and press the Add Database button.
    - Name the database according to your needs and add a description for your convenience.
    - My database name is rds_database.
    - My database name is s3_database.
    - My database name is redshift_database.

#### RDS STEPS 
    - Now goto Connections, click on Add Connection button.
        - Assign a Connection Name.
        - My connection name is rds_mysql_connection.
        - Choose Amazon RDS in Connection Type dropdown menu.
        - Choose MySQL as Database Engine dropdown menu.
        - Click on Next.
        - Choose the instance, mine had to be data-engineering-aws because it is present in RDS instance under MySQL DB Engine.
        - Assign Database name to be same as the database name used in your MySQL workbench.
            - Mine is ECommerce_Database.
        - Give the credentials same as given for setting up the RDS Instance.
            - Username: ******
            - Password: ******
        - Test the connection with IAM role created above: ******
    - Now goto Crawler, click on Add Crawler.
        - Give a crawler name: rds_crawler
        - Crawler source type: Data Stores
        - Ignore the Repeat crawls of S3 data stores as our data does not come from S3
        - Click Next.
        - Choose a data store : JDBC
        - Select the connection from the dropdown menu : the connection created in the Connection section : rds_mysql_connection
        - Include Path: ECommerce_Database/Uk_Ecommerce_Data (this is the only table that is to be crawled)
        - Choose the IAM Role for the process : ******
        - Frequency: Run On Demand
        - Choose the database where we want to store the crawled data: rds_database
        - Run the crawler to determine the metadata. It may take few minutes to run.

#### S3 STEPS
    - Now goto Connections, click on Add Connection button.
        - Assign a Connection Name.
        - My connection name is s3_connection.
        - Connection Type: Network
        - Click Next.
        - Choose VPC same as RDS
        - Choose one of the subnets that are present in RDS
        - Click on Finish
        - Test the connection with IAM role created above: ******
    - Now goto Crawler, click on Add Crawler.
        - Give a crawler name: s3_crawler
        - Crawler source type: Data Stores
        - Click Next
        - Choose Data Store: S3
        - Choose the Connection Name: s3_connection
        - Tick on Specify Path in my account
        - Add path: s3://uk-ecommerce-data-output
        - Select the IAM Role: Rds_Glue_S3_Role
        - Frequency: Run On Demand
        - Choose Database: s3_database
        - Do not run this crawler until the ETL part is completed from exporting the data RDS -> S3.

#### REDSHIFT CLUSTER STEPS
    - Now goto Connections, click on Add Connection button.
        - Assign a Connection Name.
        - My connection name is redshift_connection.
        - Connection Type: Amazon Redshift
        - Click Next.
        - Select the cluster you made in Redshift: data-engineering-aws-redshift
        - Database: dw_ecommerce
        - Username: ******
        - Password: ******
        - Click on Finish
        - Test the connection with IAM role created above: ******
    - Now goto Crawler, click on Add Crawler.
        - Give a crawler name: redshift_crawler
        - Crawler source type: Data Stores
        - Click Next
        - Choose Data Store: JDBC
        - Choose the Connection Name: redshift_connection
        - Tick on Specify Path in my account
        - Add path: dw_ecommerce/public/%
        - Select the IAM Role: ******
        - Frequency: Run On Demand
        - Choose Database: redshift_database

- Now goto ETL section of AWS Glue
    - Source: MySQL
    - Target: S3
    - Click on Create.
    - Click on MySQL Node
        - Choose the appropriate database and the table for MySQL.
    - Click on S3 Node
        - Format: CSV
        - S3 Target location: s3://uk-ecommerce-data-output/Output
    - Goto Job Details
        - Name the job: rds_to_s3_data_transfer
        - Select the IAM Role
        - Type: Spark
        - Glue Version: Glue 2.0 - Supports Spark 2.4, Scala 2, Python 3
        - Language: Python
        - Worker type: G1.X
        - No of workers: 2
        - Job Bookmark: Enable
        - Number of retries: 3
        - Job timeout: 2880 minute
        - Script Path: s3://uk-ecommerce-data-output/scripts/
        - Spark UI logs path: s3://uk-ecommerce-data-output/sparkHistoryLogs/
        - Maximum Concurrency: 1
        - Temporary path: s3://uk-ecommerce-data-output/temporary/
        - Connections: add s3_connection the access S3
        - Click on Save button

### 8. AWS Redshift
- Go into the redshift cluster and click on create cluster button.
- Assign the cluster instance name: data-engineering-aws-redshift
- Select free trial.
- Configurations are as follow:
    - dc2.large | 1 node
    - High performance with fixed local SSD storage
    - Compute: 2 vCPU (gen 2) / node x 1 = 2 vCPU
    - Storage Capacity: 160 GB x 1 nodes = 160 GB
- Admin User Name: ******
- Password: ******
- The cluster is created.

### 9. DataGrip
- Download the required drivers for amazon redshift.
- Name: My_Redshift_Connection
- Host: ******
- Port: ******
- User: ******
- Password: ******
- Database: dw_ecommerce
- URL: ******

## Connect

- Lambda function: It was configured to be triggered whenever there was an upload from the local machine to S3. The trigger functionality was to load the dataset from S3 to RDS MySQL Database.

## Processing

- Glue with PySpark: This tool was used as ETL with PySpark for distributed processing of data. Glue was initiated to do two batch jobs as follow:
  - First job consisted of extracting data from RDS and directly loading it to S3 (Staging table).
  - Second job consisted of extracting the data from S3 and performing transformation on the data according to the requirements and finally loading it to the Redshift warehouse.

## Storage

- MySQL RDS database: Lambda funcion would load the data from S3 to MySQL RDS Database. Whenever the data is extracted form the data source, it gets loaded into a database. According to the business requirements, the data gets extracted from the database to perform transformations on it.
- MySQL Workbench: This was used for creating the database and table on RDS Instance.
- S3: This was used as a staging table because the data can't be directly transformed. It has to be stored at some storage system where it will be present for preprocessing
- Athena: It was used for checking the data availability in S3 (staging table).
- Redshift: This was the final stage where the data was stored after transformation in accordance with business requirements.
- DataGrip: It was connected with Redshift to create the database and table in the cluster.

## Visualization

- Tableau: It was connected to Redshift for visualising the historic data trends.

## Visualizations

- Coming soon.

# Conclusion

- The project turned out really well and I had learnt a lot from this project.
- From connecting various services on cloud with each other as well as to local machines was fascinating for me. 
- The major things I learnt in the journey of data engineering was to get hands on experience on AWS services and trying not to exceed the limit of free tier options. Sometimes, it was challenging but had a great fun in learning all the principles of data engineering.
- The biggest challenges for me were as follow:
  - Tuning Lambda function with optimum RAM for faster execution.
  - RDS had it's own issues while loading the data from S3. I had to deal with VPC for the access and had to tune the internal parameters to increase the buffer and log size of the instance. This changes allowed me to load the data into the instance easily
  - Another challenge was to split the date into days (words), months(words), and year in the transformation part of glue using PySpark (S3 -> Redshift)

# Follow Me On

http://linkedin.com/in/shreshthrathod
