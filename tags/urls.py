from django.conf.urls import url

from . import views

app_name = 'tags'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'tags/create$', views.create_tag, name='create-tag'),
    url(r'tags/(?P<tag_id>[0-9]+)/delete$', views.delete_tag, name='delete-tag'),
    url(r'tags/(?P<tag_id>[0-9]+)/name/update$', views.update_tag_name, name='update-tag-name'),
    url(r'tags/(?P<tag_id>[0-9]+)/color/update/(?P<color_id>[0-9]+)$', views.update_tag_color, name='update-tag-color'),
    url(r'notes/(?P<note_id>[0-9]+)/tags/(?P<tag_id>[0-9]+)/remove$', views.remove_note_tag, name='remove-note-tag'),
    url(r'notes/(?P<note_id>[0-9]+)/delete$', views.delete_note, name='delete-note'),
]