from rest_framework import viewsets
from django.apps import apps
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .fingermodule import *

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.filter(is_staff=False)
	serializer_class = UserSerializer

"""
@api_view(['GET', 'POST'])
def figer_print_viewset(request):
	print("hola")
	if request.method == 'POST':
		import pdb; pdb.set_trace()
		return Response({"message": "Got some data!"})
	return Response({"message": "Hello, world!"})
"""

class FigerPrintViewSet(APIView):
	serializer_class = FigerSerializer
	model_metricas = Metricas
	def get(self, request, *args, **kwargs):
		return Response({"message":"Envie una foto via POST para la verificacion de Huella"})

	def post(self, request, *args, **kwargs):
		imagenr = request.FILES['image']
		read = imagenr.read()
		image_prueba = readBytesCV2(read)
		image_prueba = limpiarBytes(image_prueba)
		metricas = self.model_metricas.objects.all()
		maxp = 0
		maxobj = None
		for m in metricas:
			a, b, c =compararBytes(image_prueba, cv2.imread(m.imagen.path))
			print(m.user, c)
			if(c>maxp or c>=0.5):
				maxp=c
				maxobj = m
			if(c>=0.5):
				break
		#print(maxobj, maxp)
		if(maxobj and maxp>=0.5):
			serializer = UserSerializer(maxobj.user)
			print(serializer.data)
			return Response(serializer.data)
		return Response({"user":None})
