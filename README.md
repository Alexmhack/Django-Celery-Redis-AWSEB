# Django-Celery-SQS-AWSEB
Deploying Django application with Celery and Reddis as broker on AWS Elastic Beanstalk

**UPDATE**: Elastic Cache Redis instance on AWS can cost you much more than SQS will, so I have switched from Redis to SQS.
SQS even has 1 million requests free every month.

**CAVEAT**: Only thing that SQS Celery broker lacks is the result backend, which is not yet available 
for SQS, which basically means that you cannot store the results that are returned from your tasks 
anywhere,

`result = some_task.delay()`
`result.get()  # gives error -> Result backend 'sqs' not found.`

# Getting Started
To get started you need to first launch a Elastic Beanstalk environment inside a VPC. I assume you
have a VPC already created if not [create](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/vpc-rds.html).

**NOTE:** AWS RDS won't create a **Subnet Group** until you have subnets in two availability zones.
So for that go into your **VPC** console > **Subnets** then create two new subnets with availability 
zones different from your default subnets, if you have any problems with the **
IPv4 CIDR block** then enter `10.0.2.0/24` and `10.0.3.0/24`. If you have another range for example
`35.23.2.0/24` then use that but these **CIDR Blocks** should not overlap with the existing ones.

Now run the following commands for launching EB Environment inside newly created VPC.

1. `eb create test -db.engine postgres -db.user rootuser -db.pass rootpass --vpc --vpc.dbsubnets xxxxxxxxxxx,xxxxxxxxxxx,xxxxxxxxxxxxx,xxxxxxxxxxxx`

	`--vpc.dbsubnets` -> **Subnets of the RDS that you just created**

2. You will be prompted to enter some details about the VPC you have just created like the **VPC Id** 
	which you can get from the VPC Console and you should assign a **public IP address** and for the 
	**EC2 instance subnet** enter the private subnet which defaults to `10.0.1.0/24` and for the 
	**EB subnet groups** enter the public subnet which defaults to `10.0.0.0/24`.

3. Assign a external/public load balancer and for the security group enter the default VPC Security 
	group that is newly created by your VPC in the section **VPC Console > Security Groups.**

4. The EB Env should take about 5 to 10 minutes to finish and start.

5. Now if you haven't set the **WSGIPath** setting then use `eb config` and in the window that 
	appears find the **WSGIPath** and replace that path with your django project `wsgi.py` file like,
	`WSGIPath: boilerplate/wsgi.py`. Save the file and close the window, the env will start updating.

6. Run `eb status` and copy paste the **CNAME** in your `ALLOWED_HOSTS` settings.

7. Deploy the application and you run `eb open`.

# SQS
Head to the AWS **SQS** (Simple Queue Service) console and **Create New Queue**.

1. Enter the name of the queue. 

2. Standard Queue should work with most of the use cases.

3. In **Configure Queue** you can use the **Use SE**.

4. Click **create queue**

Copy the queue name and paste it in the `CELERY_DEFAULT_QUEUE` setting in your `settings.py` file,
you can even use the environment variables of your elasticbeanstalk environment to hide the name of your queue like I did in my settings.

With this done, you also need a AWS **IAM User** with a Role or Group that has permissions to access 
the Simple Queue Service, you can create it easily with programmatic access and use the credentials 
generated in your environment.

Define two environment variables namely, `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY` by EB Console > Configuration > Software.

Create a file named `celeryapp.py` along side your `settings.py` file with code same as this repo 
contains. You may need to change some things like,

`os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boilerplate.settings')` -> boilerplate is my project name yours might be different, change it everywhere.

In your settings define some more celery configuration settings like

`CELERY_DEFAULT_QUEUE = os.getenv('CELERY_DEFAULT_QUEUE') # name of your sqs queue`

`AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')`

`CELERY_RESULT_BACKEND = None  # Disabling the results backend since not supported with SQS`

`BROKER_TRANSPORT_OPTIONS = {`

`    'polling_interval': 20,`

`    'region': 'ap-south-1',`

`}`

`BROKER_URL = "sqs://"`

The `BROKER_URL` here takes only `"sqs://"` and the rest of the things are done by celery itself by 
colleting the necessary credentials for access to this SQS queue using the credentials we have set in 
your environment variables.

**NOTE:** I first used `celery.py` named file that was causing some errors despite of the 
`absolute_import` on top of the file so finally I changed the file name to `celeryapp.py` and
that worked.

Also you need the `.ebextensions` folder my this repo to run the celery worker and don't forget to 
install and use the `requirements.txt` file same as mine.

We use pooling in celery worker from the `gevent` package by providing and extra argument 

`celery -A boilerplate worke -l Info -P gevent --app=boilerplate.celeryapp:app`

`--app` is to give the location of our celery app since we have changed the file names from 
`celery.py` to `celeryapp.py`. 

**I have tested everything and my repo works perfectly fine in the elastic beanstalk environment. If you face any problems checkout this repo code and make changes accordingly in case I have missed something in the instructions.**
