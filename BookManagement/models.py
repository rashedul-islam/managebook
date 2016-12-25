from django.db import models
from multiselectfield import MultiSelectField

CHOICES = (("default", "default"))

class Genre(models.Model):
	name = models.CharField(max_length=200)

	def save_genre(self):
		self.save()

	def __str__(self):
		return self.name

def construct_genre_choices(available_genres):
	genre_list = []
	if available_genres:
		for genre in available_genres:
			genre_list.append(genre.name)
	else:
		genre_list = ["unspecified"]

	choices = [(x,x) for x in genre_list]
	result = tuple(choices)
	return result

CHOICES = construct_genre_choices(Genre.objects.all())

class Book(models.Model):
	author = models.ForeignKey('auth.User')
	book_name = models.CharField(max_length=200)
	genres = MultiSelectField(choices=CHOICES)

	def save_book(self):
		self.save()

	def __str__(self):
		return self.book_name
