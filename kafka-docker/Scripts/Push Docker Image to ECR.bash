# These commands remove inherited permissions and grant read access to current user only, used to fix .pem file permissions (on local system)
icacls open-aq-server_key.pem /inheritance:r
icacls open-aq-server_key.pem /grant:r "%username%:R"

cd C:\Users\admin\Desktop\Test\kafka-docker\openaq-pipeline

#Build the image
docker build -t openaq-pipeline .

# 3. Tag with your REAL account ID
docker tag openaq-pipeline:latest <YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/openaq-pipeline:latest

# 4. Login to ECR (single line, no backslashes)
aws ecr get-login-password --region <YOUR_REGION> | docker login --username AWS --password-stdin <YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com

# 5. Push
docker push <YOUR_ACCOUNT_ID>.dkr.ecr.<YOUR_REGION>.amazonaws.com/openaq-pipeline:latest