# managebook
python version used for this project : python 3.5.2
django version : 1.10.4

How to run :

1. install multiselectfield (https://pypi.python.org/pypi/django-multiselectfield)
2. During migration of database, please comment the line (CHOICES = construct_genre_choices(Genre.objects.all())) from model.py file(line 28)
When the database is migrated then uncomment the line.

Hope this instruction will help to run the project 
