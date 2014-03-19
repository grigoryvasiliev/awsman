#!/bin/sh
export AWS_CLOUDWATCH_HOME=/home/charlie/cloudwatch/CloudWatch-1.0.13.4
export JAVA_HOME=/usr/lib/jvm/default-java
 
# Get the timestamp from 5 hours ago, to avoid getting > 1440 metrics (which errors).
# also, remove the +0000 from the timestamp, because the cloudwatch cli tries to enforce
# ISO 8601, but doesn't understand it.
DATE=$(date --iso-8601=hours -d "5 hours ago" |sed s/\+.*//)
 
#echo $COST
 
SERVICES='AmazonS3 ElasticMapReduce AmazonRDS AmazonDynamoDB AWSDataTransfer AmazonEC2 AWSQueueService'
 
for service in $SERVICES; do
 
COST=$(/home/charlie/cloudwatch/CloudWatch-1.0.13.4/bin/mon-get-stats EstimatedCharges --aws-credential-file ~/.ec2_credentials --namespace "AWS/Billing" --statistics Sum --dimensions "ServiceName=${service},Currency=USD" --start-time $DATE |tail -1 |awk '{print $3}')
 
if [ -z $COST ]; then
 echo "failed to retrieve $service metric from CloudWatch.."
 else
 echo "stats.prod.ops.billing.ec2_${service} $COST `date +%s`" |nc graphite.example.com 2023
 fi
 
done
 
# one more time, for the sum:
COST=$(/home/charlie/cloudwatch/CloudWatch-1.0.13.4/bin/mon-get-stats EstimatedCharges --aws-credential-file ~/.ec2_credentials --namespace "AWS/Billing" --statistics Sum --dimensions "Currency=USD" --start-time $DATE |tail -1 |awk '{print $3}')
 
if [ -z $COST ]; then
 echo "failed to retrieve EstimatedCharges metric from CloudWatch.."
 exit 1
else
 echo "stats.prod.ops.billing.ec2_total_estimated $COST `date +%s`" |nc graphite.example.com 2023
fi