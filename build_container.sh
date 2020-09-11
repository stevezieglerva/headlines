# Get the env variables
AWS_ACCESS_KEY_ID=$(aws --profile default configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws --profile default configure get aws_secret_access_key)
export ACCOUNTID=`aws sts get-caller-identity --query Account --output text`

# Build the image
docker build -t ziegler-headings-build .

# Test the image
docker run --rm -it -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY ziegler-headings-build

# Push to ECR
aws ecr create-repository --repository-name ziegler-headings-build 
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ACCOUNTID.dkr.ecr.us-east-1.amazonaws.com
docker tag ziegler-headings-build:latest $ACCOUNTID.dkr.ecr.us-east-1.amazonaws.com/ziegler-headings-build:latest
docker push $ACCOUNTID.dkr.ecr.us-east-1.amazonaws.com/ziegler-headings-build:latest



# Run the task as a test
aws ecs run-task --cli-input-json file://run_task_input.json
 