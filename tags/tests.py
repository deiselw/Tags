from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .forms import TagForm
from .models import Tag

class TagModelTests(TestCase):
	def test_create_no_color(self):
		tag = Tag.objects.create(name='tag')
		self.assertEqual(tag.color, None)
		self.assertEqual(Tag.objects.get(pk=tag.pk).color, None)

	def test_create_name_untrimmed(self):
		tag = Tag.objects.create(name=' tag name ')
		self.assertEqual(tag.name, 'tag name')

	def test_create_name_uppercase(self):
		tag = Tag.objects.create(name='TAG')
		self.assertEqual(tag.name, 'tag')

	def test_create_name_required_error(self):
		tag = Tag.objects.create(name='')
		with self.assertRaises(ValidationError):
			tag.full_clean()

	def test_create_name_unique_error(self):
		tag = Tag.objects.create(name='tag')
		with self.assertRaises(IntegrityError):
			tag = Tag.objects.create(name='tag')

	def test_create_color(self):
		tag = Tag.objects.create(name='tag', color=int('FFFFFF', 16))
		tag.full_clean()
		self.assertEqual(tag.color, int('FFFFFF', 16))
		self.assertEqual(Tag.objects.get(pk=tag.pk).color, int('FFFFFF', 16))

	def test_create_color_invalid(self):
		tag = Tag.objects.create(name='tag', color=int('1234567', 16))
		with self.assertRaises(ValidationError):
			tag.full_clean()

	def test_order(self):
		Tag.objects.create(name='b')
		Tag.objects.create(name='a')
		self.assertQuerysetEqual(Tag.objects.all(), ['<Tag: a>', '<Tag: b>'])

class IndexViewTagModelTests(TestCase):
	def test_first_access(self):
		response = self.client.get(reverse('tags:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['tag_list'], [])

	def test_create_tag(self):
		response = self.client.post(
			reverse('tags:create-tag'), 
			{'name': 'tag', 'color': int('FFFFFF', 16)}
		)
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(Tag.objects.all(), ['<Tag: tag>'])
		self.assertEqual(Tag.objects.get(name='tag').color, int('FFFFFF', 16))

	def test_create_tag_name_untrimmed(self):
		response = self.client.post(
			reverse('tags:create-tag'), 
			{'name': '   tag name   '}
		)
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(Tag.objects.all(), ['<Tag: tag name>'])

	def test_create_tag_name_uppercase(self):
		response = self.client.post(
			reverse('tags:create-tag'), 
			{'name': 'TAG'}
		)
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(Tag.objects.all(), ['<Tag: tag>'])

	def test_create_tag_name_required(self):
		response = self.client.post(
			reverse('tags:create-tag'), 
			{'name': ''}, 
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['name'][0]['code'], 'required')
		self.assertQuerysetEqual(Tag.objects.all(), [])

	def test_create_tag_name_unique(self):
		self.client.post(
			reverse('tags:create-tag'), 
			{'name': 'tag'}, 
		)
		response = self.client.post(
			reverse('tags:create-tag'), 
			{'name': 'tag'}, 
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['name'][0]['code'], 'unique')
		self.assertQuerysetEqual(Tag.objects.all(), ['<Tag: tag>'])

	def test_create_tag_no_color(self):
		response = self.client.post(
			reverse('tags:create-tag'), 
			{'name': 'tag'}
		)
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(Tag.objects.all(), ['<Tag: tag>'])
		self.assertIsNone(Tag.objects.get(name='tag').color)

	def test_create_tag_color_empty(self):
		response = self.client.post(
			reverse('tags:create-tag'), 
			{'name': 'tag', 'color': ''}
		)
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(Tag.objects.all(), ['<Tag: tag>'])
		self.assertIsNone(Tag.objects.get(name='tag').color)

	def test_create_tag_color_invalid(self):
		response = self.client.post(
			reverse('tags:create-tag'), 
			{'name': 'tag', 'color': int('1234567', 16)}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['color'][0]['code'], 'invalid')
		self.assertQuerysetEqual(Tag.objects.all(), [])

	def test_update_tag(self):
		tag = Tag.objects.create(name='tag')
		response = self.client.post(
			reverse('tags:update-tag'), 
			{'id': tag.pk, 'name': 'tag-upd', 'color': int('FFFFFC', 16)}, 
		)
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(Tag.objects.all(), ['<Tag: tag-upd>'])
		self.assertEqual(Tag.objects.get(pk=tag.pk).color, int('FFFFFC', 16))

	def test_update_tag_color_required_error(self):
		tag = Tag.objects.create(name='tag')
		response = self.client.post(
			reverse('tags:update-tag'), 
			{'id': tag.pk}, 
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['name'][0]['code'], 'required')

	def test_update_tag_color_invalid_error(self):
		tag = Tag.objects.create(name='tag', color=int('FFFFFF', 16))
		response = self.client.post(
			reverse('tags:update-tag'), 
			{'id': tag.pk, 'name': tag.name, 'color': int('1234567', 16)}, 
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['color'][0]['code'], 'invalid')
		self.assertEqual(Tag.objects.get(pk=tag.pk).color, int('FFFFFF', 16))

	def test_update_tag_color_empty(self):
		tag = Tag.objects.create(name='tag', color=int('FFFFFF', 16))
		response = self.client.post(
			reverse('tags:update-tag'), 
			{'id': tag.pk, 'name': tag.name, 'color': ''}, 
		)
		self.assertEqual(response.status_code, 200)
		self.assertIsNone(Tag.objects.get(name='tag').color)

	def test_update_tag_no_color(self):
		tag = Tag.objects.create(name='tag', color=int('FFFFFF', 16))
		response = self.client.post(
			reverse('tags:update-tag'), 
			{'id': tag.pk, 'name': tag.name}, 
		)
		self.assertEqual(response.status_code, 200)
		self.assertIsNone(Tag.objects.get(name='tag').color)

	def test_update_tag_not_exist_error(self):
		Tag.objects.create(name='tag')
		response = self.client.post(
			reverse('tags:update-tag'), 
			{'id': -1}, 
		)
		self.assertEqual(response.status_code, 409)
		self.assertQuerysetEqual(Tag.objects.all(), ['<Tag: tag>'])

	def test_delete_tag(self):
		tag = Tag.objects.create(name='tag')
		response = self.client.post(
			reverse('tags:delete-tag'), 
			{'id': tag.pk}, 
		)
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(Tag.objects.all(), [])

	def test_delete_tag_not_exist(self):
		Tag.objects.create(name='tag')
		response = self.client.post(
			reverse('tags:delete-tag'), 
			{'id': -1}, 
		)
		self.assertEqual(response.status_code, 409)
		self.assertQuerysetEqual(Tag.objects.all(), ['<Tag: tag>'])