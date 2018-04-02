import os
from celery import Celery
from django.utils import timezone
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DotPlaceServer_Django.settings')

app = Celery('schimcalculator', broker='amqp://service:dotplace1234@localhost:5672/schim')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.task
def calculator():
    from schimcalculator.models import DotPlace, Score
    
    dotplaces = DotPlace.objects.all()

    for dotplace in dotplaces:
        area = dotplace.area
        owner = dotplace.owner

        targets = DotPlace.objects.filter(area=area).exclude(owner=owner)

        for target in targets:
            alpha, omega = owner, target.owner if int(owner.email) < int(target.owner.email) else target.owner, owner
            
            try:
                score = Score.objects.get(alpha=alpha, omega=omega)
                
            except Score.DoesNotExist:
                score = Score.objects.create(alpha=alpha, omega=omega)
            
            # check home area
            # lat(y) -> 1' : 266667 (m)
            # lng(x) -> 1' : 133333 (m)
            
            if alpha.home and (((area.lat - alpha.home.lat)/133333)**2 + ((area.lng - alpha.home.lng)/266667)**2)**(1/2) < 10000:
                score += 2
            
            if omega.home and (((area.lat - omega.home.lat)/133333)**2 + ((area.lng - omega.home.lng)/266667)**2)**(1/2) < 10000:
                score += 2
            
            if target.is_dot:
                score += 2

            score += 1

            score.save()


@app.task
def collector():
    # time check for 3days
    # erase older dotplaces
    from schimcalculator.models import DotPlace

    dotplaces = DotPlace.objects.all()

    for dotplace in dotplaces:
        if dotplace.time + timedelta(days=3) < timezone.now():
            dotplace.delete()
