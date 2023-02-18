from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Metricas(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	imagen = models.FileField(
		upload_to='archivos/%Y-%m-%d-%H-%M-%S-%f/',
		null=False,
		blank=False
	)
	class Meta:
		permissions = (
			("users", "Modulo de usuarios"),
		)
	def __str__(self):
		return str(self.user)
