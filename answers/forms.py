from django import forms
from pagedown.widgets import PagedownWidget



class AnswerForm(forms.Form):
	content_type = forms.CharField(widget = forms.HiddenInput)
	object_id    = forms.IntegerField(widget = forms.HiddenInput)
	# parent_id    = forms.IntegerField(widget = forms.HiddenInput, required=False )

	answer_text  = forms.CharField(label='', widget = PagedownWidget())



class ReplyForm(forms.Form):
	content_type = forms.CharField(widget = forms.HiddenInput)
	object_id    = forms.IntegerField(widget = forms.HiddenInput)
	# parent_id    = forms.IntegerField(widget = forms.HiddenInput, required=False )

	answer_text  = forms.CharField(label='')