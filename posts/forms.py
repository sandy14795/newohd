from django import forms
from .models import *
from pagedown.widgets import PagedownWidget



class admission_form(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget())
	tags = forms.CharField(label='Enter comma separated tags')
	class Meta:
		model=admission
		fields=['admission_Program','title','content','tags']


class placement_form(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget())
	tags = forms.CharField(label='Enter comma separated tags')
	class Meta:
		model=placement
		fields=['Program','title','content','tags']


