from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from celery.execute import send_task


# 점수는 대칭 관계임
class Score(models.Model):
    alpha = models.ForeignKey('dotplace.User', on_delete=models.CASCADE, related_name='alpha')
    omega = models.ForeignKey('dotplace.User', on_delete=models.CASCADE, related_name='omega')
    score = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now=True)


# lat(y) : 48000000(m) ÷ 180 -> 10(m) : 0.0000375
# lng(x) : 48000000(m) ÷ 360 -> 10(m) : 0.000075
class Area(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    numofdots = models.IntegerField(default=0)


class DotPlace(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    owner = models.ForeignKey('dotplace.User', on_delete=models.CASCADE)
    ticket = models.FloatField(default=0.0)
    time = models.DateTimeField(auto_now_add=True)
    is_dot = models.BooleanField()

    class Meta:
        ordering = ['-ticket']

@receiver(post_save, sender=DotPlace)
def activate_worker(sender, instance=None, created=False, **kwargs):
    send_task('schimcalculator.celery.calculator')
    send_task('schimcalculator.celery.collector')
