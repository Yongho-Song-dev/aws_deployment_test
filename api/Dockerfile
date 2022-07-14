FROM python:3.9

WORKDIR /srv/aws_test
COPY requirments.txt .
COPY .aws /root/.aws

RUN apt-get -y update \
&& apt-get -y install vim \
&& pip install --upgrade pip \
&& pip install --no-cache-dir -r requirements_deploy.txt 

COPY . /srv/aws_test
EXPOSE 8081

CMD ["uvicorn", "main:app","--reload", "--proxy-headers", "--host", "0.0.0.0", "--port", "8081"]

