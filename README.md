# SWC - Interview Project - URL Shortener

## Run checks

```bash
just check
```

Checks include:
- ruff formatting
- mypy type checks
- pytest tests

## Run development server

```bash
just runserver
```

or

```bash
uv run manage.py runserver localhost:8080
```

The development server will run on port 8080

## How to shorten URLs

1. Start development server `just runserver`
2. Go to http://localhost:8080/shorten/ you will see DRF UI for testing endpoints
3. Put `{"url": "http://example.com/"}` into Content field and click "Post" button. You will see output of the call above the form.
4. The "short_url" key in output dict containes the resulting URL. If you open it in new window it will redirect you to the original URL
