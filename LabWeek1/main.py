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

# Creates a "spark" instance.
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

def _create_delta_spark():
  builder = SparkSession.builder.appName("DeltaLakeApp") \
  .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
  .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
  .config("spark.jars.packages","io.delta:delta-core_2.12:2.0.0")
  return configure_spark_with_delta_pip(builder).getOrCreate()

spark = _create_delta_spark()