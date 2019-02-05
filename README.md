# Test task for Fondy.eu

Server must provide API for transaction log and method to update data from csv.
Test data:
  - [initial](https://gist.github.com/TihonV/bd5b2a963519a468ba9882b93b9c8ad6)
  - [patch](https://gist.github.com/TihonV/cb486255e19cd3546613a9ea07d1ae8d)

### Env

Use [pipenv](https://github.com/pypa/pipenv) or virtualenv

### Example
```chameleon
pipenv shell
pipenv install
python manage.py apply_csv_patch --path ./path/to/file.csv
python manage.py apply_csv_patch --path https://gist.github.com/TihonV/bd5b2a963519a468ba9882b93b9c8ad6/raw/25a4581d97d079c8620bc2a7747bc47462e99b3d/import.csv
python manage.py apply_csv_patch --path https://gist.github.com/TihonV/cb486255e19cd3546613a9ea07d1ae8d/raw/9059b76e6556dd66d228d750f4b72e4513f8ad64/import_patch.csv
python manage.py runserver
```
[Open browser](http://localhost:8000/)
