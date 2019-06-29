from celery import Celery

app = Celery('boilerplate', include=['boilerplate.tasks'])

app.config_from_object('django.conf:settings')

if __name__ == '__main__':
	app.start()
