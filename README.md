Brain
=====

System Architecture Application.

About
-----

Brain is an app for documenting system architectures. Within a map, you can track items of any type and their dependencies on each other.

Installation
------------

Brain uses `pipenv` to manage its dependencies.

Clone the repository and `cd` into it. Run `pipenv install` to create a virtual environment and install the dependencies.

Run `mv .env.example .env` and fill in the file.

Once the installation is complete, run `pipenv shell` to open a shell in the virtual environment and `cd brain` to enter the application code directory.

Run `python manage.py migrate` to create the database and `python manage.py createsuperuser` to create an administrator. Finally, run `python manage.py runserver` to start the app listening at `http://localhost:8000`.

Usage
-----
TODO