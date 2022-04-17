# django skeleton

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Documentation: ###

* [Architecture overview](docs/architecture_overview.md)
* [Backend: Pre-commit hook](docs/pre_commit_hook.md)

### API documentation: ###

* ReDoc web UI: [https://example.com/_platform/docs/v1/redoc/](https://example.com/_platform/docs/v1/redoc/)
* Swagger web UI: [https://example.com/_platform/docs/v1/swagger/](https://example.com/_platform/docs/v1/swagger/)
* Swagger JSON: [https://example.com/_platform/docs/v1/swagger.json](https://example.com/_platform/docs/v1/swagger.json)
* Swagger YAML: [https://example.com/_platform/docs/v1/swagger.yaml](https://example.com/_platform/docs/v1/swagger.yaml)

### First run: ###

Install Python requirements:

```bash
pip install -r requirments-dev.txt
```

Run backing services (require Docker & docker-compose):

```bash
docker-compose up -d
```

Run migrations:

```bash
python manage.py migrate
```

Run Django server:

```bash
python manage.py runserver
```
