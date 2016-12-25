from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Genre
from .forms import BookForm, GenreForm
from django.contrib import messages
from django.contrib.auth.models import User

MAX_BOOK_LIMIT = 5

def book_list(request):
	"""
	A list of availabe book in the system
	"""
	books = Book.objects.all()
	if not books:
		messages.info(request, "There is no book registered in the current system")
	return render(request, 'BookManagement/book_list.html', {'books': books})

def new_book(request):
	"""
	A new book is created. If there is already a book name with the same author, the system will 
	not save the book in the system
	"""
	if request.method == "POST":
		form = BookForm(request.POST)
		if form.is_valid():
			safe_to_save = True
			books = Book.objects.all()
			if books:
				is_exceed_book_limit = is_exceed_limit(books=books, current_author=request.user.username)

				if is_exceed_book_limit:
					messages.error(request, "You have already created maximum number(5) of books")
					safe_to_save = False
				else:
					is_valid_name = is_valid_book(current_author= request.user.username,
												  inputed_name=form.cleaned_data['book_name'],
												  availale_books=books)
					if not is_valid_name:
						error_msg = "You have alrady created a book with this name, try with different name"
						messages.error(request, error_msg)
						safe_to_save = False

			if safe_to_save:
				book = form.save(commit=False)
				book.author = request.user
				book.save()
				return redirect('book_list')
			else:
				form = BookForm(request.POST)
	else:
		form = BookForm()

	messages.info(request, "Creating a new book")
	return render(request, 'BookManagement/new_book.html', {'form' : form})

def edit_book(request, pk):
	"""
	Editing an exisitng book based on login user(Author)
	"""
	book = get_object_or_404(Book, pk=pk)
	if request.method == "POST":
		if book.author == request.user:
			form = BookForm(request.POST, instance=book)
			if form.is_valid():
				book = form.save(commit=False)
				book.author = request.user
				book.save()
				return redirect('book_list')
		else:
			form = BookForm(instance=book)
			error_msg = "Your are not the auther of this book, only the actual author can edit this book"
			messages.error(request, error_msg)
	else:
		form = BookForm(instance=book)

	messages.info(request, "Editing an existing book")
	return render(request, 'BookManagement/new_book.html', {'form': form})

def add_genre(request):
	"""
	Adding a new genre in the genre table
	"""
	if request.method == "POST":
		form = GenreForm(request.POST)
		if form.is_valid():
			genre = form.save(commit=False)
			genre.save()
	else:
		form = GenreForm()

	genres = Genre.objects.all()
	if genres:
		available_genre = parse_genres(genres)
		messages.info(request, available_genre)
	else:
		info_msg = """
					There is no genre registered in the system by user. 'unspecified' is a default genre
					to choose while creating a new book
				   """
		messages.info(request, info_msg)

	return render(request, 'BookManagement/genres.html', {'form' : form})

def parse_genres(genres):
	"""
	Getting all the available genres as a string
	"""
	genre_list = []
	for genre in genres:
		genre_list.append(genre.name)

	return ", ".join(genre_list)

def is_valid_book(current_author, inputed_name, availale_books):
	"""
	This method will check if the author is creating a book with the same title that he has 
	already created.

	"""
	book_info = []
	author_book = {}

	for book in availale_books:
		author = book.author.username
		author_book[author] = book.book_name
		book_info.append(author_book)
		author_book = {}

	for book in book_info:
		for author, book_name in book.items():
			if book_name == inputed_name and author == current_author:
				return False

	return True

def is_exceed_limit(books, current_author):
	"""
	Returning True if the current author has more than 5 books registered in the system
	"""
	authors =[]
	for book in books:
		authors.append(book.author.username)

	if len(authors) > 0:
		count = authors.count(current_author)
		if count >= MAX_BOOK_LIMIT:
			return True

	return False



