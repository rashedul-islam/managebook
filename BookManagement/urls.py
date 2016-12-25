from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^books$', views.book_list, name='book_list'),
    url(r'^book/new/$', views.new_book, name='new_book'),
    url(r'^book/(?P<pk>\d+)/edit/$', views.edit_book, name='edit_book'),
    url(r'^genre$', views.add_genre, name='add_genre')
]