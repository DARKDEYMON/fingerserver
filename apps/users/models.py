from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import numpy as np
from .fingermodule import *
import cv2

# Create your models here.

class Metricas(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	imagen = models.FileField(
		upload_to='archivos/%Y-%m-%d-%H-%M-%S-%f/',
		null=False,
		blank=False
	)
	"""
	def save(self, *args, **kwargs):
		read = self.imagen.read()
		image = readBytesCV2(read)
		limpiado = limpiarBytes(image)

		ret, buf = cv2.imencode('.jpg', limpiado)
		content = ContentFile(buf.tobytes())
		self.imagen.save(str(self.imagen.name), content, save=False)
		return super().save(*args, **kwargs)
	"""
	class Meta:
		permissions = (
			("users", "Modulo de usuarios"),
		)
	def __str__(self):
		return str(self.user)

class Tiqueo(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	fecha = models.DateTimeField(
		auto_now_add = True,
		blank = False,
		null = False
	)
	def __str__(self):
		return str(self.user)
