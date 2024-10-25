# AsyncFastAPI-Boilerplate

- http://localhost:8000/docs

- make up

- make down

- make generate-migrations message="Add new migration"

- make apply-migrations

- make downgrade-migrations

- make seed-initial-data


.
  |-Dockerfile
  |-pyproject.toml
  |-scripts
  |  |-start.sh
  |  |-format.sh
  |  |-lint.sh
  |  |-wait-for-it.sh
  |-alembic
  |  |-README
  |  |-versions
  |  |  |-bedbd670c13d_init_models.py
  |  |  |-.keep
  |  |-script.py.mako
  |  |-env.py
  |-.env.$ENV.example
  |-alembic.ini
  |-Makefile
  |-.gitignore
  |-docker-compose.yml
  |-README.md
  |-.env.development
  |-app
  |  |-__init__.py
  |  |-main.py
  |  |-tests
  |  |  |-__init__.py
  |  |  |-test_health.py
  |  |-schemas
  |  |  |-__init__.py
  |  |  |-token.py
  |  |  |-user.py
  |  |-crud
  |  |  |-__init__.py
  |  |  |-base.py
  |  |  |-user.py
  |  |-api
  |  |  |-__init__.py
  |  |  |-v1
  |  |  |  |-__init__.py
  |  |  |  |-endpoints
  |  |  |  |  |-__init__.py
  |  |  |  |  |-user.py
  |  |  |  |  |-auth.py
  |  |  |  |-api.py
  |  |  |-deps.py
  |  |-logs
  |  |  |-app.log
  |  |-utils
  |  |  |-__init__.py
  |  |  |-seeder.py
  |  |  |-referral_code.py
  |  |  |-backend_pre_start.py
  |  |-models
  |  |  |-__init__.py
  |  |  |-user.py
  |  |-core
  |  |  |-__init__.py
  |  |  |-logging.py
  |  |  |-config.py
  |  |  |-security.py
  |  |-db
  |  |  |-__init__.py
  |  |  |-session.py
  |  |  |-base_class.py
  |  |  |-base.py
  |  |-services
  |  |  |-__init__.py
  |  |  |-http.py