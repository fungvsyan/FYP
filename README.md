Cloud 9 Setup

git clone https://github.com/fungvsyan/FYP.git

cd FYP/  
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

aws s3api create-bucket --bucket fyp-demo-bucket --region ap-southeast-1 --create-bucket-configuration LocationConstraint=ap-southeast-1
cp lambda_function/* venv/lib/python3.6/dist-packages
sam package --template-file template.yaml --s3-bucket fyp-demo-bucket --output-template-file package.yaml
aws cloudformation deploy --stack-name fyp-demo-stack --template-file package.yaml --capabilities CAPABILITY_NAMED_IAM

after that you may need to run  
source venv/bin/activate  
if you found that you are not under the Python 3 Virtual Environment.
