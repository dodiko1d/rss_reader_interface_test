<h1>RSS Reader Interface test task</h1>
1. Dev:

* Install [Poetry](https://python-poetry.org/docs/basic-usage/)
* Clone [master](https://github.com/dodiko1d/rss_reader_interface_test.git)
```commandline
https://github.com/dodiko1d/rss_reader_interface_test.git
```
* Initialize virtual environment by poetry:
```commandline
poetry install
```

* Activate virtual environment by running
```
source {path_to_venv}/bin/activate
```

* Alternatively use poetry shell and poetry run:
```commandline
poetry shell
poetry run
```

* Create dev sqlite database and make migrations:
```commandline
poetry run python manage.py migrate
```

* Run dev server
```commandline
poetry run python manage.py runserver
```

* Project main dependencies
```
django
python-dateutil
feedparser
```

