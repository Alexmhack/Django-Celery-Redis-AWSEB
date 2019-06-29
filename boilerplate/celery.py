from celery import Celery

app = Celery('boilerplate', broker='redis://', include=['boilerplate.tasks'],
	backend='redis://')

if __name__ == '__main__':
	app.start()
