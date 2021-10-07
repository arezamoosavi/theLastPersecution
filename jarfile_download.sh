cd spark/jars
echo ${PWD}
wget --no-verbose https://repo1.maven.org/maven2/org/apache/spark/spark-streaming_2.12/3.1.1/spark-streaming_2.12-3.1.1.jar
wget --no-verbose https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10-assembly_2.12/3.1.1/spark-streaming-kafka-0-10-assembly_2.12-3.1.1.jar
wget --no-verbose https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.6.0/kafka-clients-2.6.0.jar
wget --no-verbose https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.9.0/commons-pool2-2.9.0.jar
wget --no-verbose https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.1.1/spark-sql-kafka-0-10_2.12-3.1.1.jar
wget --no-verbose https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.1.1/spark-token-provider-kafka-0-10_2.12-3.1.1.jar
wget --no-verbose https://repo1.maven.org/maven2/org/postgresql/postgresql/42.2.5/postgresql-42.2.5.jar
wget --no-verbose https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.534/aws-java-sdk-1.11.534.jar
wget --no-verbose https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.874/aws-java-sdk-bundle-1.11.874.jar
wget --no-verbose https://repo1.maven.org/maven2/io/delta/delta-core_2.12/1.0.0/delta-core_2.12-1.0.0.jar
wget --no-verbose https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.2.0/hadoop-aws-3.2.0.jar
cd ../..