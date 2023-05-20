from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Quejas(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	queja = models.TextField(
		null=False,
		blank=False
	)
	def __str__(self):
		return str(self.user)
