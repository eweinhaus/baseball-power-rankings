#!/bin/bash

# Baseball Power Rankings Deployment Script
# This script automates the deployment of the application to AWS

set -e  # Exit on any error

# Configuration
AWS_REGION="us-east-2"
STACK_NAME="baseball-power-rankings-stack"
ECR_REPOSITORY="baseball-power-rankings"
ACCOUNT_ID="728078289631"

echo "🚀 Starting deployment of Baseball Power Rankings..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install it first."
    exit 1
fi

# Check AWS credentials
echo "🔐 Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials are not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ AWS credentials are valid"

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t $ECR_REPOSITORY:latest .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker image built successfully"

# Login to ECR
echo "🔑 Logging in to Amazon ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

if [ $? -ne 0 ]; then
    echo "❌ ECR login failed"
    exit 1
fi

echo "✅ Logged in to ECR successfully"

# Tag and push Docker image
echo "📤 Pushing Docker image to ECR..."
docker tag $ECR_REPOSITORY:latest $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest

if [ $? -ne 0 ]; then
    echo "❌ Failed to push Docker image to ECR"
    exit 1
fi

echo "✅ Docker image pushed to ECR successfully"

# Deploy CloudFormation stack
echo "☁️ Deploying CloudFormation stack..."
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
aws cloudformation deploy \
    --template-file cloudformation-template.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides Environment=production DatabasePassword=$DB_PASSWORD \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $AWS_REGION

if [ $? -ne 0 ]; then
    echo "❌ CloudFormation deployment failed"
    exit 1
fi

echo "✅ CloudFormation stack deployed successfully"

# Wait for stack to be complete
echo "⏳ Waiting for stack to be complete..."
aws cloudformation wait stack-create-complete --stack-name $STACK_NAME --region $AWS_REGION 2>/dev/null || \
aws cloudformation wait stack-update-complete --stack-name $STACK_NAME --region $AWS_REGION

echo "✅ Stack deployment completed"

# Update ECS service to force new deployment
echo "🔄 Updating ECS service..."
aws ecs update-service \
    --cluster production-baseball-power-rankings-cluster \
    --service production-baseball-power-rankings-service \
    --force-new-deployment \
    --region $AWS_REGION

if [ $? -ne 0 ]; then
    echo "❌ Failed to update ECS service"
    exit 1
fi

echo "✅ ECS service updated"

# Wait for service to be stable
echo "⏳ Waiting for ECS service to be stable..."
aws ecs wait services-stable \
    --cluster production-baseball-power-rankings-cluster \
    --services production-baseball-power-rankings-service \
    --region $AWS_REGION

echo "✅ ECS service is stable"

# Get the load balancer URL
echo "🌐 Getting application URL..."
ALB_DNS=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
    --output text \
    --region $AWS_REGION)

if [ $? -eq 0 ] && [ ! -z "$ALB_DNS" ]; then
    echo "🎉 Deployment completed successfully!"
    echo "🌐 Application URL: http://$ALB_DNS"
    echo "📊 CloudWatch Logs: https://console.aws.amazon.com/cloudwatch/home?region=$AWS_REGION#logsV2:log-groups/log-group/\$252Fecs\$252Fproduction-baseball-power-rankings"
else
    echo "⚠️ Deployment completed but could not retrieve the application URL"
    echo "Please check the AWS Console for the load balancer DNS name"
fi

echo "✅ Deployment script completed" 