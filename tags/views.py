import json

from django.contrib.auth import authenticate, login
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .models import Color
from .models import Note
from .models import Tag
from .forms import NoteForm
from .forms import TagForm
from .decorators import require_ajax

# HTTP status code:
# 400: invalid form; 409: desync

# How to get notes_ids related to some tag:
#notes_ids = []
#if tag.note_set:
#	notes_ids = list(tag.note_set.all().values_list('id', flat=True))

@require_GET
@ensure_csrf_cookie
def index(request):
	#if request.user.is_authenticated:
	context = {
		'color_list': Color.objects.all(),
		'tag_list': Tag.objects.all(), 
		'note_list': Note.objects.all()
	}
	return render(
		request, 
		'tags/index.html', 
		context)
	#else:
		#return render(
			#request, 
			#'tags/login.html')

#def create

def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect('tags:index')
	else:
		pass


@require_POST
@require_ajax
def create_tag(request):
	form = TagForm(request.POST)
	if form.is_valid():
		tag = form.save()
		try:
			color = Color.objects.get(pk=request.POST.get('color'))
			tag.color = color
			tag.save()
		except:
			pass
		return render(
			request, 
			'tags/tag_list.html', 
			context={'color_list': Color.objects.all(), 'tag_list': Tag.objects.all()})
	else:
		return JsonResponse(json.loads(form.errors.as_json()), status=400)

@require_POST
@require_ajax
def delete_tag(request, tag_id):
	try:
		tag = Tag.objects.get(pk=tag_id)
	except Tag.DoesNotExist:
		return render(
			request, 
			'tags/tag_list.html', 
			context={'color_list': Color.objects.all(), 'tag_list': Tag.objects.all()}, 
			status=409)
	else:
		tag.delete()
		return JsonResponse({'tag_id': tag_id})

@require_POST
@require_ajax
def update_tag_color(request, tag_id, color_id):
	try:
		tag = Tag.objects.get(pk=tag_id)
		color = Color.objects.get(pk=color_id)
	except ObjectDoesNotExist:
		return render(
			request, 
			'tags/tag_list.html', 
			context={'color_list': Color.objects.all(), 'tag_list': Tag.objects.all()}, 
			status=409)
	else:
		tag.color = color
		tag.save()
		return JsonResponse({'tag_id': tag.id, 'tag_color': tag.color})

@require_POST
@require_ajax
def update_tag_name(request, tag_id):
	try:
		tag = Tag.objects.get(pk=tag_id)
	except Tag.DoesNotExist:
		return render(
			request, 
			'tags/tag_list.html', 
			context={'color_list': Color.objects.all(), 'tag_list': Tag.objects.all()}, 
			status=409)
	else:
		form = TagForm(
			{'name': request.POST.get('tag_name')}, 
			instance=tag)
		if form.is_valid():
			form.save()
			template = render_to_string(
				'tags/tag_list.html', 
				{'color_list': Color.objects.all(), 'tag_list': Tag.objects.all()}, 
				request=request)
			return JsonResponse({
				'template': template, 
				'tag_id': tag.id, 
				'tag_name': tag.name
			})
		else:
			return JsonResponse(
				json.loads(form.errors.as_json()), 
				status=400)

@require_POST
@require_ajax
def create_note(request):
	form = NoteForm(request.POST)
	if form.is_valid():
		new_note = form.save()
		has_new_tags = False
		for tag_name in request.POST.get('tags'):
			try:
				tag = Tag.objects.get(name=tag_name)
			except ObjectDoesNotExist:
				tagForm = TagForm(name=tag_name)
				if tagForm.is_valid():
					tag = tagForm.save()
					has_new_tags = True
				else:
					continue
			new_note.tags.add(tag)
		if has_new_tags:
			tag_list_template = render_to_string(
				'tags/tag_list.html', 
				context={'color_list': Color.objects.all(), 'tag_list': Tag.objects.all()})
			node_list_template = render_to_string(
				'tags/node_list.html', 
				context={'note_list': Note.objects.all()})
			return JsonResponse({'tag_list': tag_list_template, 'node_list': node_list_template})
		else:
			return render(
				request, 
				'tags/note_list.html', 
				context={'note_list': Note.objects.all()})
	else:
		return JsonResponse(
			json.loads(form.errors.as_json()), 
			status=400)

@require_POST
@require_ajax
def remove_note_tag(request, note_id, tag_id):
	try:
		note = Note.objects.get(pk=note_id)
		tag = Tag.objects.get(pk=tag_id)
		tag.note_set.remove(note)
	except ObjectDoesNotExist:
		return render(
			request, 
			'tags/note_list.html', 
			context={'note_list': Note.objects.all()}, 
			status=409)
	else:
		return JsonResponse({'tag_id': tag.id})

@require_POST
@require_ajax
def delete_note(request, note_id):
	try:
		note = Note.objects.get(pk=note_id)
	except Note.DoesNotExist:
		return render(
			request, 
			'tags/note_list.html', 
			context={'note_list': Note.objects.all()}, 
			status=409)
	else:
		note.delete()
		return JsonResponse({'note_id': note.id})