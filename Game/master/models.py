from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(to = settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = False, null = False)
    money = models.PositiveBigIntegerField(default = 10000)
    reputation = models.IntegerField(default = 0)
    products = models.IntegerField(default = 0)
    storage = models.IntegerField(default = 5000)
    production = models.IntegerField(default = 3)
    resource = models.IntegerField(default = 20000)
    tax = models.IntegerField(default = 0)
    level = models.IntegerField(default = 0)
    selling_mult = models.IntegerField(default = 8)
    last_active = models.DateTimeField(default = now)