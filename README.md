# example-backend

## Requirements

- [uv](https://github.com/astral-sh/uv) 0.6.4+

## Installation

```bash
git clone https://github.com/kumarstack55/example-backend.git
cd ./example-backend
uv sync --frozen
```

## Running Tests

```bash
pytest tests/test_message_factory.py
```

## Running the Application

```bash
uv run app.py
```

## Running with Modified Error Rates

```bash
OK_RATIO=0.9 uv run app.py
```

## Building the Container Image

```bash
docker compose build
```

or

```bash
docker buildx build -t example-backend .
```

## Running in a Container

```bash
docker run -p 8080:8080 example-backend
```

## Running Tests for Container

At first, start the service.

```bash
docker compose up -d
```

Then, run the tests.

```bash
uv run pytest test_app.py
```

## License

MIT License.
See the [LICENSE](LICENSE) file for details.