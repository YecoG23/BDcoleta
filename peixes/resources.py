from import_export import resources
from .models import Lote, Tecido

class LoteResource(resources.ModelResource):
	"""docstring for LoteResource"""
	class Meta:
		model = Lote

class TecidoResource(resources.ModelResource):
	"""docstring for LoteResource"""
	class Meta:
		model = Tecido
		