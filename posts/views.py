from django.shortcuts import render, get_object_or_404 , redirect
from .models import *
from answers.models import *
from answers.forms import *
from .forms import *
from django.http import HttpResponseRedirect,HttpResponse,Http404,HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import datetime
# Create your views here.

def home(request):
	query_list = admission.objects.all().order_by("-updated","-timestamp")
	query_list2 = placement.objects.all().order_by("-updated","-timestamp")
	c = query_list.count()
	# count = admission_Answer.objects.count
	paginator = Paginator(query_list, 5 )
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    queryset = paginator.page(1)
	except EmptyPage:
	    #If page is out of range (e.g. 9999), deliver last page of results.
	    queryset = paginator.page(paginator.num_pages)



	paginator = Paginator(query_list2, 5 )
	page = request.GET.get('page')
	try:
		queryset2 = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    queryset2 = paginator.page(1)
	except EmptyPage:
	    #If page is out of range (e.g. 9999), deliver last page of results.
	    queryset2 = paginator.page(paginator.num_pages)
	        
	template = loader.get_template('home.html')
	context = RequestContext(request, {
		'query':queryset,
		'query2' : queryset,
		'queryplc' :queryset2 ,
		"count":c,
		})
	return HttpResponse(template.render(context))

def tag(request,tag = None):
	word = tag
	query_list = admission.objects.filter(tags__slug__contains=word).order_by("-updated","-timestamp")
	query_list2 = admission.objects.all().order_by("-updated","-timestamp")
	paginator = Paginator(query_list, 5 )
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    queryset = paginator.page(1)
	except EmptyPage:
	    #If page is out of range (e.g. 9999), deliver last page of results.
	    queryset = paginator.page(paginator.num_pages)
	template = loader.get_template('home.html')
	context = RequestContext(request, {
		'query':queryset,
		'query2' : query_list2,
		
		})
	return HttpResponse(template.render(context))







		

def about(request):
	return render(request,"aboutus.html",{})



def querytype(request):
	return render(request,"querytype.html",{})


def admquery(request):
	if not request.user.is_authenticated():
		raise Http404('You have to login')
	form = admission_form(request.POST or None)
	

	if form.is_valid():


		instance=form.save(commit=False)
		tags_text = form.cleaned_data.get('tags')
		instance.user=request.user
		instance.save()
		tagt = tags_text.split(',')
		for tag in tagt:
			try:
				t = Tag.objects.get(slug=tag)
				instance.tags.add(t)
			except Tag.DoesNotExist:
				t=Tag()
				t.slug = tag
				t.save()
				instance.tags.add(t)
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
	"form":form,
	
	}
	return render(request,"adm_query.html",context)

def admquerylist(request):
	query_list = admission.objects.all().order_by("-updated","-timestamp")
	paginator = Paginator(query_list, 30 )
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    queryset = paginator.page(1)
	except EmptyPage:
	    #If page is out of range (e.g. 9999), deliver last page of results.
	    queryset = paginator.page(paginator.num_pages)
	context = {
	
	"query":queryset,
	}
 	return render(request,"admquerylist.html",context)

