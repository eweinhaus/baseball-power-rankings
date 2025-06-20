# Baseball Power Rankings

A web application for tracking and displaying baseball power rankings using Python, Dash, and AWS infrastructure.

**🚀 CI/CD Pipeline Status: Ready for deployment!**

## Infrastructure

This application is deployed using the following AWS services:

- **ECS Fargate**: Serverless containers for running the application
- **RDS PostgreSQL**: Database for storing application data (free tier)
- **S3**: Static file storage
- **Application Load Balancer**: Traffic distribution
- **CloudWatch**: Monitoring and logging
- **CloudFormation**: Infrastructure as Code

## Local Development

### Prerequisites

- Python 3.9+
- Docker
- AWS CLI

### Running Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Access the application**:
   Open your browser and go to `http://localhost:10000`

### Docker Development

1. **Build the Docker image**:
   ```bash
   docker build -t my-app .
   ```

2. **Run the container**:
   ```bash
   docker run -p 10000:10000 my-app
   ```

## Deployment

### Prerequisites

1. **AWS Account**: Ensure you have an AWS account with appropriate permissions
2. **AWS CLI**: Configure your AWS credentials
3. **GitHub Repository**: Push your code to GitHub

### Setup AWS Credentials

1. **Create an IAM user** with the following permissions:
   - ECR full access
   - ECS full access
   - RDS full access
   - S3 full access
   - CloudFormation full access
   - Secrets Manager full access
   - CloudWatch full access

2. **Configure AWS CLI**:
   ```bash
   aws configure
   ```

### Manual Deployment

1. **Create ECR Repository**:
   ```bash
   aws ecr create-repository --repository-name baseball-power-rankings --region us-east-2
   ```

2. **Login to ECR**:
   ```bash
   aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 728078289631.dkr.ecr.us-east-2.amazonaws.com
   ```

3. **Build and push Docker image**:
   ```bash
   docker build -t 728078289631.dkr.ecr.us-east-2.amazonaws.com/baseball-power-rankings:latest .
   docker push 728078289631.dkr.ecr.us-east-2.amazonaws.com/baseball-power-rankings:latest
   ```

4. **Deploy CloudFormation stack**:
   ```bash
   aws cloudformation deploy \
     --template-file cloudformation-template.yaml \
     --stack-name baseball-power-rankings-stack \
     --parameter-overrides Environment=production \
     --capabilities CAPABILITY_NAMED_IAM \
     --region us-east-2
   ```

### Automated Deployment (GitHub Actions)

1. **Add GitHub Secrets**:
   - Go to your GitHub repository settings
   - Navigate to Secrets and variables > Actions
   - Add the following secrets:
     - `AWS_ACCESS_KEY_ID`: Your AWS access key
     - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

2. **Push to main branch**:
   The GitHub Actions workflow will automatically:
   - Build the Docker image
   - Push to ECR
   - Deploy the CloudFormation stack
   - Update the ECS service

## Infrastructure Details

### ECS Fargate
- **CPU**: 256 (.25 vCPU)
- **Memory**: 512 MB
- **Port**: 10000
- **Auto-scaling**: Disabled (can be enabled for production)

### RDS PostgreSQL
- **Instance Class**: db.t3.micro (free tier)
- **Storage**: 20 GB
- **Backup Retention**: 7 days
- **Multi-AZ**: Disabled (free tier limitation)

### S3 Bucket
- **Name**: `production-baseball-power-rankings-static`
- **Access**: Private (accessed via IAM roles)
- **CORS**: Enabled for web access

### Security
- **VPC**: Custom VPC with public and private subnets
- **Security Groups**: Restricted access to necessary ports only
- **IAM Roles**: Least privilege access for ECS tasks

## Monitoring

### CloudWatch
- **Logs**: Application logs are sent to CloudWatch Logs
- **Metrics**: ECS service metrics are automatically collected
- **Alarms**: Can be configured for CPU, memory, and error rates

### Health Checks
- **Load Balancer**: HTTP health checks on port 10000
- **ECS**: Container health checks
- **Database**: RDS automated backups and monitoring

## Cost Optimization

### Free Tier Usage
- **RDS**: db.t3.micro instance (750 hours/month)
- **ECR**: 500 MB storage and 5 GB transfer
- **CloudWatch**: 5 GB log ingestion and 5 GB log storage

### Cost Monitoring
- Set up AWS Cost Explorer to monitor spending
- Configure billing alerts
- Use AWS Budgets to set spending limits

## Troubleshooting

### Common Issues

1. **ECS Service not starting**:
   - Check CloudWatch logs for container errors
   - Verify ECR image exists and is accessible
   - Check security group configurations

2. **Database connection issues**:
   - Verify RDS security group allows ECS traffic
   - Check database endpoint and credentials
   - Ensure database is in the correct VPC

3. **Load Balancer health check failures**:
   - Verify application is listening on port 10000
   - Check security group allows ALB traffic
   - Review application logs for errors

### Useful Commands

```bash
# Check ECS service status
aws ecs describe-services --cluster production-baseball-power-rankings-cluster --services production-baseball-power-rankings-service

# View CloudWatch logs
aws logs describe-log-groups --log-group-name-prefix /ecs/production-baseball-power-rankings

# Check RDS status
aws rds describe-db-instances --db-instance-identifier production-baseball-power-rankings-db

# Get load balancer DNS
aws cloudformation describe-stacks --stack-name baseball-power-rankings-stack --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' --output text
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This project is licensed under the MIT License.

Dash Web App that gets the live updating scores and schedule from Boston Men's Amateur Baseball League website and creates: Standings, Power Rankings, Single Game Win Probability, and Playoff Probability.

Deployed to: https://dash-playoff-odds.onrender.com/

**1. Standings:**
Uses webcrawler to grab outcome of each game and create league standings updated to the minute.



**2. Power Rankings:**
Takes each team's performance thus far (Runs Scored, Runs Allowed, and Games Played) and applies Bill James' Pythagorean Win Probability formula to estimate each team's expected win percentage vs. a league average team.

![Screen Shot 2024-02-04 at 11 18 03 PM](https://github.com/eweinhaus/baseball-power-rankings/assets/98419357/83e0f6ca-17b9-4962-b1d6-101ef8804e83)

Using a derivative of Tangotigers win probability forumla, factors in each team's home field advantage and strength of schedule into pythagorean win percentage in order to get adjusted expected winning percentage (Power Rank)

![Screen Shot 2024-02-04 at 11 35 22 PM](https://github.com/eweinhaus/baseball-power-rankings/assets/98419357/cb255c93-8331-43ae-9c97-dc4e568e36bf)



**3. Single Game Win Probability:**
Applies Tangotiger's win probability formula to each team's power rank in order to estimate the percentage chance any given home team beats any given away team in a potential matchup.

![Screen Shot 2024-02-04 at 11 40 30 PM](https://github.com/eweinhaus/baseball-power-rankings/assets/98419357/78a790a6-b915-4c5e-807a-4524c92dfecd)

Utilizes Dash callbacks in order to allow user to input any potential matchup and estimate outcome in real time.



**4. Playoff Probability:**
Given current standings, power rankings, individual matchup win probability, and remaining schedule, app uses Pandas and Numpy to run a Monte Carlo simulation to simulate the rest of the season 1000 times and graphs the probability that each team finishes top 6 in the standings in order to make the league playoffs.


