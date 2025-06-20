#!/bin/bash

# Test deployment script to debug CloudFormation issues

set -e

AWS_REGION="us-east-2"
STACK_NAME="baseball-power-rankings-test"

echo "🧪 Testing CloudFormation deployment..."

# Check if template file exists
if [ ! -f "cloudformation-template.yaml" ]; then
    echo "❌ CloudFormation template file not found!"
    ls -la
    exit 1
fi

echo "✅ Template file found"

# Check file size
echo "📏 Template file size: $(wc -c < cloudformation-template.yaml) bytes"

# Validate template
echo "🔍 Validating CloudFormation template..."
if aws cloudformation validate-template --template-body file://cloudformation-template.yaml --region $AWS_REGION > /dev/null 2>&1; then
    echo "✅ Template validation successful"
else
    echo "❌ Template validation failed"
    aws cloudformation validate-template --template-body file://cloudformation-template.yaml --region $AWS_REGION
    exit 1
fi

# Generate test password
DB_PASSWORD="test123!"

echo "🚀 Testing deployment with minimal resources..."

# Try to create a minimal stack first
aws cloudformation deploy \
    --template-file cloudformation-template.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides Environment=test DatabasePassword=$DB_PASSWORD \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $AWS_REGION \
    --no-fail-on-empty-changeset

echo "✅ Test deployment completed"

# Clean up test stack
echo "🧹 Cleaning up test stack..."
aws cloudformation delete-stack --stack-name $STACK_NAME --region $AWS_REGION
aws cloudformation wait stack-delete-complete --stack-name $STACK_NAME --region $AWS_REGION

echo "✅ Test completed successfully" 