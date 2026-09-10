'''
# Install Java 11
!apt-get -qq update
!apt-get -qq install -y openjdk-11-jdk-headless > /dev/null

# Remove conflicting Spark packages that may already exist in Colab
!pip -q uninstall -y dataproc-spark-connect pyspark delta-spark

# Install PySpark 3.5.6 and Delta Lake 3.2.0
!pip -q install pyspark==3.5.6 delta-spark==3.2.0

import os

# Configure Java
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
os.environ["PATH"] += ":/usr/lib/jvm/java-11-openjdk-amd64/bin"

# Remove conflicting Spark environment variables
os.environ.pop("SPARK_HOME", None)
os.environ.pop("PYSPARK_SUBMIT_ARGS", None)
'''

# Creates a "spark" instance, i.e an object for us to be able to use the Spark functions.
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

# We use the datalake format "delta lake" for our datalake.
def _create_delta_spark():
  builder = SparkSession.builder.appName("DeltaLakeApp") \
  .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
  .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
  .config("spark.jars.packages","io.delta:delta-core_2.12:2.0.0")
  return configure_spark_with_delta_pip(builder).getOrCreate()

spark = _create_delta_spark()


# Here we read data from the "california_housing_train.csv" dataset.
df = spark.read.options(inferSchema=True, header=True).csv("/content/sample_data/california_housing_train.csv")
df.printSchema()


# To work with the data using a Delta Table, we first need to create our Spark database:
spark.sql("create database id2221")
spark.sql("use id2221")

# Next we can write to the (currently empty) database, but we write data in the "delta lake" format.
# write csv data as deltap
df.write.mode("overwrite").format("delta").save("id2221/df_delta")
# If I understand it correctly, the data from "california_housing_train.csv" is now stored not as a regular "table", but as a file system/directory from the path "id2221".
# So there is now a folder called "id2221", in which there is a folder called "df_delta" which in turn contains all the data in "delta table" format along with the delta log.

# Then we can read from the delta lake database table.
#read delta table
df_delta = spark.read.format("delta").load("id2221/df_delta")
df_delta.show(1) # Shows the 1st row in the delta table.

# We can also add a new column in the delta lake table:
# create a new column in housing_df_delta dataframe with the name "median_house_value_new" and its values as "median_house_value"*1.1
df_delta = df_delta.withColumn("median_house_value_new", df_delta["median_house_value"] * 1.1)
df_delta.show(1)
# But we need to commit this new version of the delta table, which we do with:
df_delta.write\
.option("mergeSchema", "true")\
.mode("append").format("delta").save("id2221/df_delta")