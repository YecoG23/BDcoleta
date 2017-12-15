from django.forms import ModelForm, DateTimeInput, NumberInput, SelectMultiple, Select, Textarea, ChoiceField, ModelMultipleChoiceField
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.utils.translation import ugettext_lazy as _
from .models import Determinação, Coletor, Tecido, Lote, Projeto, Profile
from django.core.urlresolvers import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper, AddAnotherEditSelectedWidgetWrapper
from django_addanother.contrib.select2 import Select2MultipleAddAnother, Select2EditSelected
from django.contrib.auth.models import User

#INITIAL STUFF


# if User.objects.exists():
# 	list_curador = list(User.objects.filter(groups__name='Curador').values_list('id','username'))
# else:
# 	list_curador = list()

# if Projeto.objects.exists():
# 	list_projetos = list(Projeto.objects.all().values_list('id','nome'))
# else:
# 	list_projetos = list()


class LoteForm(ModelForm):
	# def __init__(self, *args, **kwargs):
	# 	current_user = kwargs.pop('user',None)
	# 	super(LoteForm, self).__init__(*args, *kwargs)
	# 	self.fields['projeto'] = Select(choices = list(Projeto.objects.filter(profile__user__username=current_user.username).values_list('id','nome')) )

	class Meta:
		model = Lote
		exclude = ['createdby']
		widgets = {
			#'projeto': Select(choices = list(Projeto.objects.filter(profile__user__username=current_user.username).values_list('id','nome')) ) ,
			'comentarios': Textarea(attrs = {'placeholder':'Insira seus comentarios aqui'}),
			'determinadores':Select2MultipleAddAnother(reverse_lazy('new_determinador')),
			'coletores' : Select2MultipleAddAnother(reverse_lazy('new_coletor')),
			'latitude': NumberInput(attrs = {'placeholder':'Coordenadas em WGS-84'}),
			'longitude': NumberInput(attrs = {'placeholder':'Coordenadas em WGS-84'}),
		}

class TecidoForm(ModelForm):
	# def __init__(self, *args, **kwargs):
	# 	instance = kwargs.get('instance',None)
	# 	if instance:
	# 		kwargs['initial'] = {'tecido_id':instance.pk}
	# 	super(TecidoForm, self).__init__(*args, **kwargs)
	class Meta:
		model = Tecido
		fields = '__all__'
		widgets = {
			'lote':AddAnotherEditSelectedWidgetWrapper(
				Select,
				reverse_lazy('new_lote'),
				reverse_lazy('edit_lote',args=['__fk__'])),
			
		}

class ProjetoForm(ModelForm):
	# curador  = ModelChoiceField(queryset =User.objects.filter(groups__name='Curador')) 
	class Meta:
		model = Projeto
		fields = ['nome','descrição','curador']
		widgets = {
			'descrição': Textarea(attrs = {'placeholder':'Descrição do projeto aqui'}),

			#'curador': Select(choices = list(User.objects.filter(groups__name='Curador').values_list('id','username'))),
			

			# 'curador': User.objects.filter(groups__name='Curador')[0].username ,
			# 'curador': Select(choices = list_curador),
			#'curador': ChoiceField(queryset =User.objects.filter(groups__name='Curador') ),
		}
		
class ProfileForm(ModelForm):
	# projeto = ModelMultipleChoiceField(queryset =Projeto.objects.all() )
	"""docstring for ProfileForm"""
	class Meta:
		model = Profile
		fields = ['projeto']
		widgets = {

			#'projeto': SelectMultiple(choices = list(Projeto.objects.all().values_list('id','nome'))),
			

			# 'projeto': SelectMultiple(choices = list_projetos),
		}

class UserForm (ModelForm):
	class Meta():
		model = User
		fields = ['username']
			
		