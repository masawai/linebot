FROM public.ecr.aws/amazonlinux/amazonlinux:latest

RUN yum install -y python3 pip3 
RUN pip3 install boto3
COPY dynamo_action.py lambda_function.py ./

CMD ["lambda_function.lambda_handler"]