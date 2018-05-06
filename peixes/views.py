from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .forms import LoteForm, TecidoForm, ProjetoForm, ProfileForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin #PermissionRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin as PRMDefault
import datetime
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.http import JsonResponse
from registration.backends.hmac.views import RegistrationView
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.db import transaction


#from .forms import CreateLoteForm

from .models import Lote, Determinação, Coletor, Tecido, Projeto, Profile, Peticoes
from django.contrib.auth.models import User, Group

#Exportacao
from django.template import loader, Context

#GUARDIAN PERMISSION

from guardian.shortcuts import assign_perm, get_objects_for_user
from guardian.mixins import PermissionRequiredMixin
from guardian.core import ObjectPermissionChecker #to get list of object with permission to unique object

#IMPORT AND EXPORT
from .resources import LoteResource, TecidoResource
from tablib import Dataset #needed to import data

from django.shortcuts import get_object_or_404





@login_required
@transaction.atomic
def uptade_profile(request, slug):
    #slug_field = "username"
    if request.method == 'POST':
        user_form =UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Seu profile foi atualizado com sucesso!'))
            return redirect('home_peixes')
        else:
            messages.error(request, ('Por favor corriga os erros'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance = request.user.profile)
    return render(request, 'profiles/user_profile_edit.html', {
        'user_form':user_form,
        'profile_form':profile_form
        })


class PeixesView(TemplateView):
    template_name = 'peixes/peixes_modif.html'
    def get_context_data(self, **kwargs):
        context = super(PeixesView, self).get_context_data(**kwargs)
        if Projeto.objects.exists():
            projetos_per_user = Projeto.objects.filter(profile__user__username=self.request.user.username).order_by('-id')
            print(projetos_per_user)
            num_projetos = projetos_per_user.count()
            print(num_projetos)
            curador_peixes = User.objects.filter(groups__name='Curador')
            # list_integrantes = Projeto.objects.get(id=2).usuario
            last_projeto  = Projeto.objects.latest('id')
            list_integrantes = Profile.objects.filter(projeto=last_projeto)
            context['num_projetos'] = num_projetos
            context['projetos'] = projetos_per_user
            context['curador'] = curador_peixes
            context['integrantes'] = list_integrantes
        return context

class LoteListView( ListView):
    """Shows users a list of BDColeta"""
    model = Lote


    def get_context_data(self, **kwargs):
        context = super(LoteListView, self).get_context_data(**kwargs)
        tecidos = Tecido.objects.all()
        projetos = list(Projeto.objects.all().values_list('id','nome'))
        print(self.request.user)
        print(type(self.request.user))
        context['projetos'] = projetos
        context['tecidos'] = tecidos
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated():
            current_user = self.request.user
            qs1 = get_objects_for_user(current_user,'can_view_lote',Lote.objects.all())
            qs2 = Lote.objects.filter(publico=True)
            qs3 = Lote.objects.filter(createdby=current_user)
            qs_ok = (qs1 | qs2 | qs3).distinct()
            return qs_ok
        else:
            return Lote.objects.none()
        


class LoteDetailView(PermissionRequiredMixin, DetailView):
    """Shows users a single appointment"""
    model = Lote
    permission_required = ('can_view_lote')
    raise_exception = True
    permission_denied_message = 'Caro amigo(a) ,não tem permissão para acessar ao lote!'

    def get_context_data(self, **kwargs):
        context = super(LoteDetailView, self).get_context_data(**kwargs)
        tecidos = Tecido.objects.all()
        context['tecidos'] = tecidos
        return context


class LoteCreateView(CreatePopupMixin, SuccessMessageMixin, CreateView):
    """Powers a form to create a new appointment"""
    model = Lote
    #contex_object_name = lote (doing itself by django)
    success_message = 'Lote criado com sucesso.'
    form_class = LoteForm
    template_name = 'peixes/lote_form.html'
    #form_class = LoteForm
    #initial stuff for my form
    #today = datetime.datetime.now()
    #initial = {'data_coleta':today}

    # def get(self, request):
    #     projetos_per_user = Projeto.objects.filter(profile__user__username=self.request.user.username)
    #     if not projetos_per_user.exists():
    #         messages.add_message(request, messages.WARNING, 'Não pertence a nenhum projeto, não pode criar lote!')
    #     return render(request, self.template_name, {})

    #aditional variable in our template
    def get_context_data(self, **kwargs):
        context = super(LoteCreateView, self).get_context_data(**kwargs)
        projetos_per_user = Projeto.objects.filter(profile__user__username=self.request.user.username)
        context['projetos_per_user'] = projetos_per_user
        if Lote.objects.exists():
            context['last_lote_id'] = Lote.objects.latest('id').id+1
        else:
            context['last_lote_id'] = 1
        return context

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.createdby = current_user
        resp = super(LoteCreateView, self).form_valid(form)
        
        lista_pesquisadores = User.objects.filter(groups__name='Pesquisador',profile__projeto__nome=form.instance.projeto)
        curador_peixes = User.objects.get(groups__name='Curador')
        administrador_peixes = User.objects.get(groups__name='Administrador')
        print(type(self.request.user))
        print(lista_pesquisadores)
        print(form.instance.projeto)
        print(type(form.instance))
        print(type(self.object))
        #assigment permission for the user
        assign_perm('can_edit_lote',self.request.user,self.object)
        assign_perm('can_delete_lote',self.request.user,self.object)
        assign_perm('can_view_lote',self.request.user,self.object)

        #assigment permission for the curador of base
        assign_perm('can_edit_lote', curador_peixes, self.object)
        assign_perm('can_delete_lote', curador_peixes, self.object)
        assign_perm('can_view_lote', curador_peixes, self.object)

        #assigment permission for the curador of base
        assign_perm('can_edit_lote', administrador_peixes, self.object)
        assign_perm('can_delete_lote', administrador_peixes, self.object)
        assign_perm('can_view_lote', administrador_peixes, self.object)
        

        #assigment permission for the all pesquisadores related
        if lista_pesquisadores:
            for pesquisador in lista_pesquisadores:
                assign_perm('can_edit_lote', pesquisador, self.object)
                assign_perm('can_delete_lote', pesquisador, self.object)
                assign_perm('can_view_lote', pesquisador, self.object)
            
        # assign_perm('change_article', self.request.user, self.object)
        # assign_perm('delete_article', self.request.user, self.object)
        return resp

   


class LoteUpdateView(PermissionRequiredMixin,UpdatePopupMixin, UpdateView):
    """Powers a form to edit existing BDColeta"""
    model = Lote
    success_message = 'Lote atualizado com sucesso.'
    form_class = LoteForm
    permission_required = ('can_edit_lote')
    raise_exception = True
    # permission_denied_message = 'Caro {} ,não tem permissao para acessar!'.format(request.user)
    permission_denied_message = 'Caro amigo(a),não tem permissao para modificar o lote!'

    def get_context_data(self, **kwargs):
        context = super(LoteUpdateView, self).get_context_data(**kwargs)
        projetos_per_user = Projeto.objects.filter(profile__user__username=self.request.user.username)
        context['projetos_per_user'] = projetos_per_user
        return context


class LoteDeleteView(PermissionRequiredMixin,DeleteView):
    """Prompts users to confirm deletion of an appointment"""

    model = Lote
    success_url = reverse_lazy('list_lotes')
    permission_required = ('can_delete_lote')
    raise_exception = True
    permission_denied_message = 'Caro amigo(a) ,não tem permissao para apagar o lote!'
    

class DeterminadorCreateView(SuccessMessageMixin, CreatePopupMixin, CreateView):
    """Powers a form to edit existing BDColeta"""
    model = Determinação
    success_message = 'Determinador criado com sucesso.'
    fields = ['nome']
    success_url='/'
    

class DeterminadorUpdateView(SuccessMessageMixin, UpdatePopupMixin, UpdateView):
    """Powers a form to edit existing BDColeta"""
    model = Determinação
    success_message = 'Determinador atualizado com sucesso.'
    fields = '__all__'
    success_url='/'

class DeterminadorListView(ListView):
    """Shows users a list of BDColeta"""
    model = Determinação
    

class ColetorCreateView(SuccessMessageMixin, CreatePopupMixin, CreateView):
    """Powers a form to edit existing BDColeta"""
    model = Coletor
    success_message = 'Coletor criado com sucesso.'
    fields = ['nome']
    success_url='/'
   

class ColetorUpdateView(SuccessMessageMixin, UpdatePopupMixin, UpdateView):
    """Powers a form to edit existing BDColeta"""
    model = Coletor
    success_message = 'Coletor atualizado com sucesso.'
    fields = '__all__'
    success_url='/'
    
class ColetorListView(ListView):
    """Shows users a list of BDColeta"""
    model = Coletor

class TecidoCreateView(SuccessMessageMixin,  CreateView):
    model = Tecido
    success_message = 'Tecido criado com sucesso.'
    form_class = TecidoForm
    success_url = reverse_lazy('list_lotes')

    def get_context_data(self, **kwargs):
        context = super(TecidoCreateView, self).get_context_data(**kwargs)
        consulta = list(Lote.objects.all().values_list('id','especie'))
        context['consulta'] = consulta
        return context
    
class TecidoUpdateView(SuccessMessageMixin, UpdateView):
    model = Tecido
    success_message = 'Tecido atualizado com sucesso.'
    fields = '__all__'
    success_url = reverse_lazy('list_tecidos')

class TecidoListView(ListView):
    """Shows users a list of BDColeta"""
    model = Tecido

class TecidoDetailView(DetailView):
    """Shows users a single appointment"""
    model = Tecido    

class TecidoDeleteView(DeleteView):
    """Prompts users to confirm deletion of an appointment"""

    model = Tecido
    success_url = reverse_lazy('list_tecidos')
    #permission_required = ('can_delete_lote')
    #raise_exception = True
    #permission_denied_message = 'Caro amigo(a) ,não tem permissao para apagar o lote!'


#MANY STUFF
def update_consulta(request):
    data = {
        'new_consulta': list(Lote.objects.all().values_list('id','especie'))
    }
    return JsonResponse(data)

def update_consulta_integrantes(request, slug):
    
    print(slug)

    #USERS OF DETERMINATE PROJECT
    usersThisProject = list(Profile.objects.filter(projeto=Projeto.objects.get(id=slug)).values_list('user',flat=True))

    #NEED USERS_ID AND USERNAMES
    usersIdUsername = []

    for i in usersThisProject:
       usersIdUsername.append(list(User.objects.filter(id=i).values_list('id','username'))) 
    
  #NEED USERS_ID AND GROUPS
    usersGroups = []

    for i in usersThisProject:
        usersGroups.append(list(Group.objects.filter(user=i).values_list('user','name')))

    data = {
        'users': usersIdUsername,
        'usersGroups': usersGroups,
    }

    return JsonResponse(data)


#VIEWS PROJETOS
class ProjetoListView(ListView):
    """Shows users a list of BDColeta"""
    model = Projeto
    template_name ='peixes/peixes_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjetoListView, self).get_context_data(**kwargs)
        if Projeto.objects.exists():
            projetos_per_user = Projeto.objects.filter(profile__user__username=self.request.user.username).values_list('id', flat=True)
            context['projetos_per_user'] = projetos_per_user
        return context

class ProjetoCreateView(PRMDefault,SuccessMessageMixin, CreateView):

    model = Projeto
    form_class = ProjetoForm
    success_url = reverse_lazy('home_peixes')
    success_message = 'Projeto criado com sucesso.'
    permission_required = 'peixes.add_projeto'
    raise_exception = True
    permission_denied_message = 'Voce não tem permissão para acessar!'

    def form_valid(self, form):
        current_curador = User.objects.get(groups__name='Curador')
        form.instance.curador = current_curador
        resp = super(ProjetoCreateView, self).form_valid(form)
        #GET THE PROFILE OF CURATOR
        curador_profile = Profile.objects.get(user__id=current_curador.id)
        print(curador_profile)
        print(self.request.user)
        print(type(self.request.user))
        print(self.object)
        #GET THE CURRENT USER
        current_user = User.objects.get(id=self.request.user.id)
        #GET THE CURRENT PROFILE AND ADD
        current_profile = Profile.objects.get(user=current_user)
        current_profile.projeto.add(self.object)
        print(current_profile)
        #ADD PROJECT TO CURRENT PROFILE TO ADMIN AS WELL
        current_profile.projeto.add(self.object)
        if not current_user.is_superuser:
            admin_user = User.objects.get(is_superuser=True)
            admin_profile = Profile.objects.get(user=admin_user)
            admin_profile.projeto.add(self.object)
            
        #ADD PROJECT TO CURRENT CURATOR
        curador_profile.projeto.add(self.object)
        print(self.object)
        return resp
        
##EXPORTACAO

def Export_CSV_Loteview(request):
    lote_resource = LoteResource()
    queryset = get_objects_for_user(request.user, 'can_view_lote', Lote.objects.all())
    dataset = lote_resource.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachtment; filename = "lote.csv"'
    return response

def Export_CSV_Tecidoview(request):
    tecido_resource = TecidoResource()
    dataset = tecido_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tecido.csv"'
    return response

##IMPORTACAO

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        lote_resource = LoteResource()
        dataset = Dataset()
        new_lotes = request.FILES['myfile']
        imported_data = dataset.load(new_lotes.read().decode('utf-8'))
        result = lote_resource.import_data(dataset, dry_run=True, raise_errors=False)  # Test the data import
        print(result)

        if result.has_errors():
            messages.error(request, ('Por favor corriga o(s)) erro(s)'))
        else:
            messages.success(request, ('O arquivo foi carregado com sucesso!'))
            lote_resource.import_data(dataset, dry_run=False,raise_errors=False)  # Actually import now

        return render(request, 'simple_upload.html', {
                'result':result
                })
        
    return render(request, 'simple_upload.html')


#PEDIDOS

#TENTATIVA 1

# def pedidos(request, item):
#     #Projetos with not permission per user
#     projeto_without_acess = Projeto.objects.exclude(profile__user=request.user)
#     if request.method == 'POST':
#         #projetos that user wants to participate
#         projetos_desejados = request.POST.getlist('projetos[]')
#         print(projetos_desejados)
#         request.session['projetos_desejados'] = projetos_desejados

#     return render(request,'peixes/pedidos_lote_projeto_usuario.html', {
#         'item': item,
#         'projetos_notusers':projeto_without_acess, 
#         })

# def revisar_pedidos(request):
#     #get the list of projetos_desejados from pedidos_view throght request session django
#     projetos_desejados = request.session['projetos_desejados']
#     print(projetos_desejados)
#     return render(request, 'peixes/revisar_pedidos.html', {})
#     

class PedidoCreateView(CreateView):
    
    model = Peticoes
    fields = '__all__'
    #form_class = PeticaoForm

    #contex_object_name = lote (doing itself by django)
    #success_message = 'Lote criado com sucesso.'
    # form_class = LoteForm
    #template_name = 'peixes/lote_form.html'

    # def get_form_kwargs(self):
    #     kwargs = super(PedidoCreateView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super(PedidoCreateView, self).get_context_data(**kwargs)
        context['item'] = self.kwargs['item']
        context['projetos_notusers'] = Projeto.objects.exclude(profile__user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.current_user = self.request.user
        resp = super(PedidoCreateView, self).form_valid(form)
        return resp


        