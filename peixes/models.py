from __future__ import unicode_literals


from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField

#GUARDIAN PERMISSION
from guardian.shortcuts import assign_perm

#GOOGLE MAPS
from geoposition.fields import GeopositionField


@python_2_unicode_compatible


class Projeto(models.Model):
    """docstring for Projeto"""
    nome = models.CharField(max_length=50)
    descrição = models.CharField(max_length=400, blank=True)
    # usuario = models.ManyToManyField(User)
    curador = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["-nome"]
        verbose_name_plural = "Projetos"
        permissions = (("can_view_projeto","Can view any project"),)

class Profile(models.Model):
    """docstring for Profile"""
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    projeto = models.ManyToManyField(Projeto, blank=True)
    Autorização = models.CharField(max_length=30, blank=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Determinação(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["-nome"]
        verbose_name_plural = "Determinadores"

    # def get_absolute_url(self):
    #     return reverse('view_lote', args=[str(self.id)])

class Coletor(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["-nome"]
        verbose_name_plural = "Coletores"


class Lote(models.Model):
    numero_exemplares = models.PositiveIntegerField(verbose_name = 'numero de exemplares')
    determinadores = models.ManyToManyField(Determinação)
    coletores = models.ManyToManyField(Coletor)
    comentarios = models.CharField(max_length=400, blank=True)
    # tecidos = models.ForeignKey(Tecido,on_delete=models.CASCADE, blank=True, null=True)

    """Clasificacao taxonomica"""
    reino = models.CharField(max_length=30, blank=True)
    filo = models.CharField(max_length=50, blank=True)
    classe = models.CharField(max_length=50, blank=True)
    ordem = models.CharField(max_length=50, blank=True)
    familia = models.CharField(max_length=50, blank=True)
    sub_familia = models.CharField(max_length=50, blank=True)
    genero = models.CharField(max_length=50, blank=True)
    especie = models.CharField(max_length=50, blank=True)

    """Dados geograficos"""
    pais = models.CharField(max_length=50, blank=True)
    municipio = models.CharField(max_length=50, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    nome_rio = models.CharField(max_length=50, blank=True, verbose_name = 'nome do rio')
    bacia_hidrografica = models.CharField(max_length=50, blank=True)
    subbacia_hidrografica = models.CharField(max_length=50, blank=True)
    data_coleta = models.DateField(verbose_name = 'data da coleta')
    # latitude = models.FloatField(null=True)
    # longitude = models.FloatField(null=True)

    position = GeopositionField(blank=True)

    publico = models.BooleanField()
    createdby = models.ForeignKey(User)
    projeto = models.CharField(max_length=50,null=True)

    def get_absolute_url(self):
        return reverse('view_lote', args=[str(self.id)])

    def __str__(self):
        return 'LIC #{0}'.format(self.pk)

    class Meta:
        verbose_name_plural = "Lotes"
        permissions =  (("can_edit_lote","Can edit a lote of peixes"),
                        ("can_delete_lote","Can delete a lote of peixes"),
                        ("can_view_lote","Can edit a lote of peixes"),)


    """def get_absolute_url(self):
                    return reverse('view_appointment', args=[str(self.id)])"""

class Tecido(models.Model):
    lote = models.ForeignKey(Lote,on_delete=models.CASCADE)
    especie = models.CharField(max_length=50, blank=True )
    data = models.DateField(blank=True, null=True )
    musculo = models.BooleanField()
    nadadeira = models.BooleanField()
    inteiro = models.BooleanField()
    outro = models.BooleanField()

    def get_absolute_url(self):
        return reverse('view_tecido', args=[str(self.id)])

    def __str__(self):
        return self.especie

    class Meta:
        verbose_name_plural = "Tecidos"


        