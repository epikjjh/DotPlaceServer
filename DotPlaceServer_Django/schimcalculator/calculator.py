from celery import Celery

app = Celery('calculator', broker='pyamqp://guests@localhost')

@app.task
def add(x,y):
    return x+y