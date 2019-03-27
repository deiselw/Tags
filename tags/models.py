import re

from django.core.validators import MaxValueValidator
from django.db import models
from django.forms import ValidationError
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Color(models.Model):
	hex = models.PositiveIntegerField(validators=[MaxValueValidator(16777215)])

	def __str__(self):
		return '#' + '{:06x}'.format(self.hex)

@python_2_unicode_compatible
class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)
	color = models.ForeignKey(Color, on_delete=models.SET_DEFAULT, default=1)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name

	def clean(self):
		self.name = self.name.replace(" ", "").lower()

class Note(models.Model):
	creation_date = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=100, blank=True)
	text = models.CharField(max_length=1000, blank=True)
	link = models.TextField(blank=True)
	tags = models.ManyToManyField(Tag)

	def clean(self):
		self.title = self.title.strip()
		self.link = self.link.strip()
		if self.title is None and self.text is None and self.link is None:
			raise ValidationError('Your note is empty')