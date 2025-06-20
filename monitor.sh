#!/bin/bash

# Baseball Power Rankings Monitoring Script
# This script provides useful commands to monitor the deployed infrastructure

# Configuration
AWS_REGION="us-east-2"
STACK_NAME="baseball-power-rankings-stack"
CLUSTER_NAME="production-bpr-cluster"
SERVICE_NAME="production-bpr-service"

echo "📊 Baseball Power Rankings - Infrastructure Monitoring"
echo "=================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if AWS CLI is installed
if ! command_exists aws; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials are not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ AWS credentials are valid"
echo ""

# Get stack status
echo "🔍 CloudFormation Stack Status:"
aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $AWS_REGION \
    --query 'Stacks[0].{Status:StackStatus,LastUpdated:LastUpdatedTime}' \
    --output table

echo ""

# Get ECS service status
echo "🐳 ECS Service Status:"
aws ecs describe-services \
    --cluster $CLUSTER_NAME \
    --services $SERVICE_NAME \
    --region $AWS_REGION \
    --query 'services[0].{Status:status,RunningCount:runningCount,DesiredCount:desiredCount,PendingCount:pendingCount}' \
    --output table

echo ""

# Get load balancer URL
echo "🌐 Application URL:"
ALB_DNS=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
    --output text \
    --region $AWS_REGION 2>/dev/null)

if [ ! -z "$ALB_DNS" ]; then
    echo "http://$ALB_DNS"
else
    echo "❌ Could not retrieve load balancer DNS"
fi

echo ""

# Get RDS database status
echo "🗄️ RDS Database Status:"
aws rds describe-db-instances \
    --db-instance-identifier production-baseball-power-rankings-db-728078289631 \
    --region $AWS_REGION \
    --query 'DBInstances[0].{Status:DBInstanceStatus,Engine:Engine,Class:DBInstanceClass,Storage:AllocatedStorage}' \
    --output table

echo ""

# Get recent CloudWatch logs
echo "📝 Recent CloudWatch Logs (last 10 entries):"
LOG_GROUP="/ecs/production-bpr"
aws logs describe-log-streams \
    --log-group-name $LOG_GROUP \
    --region $AWS_REGION \
    --order-by LastEventTime \
    --descending \
    --max-items 1 \
    --query 'logStreams[0].logStreamName' \
    --output text 2>/dev/null | \
xargs -I {} aws logs get-log-events \
    --log-group-name $LOG_GROUP \
    --log-stream-name {} \
    --region $AWS_REGION \
    --start-time $(date -d '1 hour ago' +%s)000 \
    --query 'events[-10:].{Timestamp:timestamp,Message:message}' \
    --output table 2>/dev/null || echo "No recent logs found"

echo ""

# Get S3 bucket info
echo "📦 S3 Bucket Status:"
aws s3 ls s3://production-baseball-power-rankings-static --region $AWS_REGION 2>/dev/null && \
echo "✅ S3 bucket is accessible" || echo "❌ S3 bucket is not accessible"

echo ""

# Quick health check
echo "🏥 Quick Health Check:"
if [ ! -z "$ALB_DNS" ]; then
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://$ALB_DNS 2>/dev/null || echo "000")
    if [ "$HTTP_STATUS" = "200" ]; then
        echo "✅ Application is responding (HTTP 200)"
    else
        echo "❌ Application is not responding properly (HTTP $HTTP_STATUS)"
    fi
else
    echo "⚠️ Cannot perform health check - no load balancer URL"
fi

echo ""
echo "🔗 Useful Links:"
echo "AWS Console - ECS: https://console.aws.amazon.com/ecs/home?region=$AWS_REGION#/clusters/$CLUSTER_NAME"
echo "AWS Console - CloudWatch: https://console.aws.amazon.com/cloudwatch/home?region=$AWS_REGION#logsV2:log-groups/log-group/\$252Fecs\$252Fproduction-bpr"
echo "AWS Console - RDS: https://console.aws.amazon.com/rds/home?region=$AWS_REGION#database:id=production-baseball-power-rankings-db-728078289631"
echo "AWS Console - S3: https://console.aws.amazon.com/s3/buckets/production-baseball-power-rankings-static-728078289631"

echo ""
echo "📋 Useful Commands:"
echo "Check ECS tasks: aws ecs list-tasks --cluster $CLUSTER_NAME --region $AWS_REGION"
echo "View logs: aws logs tail /ecs/production-baseball-power-rankings --region $AWS_REGION --follow"
echo "Check costs: aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-12-31 --granularity MONTHLY --metrics BlendedCost --region us-east-1" 