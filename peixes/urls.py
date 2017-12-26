from django.conf.urls import url
from django.views.generic import TemplateView
from .views import (
                    LoteListView, 
                    LoteCreateView, 
                    LoteDetailView, 
                    LoteUpdateView, 
                    LoteDeleteView, 
                    DeterminadorCreateView, 
                    DeterminadorUpdateView, 
                    ColetorCreateView, 
                    ColetorUpdateView, 
                    TecidoCreateView, 
                    TecidoUpdateView,
                    TecidoDetailView,
                    TecidoDeleteView, 
                    uptade_profile
    )
from .views import ProjetoListView, PeixesView, ProjetoCreateView
from .views import DeterminadorListView, ColetorListView, TecidoListView
from .views import Export_CSV_Loteview, Export_CSV_Tecidoview
from django.conf.urls.static import static
from django.conf import settings
from .views import update_consulta, update_consulta_integrantes



urlpatterns = [
    url(r'^$', PeixesView.as_view(), name='home_peixes'),
    url(r"^user/settings/profile/(?P<slug>[\w-]+)/$", uptade_profile, name='edit_profile'),

    #LOTE
    # List,detail and export views
    url(r'^lote/lista$', LoteListView.as_view(), name='list_lotes'),
    url(r'^lote/lista/export$', Export_CSV_Loteview , name='list_lotes_export'),
    url(r'^lote/(?P<pk>[0-9]+)/detail$', LoteDetailView.as_view(), name='view_lote'),

    # Create, update, delete lote
    url(r'^lote/add$', LoteCreateView.as_view(), name='new_lote'),
    url(r'^lote/(?P<pk>.*)/edit$', LoteUpdateView.as_view(), name='edit_lote'),
    url(r'^lote/(?P<pk>[0-9]+)/delete$', LoteDeleteView.as_view(), name='delete_lote'),

    #DETERMINADOR
    # List and detail views
    url(r'^determinador/lista$', DeterminadorListView.as_view(), name='list_determinadores'),
    # url(r'^lote/(?P<pk>[0-9]+)/detail$', LoteDetailView.as_view(), name='view_lote'),

    # Create, update, delete determinador
    url(r'^determinador/add$', DeterminadorCreateView.as_view(), name='new_determinador'),
    url(r'^determinador/(?P<pk>[0-9]+)/edit$', DeterminadorUpdateView.as_view(), name='edit_determinador'),
    # url(r'^lote/(?P<pk>[0-9]+)/delete$', LoteDeleteView.as_view(), name='delete_lote'),

    #COLETOR
    # List and detail views
    url(r'^coletor/lista$', ColetorListView.as_view(), name='list_coletores'),
    # url(r'^lote/(?P<pk>[0-9]+)/detail$', LoteDetailView.as_view(), name='view_lote'),

    # Create, update, delete coletor
    url(r'^coletor/add$', ColetorCreateView.as_view(), name='new_coletor'),
    url(r'^coletor/(?P<pk>[0-9]+)/edit$', ColetorUpdateView.as_view(), name='edit_coletor'),

    #TECIDO
    #List,detail and view
    url(r'^tecido/lista$', TecidoListView.as_view(), name='list_tecidos'),
    url(r'^tecido/(?P<pk>[0-9]+)/detail$', TecidoDetailView.as_view(), name='view_tecido'),
    url(r'^tecido/lista/export$', Export_CSV_Tecidoview , name='list_tecidos_export'),
    # url(r'^lote/(?P<pk>[0-9]+)/detail$', LoteDetailView.as_view(), name='view_lote'),

    # Create, update, delete tecido
    url(r'^tecido/add$', TecidoCreateView.as_view(), name='new_tecido'),
    url(r'^tecido/(?P<pk>[0-9]+)/edit$', TecidoUpdateView.as_view(), name='edit_tecido'),
    url(r'^tecido/(?P<pk>[0-9]+)/delete$', TecidoDeleteView.as_view(), name='delete_tecido'),

    #AJAX_CONSULTA
    url(r'^ajax/update_consulta/$', update_consulta, name='update_consulta'),
    url(r'^ajax/update_consulta_integrantes/(?P<slug>[\w\-]+)/$', update_consulta_integrantes, name='update_consulta_integrantes'),


    #PROJETOS
    url(r'^lista$', ProjetoListView.as_view(), name='list_projetos'),
    url(r'^projeto/add$', ProjetoCreateView.as_view(), name='new_projeto'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),