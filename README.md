# Another TODO API:

#### Steps to run the Application locally:

##### Dependencies required:
- Python3.12
- Sqlite3
- Docker (for shorter way to setup)

#### Short way:

* **Step 0** - Make sure Docker is installed.

```sh
git clone https://github.com/prateekj117/ToDo-API.git
cd ToDo-API
docker build -t django-todo .
docker run -i -p 8000:8000 --name django-todo django-todo
```

#### Long way:

Make sure you have the dependencies mentioned above installed before proceeding further.

* **Step 0** - Clone the repository and ```cd ``` into the directory.

```sh
git clone https://github.com/prateekj117/ToDo-API.git
cd ToDo-API
```

* **Step 1** - Create virtualenv and Install Python Dependencies.

```sh
mkvirtualenv todo
pip install -r requirements.txt
```

* **Step 2** - Run Migrations.

```sh
python manage.py migarte
```

* **Step 3** - Make static files.

```sh
python manage.py collectstatic
```

* **Step 4** - Run Server.

```sh
python manage.py runserver
```

* Run Unit Tests:

```sh
python manage.py test todo
python manage.py test authentication
```

#### API Docs:
- You can find the API docs at 0.0.0.0:8000/swagger

#### Requirements explained and Methodology:
* Created a basic backend api with auth.
* Created basic user registration and authentication system.
* Also made a Dockerfile for the project for easy setup
* Also made a good amount of tests
* As further improvements:
    * Can add priority to the tasks, as well as deadline time
    * Also can add forget password flow, etc.
