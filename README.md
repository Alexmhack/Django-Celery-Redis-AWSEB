# Django-Celery-SQS-AWSEB
Deploying Django application with Celery and Reddis as broker on AWS Elastic Beanstalk

**UPDATE**: Elastic Cache Redis instance on AWS can cost you much more than SQS will, so I have switched from Redis to SQS.
SQS even has 1 million requests free every month.

**CAVEAT**: Only thing that SQS Celery broker lacks is the result backend, which is not yet available for SQS
