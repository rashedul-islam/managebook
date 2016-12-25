from django import forms
from .models import Book, Genre

class BookForm(forms.ModelForm):
	
	class Meta:
		model = Book
		fields = ('book_name', 'genres',)

class GenreForm(forms.ModelForm):
	class Meta:
		model = Genre
		fields = ('name',)