check:
    uv run ruff check --fix .
    uv run mypy .
    uv run pytest --pdb

runserver:
    uv run manage.py runserver localhost:8080