def admquerydetail(request,id=None):
	instance=get_object_or_404( admission,id=id)
	


				
	initial_data = {
			"content_type" : instance.get_content_type,
			"object_id" : instance.id,
			}
	answer_form = AnswerForm(request.POST or None , initial = initial_data )
	reply_form = ReplyForm(request.POST or None , initial = initial_data)
	if(request.user.is_authenticated):
	    # if (request.user != instance.user):
			

			if answer_form.is_valid():
				c_type = answer_form.cleaned_data.get('content_type')
				content_type = ContentType.objects.get(model=c_type)
				obj_id = answer_form.cleaned_data.get('object_id')
				content_data = answer_form.cleaned_data.get('answer_text')
				parent_obj = None
				try:
					parent_id = int(request.POST.get("parent_id"))
				except:
					parent_id = None

				if parent_id:
					parent_qs = admission_Answer.objects.filter(id= parent_id)
					if parent_qs.exists() and parent_qs.count() == 1:
						parent_obj = parent_qs.first()


				new_answer, created = admission_Answer.objects.get_or_create(

					user=request.user,
					content_type=content_type,
					object_id=obj_id,
					answer_text=content_data,
					pub_date = datetime.datetime.now(),
					parent = parent_obj



					)
				return HttpResponseRedirect(new_answer.content_object.get_absolute_url())


			
			if reply_form.is_valid():
				c_type = answer_form.cleaned_data.get('content_type')
				content_type = ContentType.objects.get(model=c_type)
				obj_id = answer_form.cleaned_data.get('object_id')
				content_data = answer_form.cleaned_data.get('answer_text')
				parent_obj = None
				try:
					parent_id = int(request.POST.get("parent_id"))
				except:
					parent_id = None

				if parent_id:
					parent_qs = admission_Answer.objects.filter(id= parent_id)
					if parent_qs.exists() and parent_qs.count() == 1:
						parent_obj = parent_qs.first()


				new_answer, created = admission_Answer.objects.get_or_create(

					user=request.user,
					content_type=content_type,
					object_id=obj_id,
					answer_text=content_data,
					pub_date = datetime.datetime.now(),
					parent = parent_obj



					)
				return HttpResponseRedirect(new_answer.content_object.get_absolute_url())	
		
	answers = admission_Answer.objects.filter_by_instance(instance)	
	context = {
	"instance":instance,
	"answers":answers,
	"answer_form":answer_form,
	"reply_form":reply_form,
	
	
	}
 	return render(request,"admquerydetail.html",context)

def admqueryupdate(request,id=None):
	if not request.user.is_authenticated():
		raise Http404('You have to login')
	
	instance=get_object_or_404( admission,id=id)
	if instance.user != request.user :
		raise Http404('You are not the author of this post')
    
	c=len(instance.tags.all())
	t= instance.tags.all()
	d=''
	for x in range(0,c-1) :
		d=d+str(t[x])+','

	d=d+str(t[c-1])
	tt=d
	form = admission_form(request.POST or None ,instance= instance, initial = {'tags': tt })
	


	if form.is_valid():
		instance=form.save(commit=False)
		tags_text = form.cleaned_data.get('tags')
		instance.save()
		tagt = tags_text.split(',')
		for tag in tagt:
			try:
				t = Tag.objects.get(slug=tag)
				instance.tags.add(t)
			except Tag.DoesNotExist:
				t=Tag()
				t.slug = tag
				t.save()
				instance.tags.add(t)
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
	"instance":instance,
	"form":form,
	
	}
	return render(request,"adm_query.html",context)
		

def admquerydelete(request, id=None):
	if not request.user.is_authenticated():
		raise Http404('You have to login')

	instance=get_object_or_404( admission,id=id)
	if instance.user != request.user :
		raise Http404('You are not the author of this post') 
	instance.delete()
	return redirect('admquerylist')




	##########################################3





def plcmntquery(request):
	if not request.user.is_authenticated():
		raise Http404('You have to login')
	form = placement_form(request.POST or None)
	

	if form.is_valid():


		instance=form.save(commit=False)
		tags_text = form.cleaned_data.get('tags')
		instance.user=request.user
		instance.save()
		tagt = tags_text.split(',')
		for tag in tagt:
			try:
				t = Tag.objects.get(slug=tag)
				instance.tags.add(t)
			except Tag.DoesNotExist:
				t=Tag()
				t.slug = tag
				t.save()
				instance.tags.add(t)
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
	"form":form,
	
	}
	return render(request,"plcmnt_query.html",context)

def plcmntquerylist(request):
	query_list = placement.objects.all().order_by("-updated","-timestamp")
	paginator = Paginator(query_list, 30 )
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    queryset = paginator.page(1)
	except EmptyPage:
	    #If page is out of range (e.g. 9999), deliver last page of results.
	    queryset = paginator.page(paginator.num_pages)
	context = {
	
	"query":queryset,
	}
 	return render(request,"plcmntquerylist.html",context)

