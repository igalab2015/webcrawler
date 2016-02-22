## Web crawler written in python

#### Usage
start crawler
```
python3 manage.py celery worker --beat --scheduler=djcelery.schedulers.DatabaseScheduler
```

start server
```
python3 manage.py runserver --insecure
```

#### Dependency
redis-server
celery

#### Caution
This crawler takes long time if max_depth is 2.
And it could be cyber attack.

