from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from answers.models import *




# Create your models here.

class Tag(models.Model):
    slug = models.SlugField(max_length=100, unique=True)

    def __unicode__(self):
        return str(self.slug)

    class Meta:
        ordering = ('slug',)


class admission(models.Model):
	

    adm_type=(
        ('UG','Under Graduate'),
        ('PG','Post Graduate'),
        ('LEET','UG Leet')
        

    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True)
    admission_Program= models.CharField(max_length=30,choices=adm_type)
    title = models.CharField(max_length=120)
    tags = models.ManyToManyField(Tag)
    content = models.TextField()
    
    timestamp=models.DateTimeField(auto_now_add=True,auto_now=False)
    updated=models.DateTimeField(auto_now_add=False,auto_now=True)

    def __unicode__(self):
        return '%s --------------------- %s' %(self.title,self.user)

    
        
           

    def get_absolute_url(self):
    	return reverse("admquerydetail" , kwargs={"id":self.id})

    @property
    def answers(self):
    	instance=self
    	qs=admission_Answer.objects.filter_by_instance(instance)
        return qs 
    

    @property
    def get_content_type(self):
    	instance=self
    	content_type=ContentType.objects.get_for_model(instance.__class__)
        return content_type
    




   
    





class placement(models.Model):
	

    plc_type=(
        ('Internships','Internships'),
        ('Campus Placement','Campus Placement'),
        
        

    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True)
    Program = models.CharField(max_length=30,choices=plc_type)
    title = models.CharField(max_length=120)
    tags = models.ManyToManyField(Tag)
    content = models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True,auto_now=False)
    updated=models.DateTimeField(auto_now_add=False,auto_now=True)

    def __unicode__(self):
        return '%s --------------------- %s' %(self.title,self.user)

    
        
           

    def get_absolute_url(self):
    	return reverse("plcmntquerydetail" , kwargs={"id":self.id})

    @property
    def answers(self):
    	instance=self
    	qs=placement_Answer.objects.filter_by_instance(instance)
        return qs 
    

    @property
    def get_content_type(self):
    	instance=self
    	content_type=ContentType.objects.get_for_model(instance.__class__)
        return content_type