def plcmntquerydetail(request,id=None):
	instance=get_object_or_404( placement,id=id)
	initial_data = {
			"content_type" : instance.get_content_type,
			"object_id" : instance.id,
			}
	answer_form = AnswerForm(request.POST or None , initial = initial_data )
	reply_form = ReplyForm(request.POST or None , initial = initial_data)
	if(request.user.is_authenticated):
	    # if (request.user != instance.user):
			

			if answer_form.is_valid():
				c_type = answer_form.cleaned_data.get('content_type')
				content_type = ContentType.objects.get(model=c_type)
				obj_id = answer_form.cleaned_data.get('object_id')
				content_data = answer_form.cleaned_data.get('answer_text')
				parent_obj = None
				try:
					parent_id = int(request.POST.get("parent_id"))
				except:
					parent_id = None

				if parent_id:
					parent_qs = placement_Answer.objects.filter(id= parent_id)
					if parent_qs.exists() and parent_qs.count() == 1:
						parent_obj = parent_qs.first()


				new_answer, created = placement_Answer.objects.get_or_create(

					user=request.user,
					content_type=content_type,
					object_id=obj_id,
					answer_text=content_data,
					pub_date = datetime.datetime.now(),
					parent = parent_obj



					)
				return HttpResponseRedirect(new_answer.content_object.get_absolute_url())


			
			if reply_form.is_valid():
				c_type = answer_form.cleaned_data.get('content_type')
				content_type = ContentType.objects.get(model=c_type)
				obj_id = answer_form.cleaned_data.get('object_id')
				content_data = answer_form.cleaned_data.get('answer_text')
				parent_obj = None
				try:
					parent_id = int(request.POST.get("parent_id"))
				except:
					parent_id = None

				if parent_id:
					parent_qs = placement_Answer.objects.filter(id= parent_id)
					if parent_qs.exists() and parent_qs.count() == 1:
						parent_obj = parent_qs.first()


				new_answer, created = placement_Answer.objects.get_or_create(

					user=request.user,
					content_type=content_type,
					object_id=obj_id,
					answer_text=content_data,
					pub_date = datetime.datetime.now(),
					parent = parent_obj



					)
				return HttpResponseRedirect(new_answer.content_object.get_absolute_url())	
		
	answers = placement_Answer.objects.filter_by_instance(instance)	
	context = {
	"instance":instance,
	"answers":answers,
	"answer_form":answer_form,
	"reply_form":reply_form,
	
	}
 	return render(request,"plcmntquerydetail.html",context)

def plcmntqueryupdate(request,id=None):
	if not request.user.is_authenticated():
		raise Http404('You have to login')
	
	instance=get_object_or_404( placement,id=id)
	if instance.user != request.user :
		raise Http404('You are not the author of this post')
    
	c=len(instance.tags.all())
	t= instance.tags.all()
	d=''
	for x in range(0,c-1) :
		d=d+str(t[x])+','

	d=d+str(t[c-1])
	tt=d
	form = placement_form(request.POST or None ,instance= instance, initial = {'tags': tt })
	


	if form.is_valid():
		instance=form.save(commit=False)
		tags_text = form.cleaned_data.get('tags')
		instance.save()
		tagt = tags_text.split(',')
		for tag in tagt:
			try:
				t = Tag.objects.get(slug=tag)
				instance.tags.add(t)
			except Tag.DoesNotExist:
				t=Tag()
				t.slug = tag
				t.save()
				instance.tags.add(t)
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
	"instance":instance,
	"form":form,
	
	}
	return render(request,"plcmnt_query.html",context)
		

def plcmntquerydelete(request, id=None):
	if not request.user.is_authenticated():
		raise Http404('You have to login')

	instance=get_object_or_404( placement,id=id)
	if instance.user != request.user :
		raise Http404('You are not the author of this post') 
	instance.delete()
	return redirect('plcmntquerylist')	



