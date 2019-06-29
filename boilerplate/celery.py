from celery import Celery

app = Celery('boilerplate', include=['boilerplate.tasks'])

if __name__ == '__main__':
	app.start()
