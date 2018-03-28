from dotplace.models import User
from django.db import models


# 점수는 대칭 관계임
class Score(models.Model):
    alpha = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alpha')
    omega = models.ForeignKey(User, on_delete=models.CASCADE, related_name='omega')
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.FloatField(default=0.0)
    time = models.DateTimeField(auto_now_add=True)
    is_dot = models.BooleanField()
    pin = models.BooleanField(default=True)