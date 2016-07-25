# FunkTown

Volunteer database system.

## Setting up the first time

```
$ virtualenv env
$ source bin/env/activiate
$ pip install -r requirements.txt
$ touch app.db
$ python migrate.py
```

Activating the virtualenv (line 2) must be done in every terminal that
you intend to use for development.

Running database migrations (line 5) might be necessary after pulling in
new code.

## Running development server

```
$ python funktown.py
```

