from django.forms import CharField
from django.forms import ModelForm

from .models import Note
from .models import Tag

class TagForm(ModelForm):
	class Meta:
		model = Tag
		fields = ['name']
		error_messages = {
			'name': {
				'required': 'Please, give a name to the tag.',
				'unique': 'This tag already exists.'
			}
		}

class NoteForm(ModelForm):
	class Meta:
		model = Note
		fields = ['title', 'text', 'link']