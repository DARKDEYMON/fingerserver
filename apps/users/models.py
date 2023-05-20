from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import numpy as np
from .fingermodule import *
from django.contrib.postgres.fields import ArrayField
import cv2
import json
import pickle

# Create your models here.

class Kardex(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	ci = models.CharField(
		max_length=50
	)
	hoja_vida = models.TextField(
		verbose_name='Hoja de vida',
	)
	recorrido = models.TextField(
		verbose_name='Hoja de recorrido',
	)
	ubicacion_actual = models.CharField(
		max_length=5000,
		blank = False,
		null = False
	)
	class Meta:
		permissions = (
			("users", "Modulo de Personal"),
		) 
	def __str__(self):
		return str(self.user)

class PermisosGenerales(models.Model):
	motivo = models.CharField(
		max_length=1000,
		blank = False,
		null = False
	)
	fecha_inicio = models.DateField(
		blank = False,
		null = False
	)
	fecha_fin = models.DateField(
		blank = False,
		null = False
	)
	def verificar(self, date):
		res = PermisosGenerales.objects.all()
		for r in res:
			if(r.fecha_inicio == r.fecha_fin and date==r.fecha_inicio):
				return r
			elif(r.fecha_inicio<date<r.fecha_fin):
				return r
			return None
	def __str__(self):
		return self.motivo

class Permisos(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	motivo = models.CharField(
		max_length=1000,
		blank = False,
		null = False
	)
	fecha_inicio = models.DateField(
		blank = False,
		null = False
	)
	fecha_fin = models.DateField(
		blank = False,
		null = False
	)
	def verificar(self, date):
		if(self.fecha_inicio == self.fecha_fin and self.data==self.fecha_inicio):
			return True
		elif(self.fecha_inicio<date<self.fecha_fin):
			return True
		return False
	def __str__(self):
		return str(self.user)

class Metricas(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	imagen = models.FileField(
		upload_to='archivos/%Y-%m-%d-%H-%M-%S-%f/',
		null=False,
		blank=False
	)
	binary = models.BinaryField(
		verbose_name='Array',
		null=True,
		blank=True,
	)
	@property
	def binary_decode(self):
		return pickle.loads(self.binary)
	def save(self, *args, **kwargs):
		detector = cv2.SIFT_create()
		read = self.imagen.read()
		image = readBytesCV2(read)
		keypoints1, descriptors1 = detector.detectAndCompute(image, None)
		#print(str(descriptors1))
		self.binary = pickle.dumps(descriptors1)
		return super().save(*args, **kwargs)
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
		return str(self.user) + ' ' + str(self.fecha)
