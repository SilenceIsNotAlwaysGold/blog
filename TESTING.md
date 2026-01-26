# Testing Guide

## Overview

This project includes comprehensive testing at multiple levels:
- Unit tests for individual components
- Integration tests for API workflows
- End-to-end tests for complete user journeys

## Running Tests

### Quick Start

```bash
# Run all tests
./run-tests.sh

# Run backend tests only
cd backend && pytest

# Run frontend tests only
cd frontend && npm test
```

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_articles.py

# Run specific test
pytest tests/test_articles.py::test_article_create_schema

# Run integration tests only
pytest tests/test_integration.py -v

# Run with markers
pytest -m unit
pytest -m integration
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

## Test Structure

### Backend Tests

```
backend/tests/
├── test_integration.py      # Integration tests
├── test_articles.py          # Article tests
├── test_auth.py              # Authentication tests
├── test_categories.py        # Category tests
├── test_email.py             # Email tests
├── test_images.py            # Image upload tests
├── test_likes.py             # Like functionality tests
├── test_models.py            # Database model tests
├── test_projects.py          # Project tests
├── test_response.py          # Response format tests
├── test_search.py            # Search tests
├── test_skills.py            # Skill tests
└── test_statistics.py        # Statistics tests
```

### Integration Test Coverage

The integration tests (`test_integration.py`) cover:

1. **Health Check**
   - Service availability

2. **User Authentication Flow**
   - Registration
   - Login
   - Token validation
   - User info retrieval

3. **Article CRUD Workflow**
   - Create article
   - Read article
   - Update article
   - Delete article

4. **Like Workflow**
   - Toggle like/unlike
   - Check like status
   - IP-based deduplication

5. **Search Workflow**
   - Article search
   - Global search
   - Search suggestions

6. **Statistics**
   - Overview stats
   - Popular articles
   - Tag statistics

7. **Skills and Projects**
   - Grouped skills
   - Project listing
   - Featured projects

8. **Error Handling**
   - 404 Not Found
   - 401 Unauthorized
   - 400 Bad Request

## Test Configuration

### pytest.ini

```ini
[tool:pytest]
testpaths = tests
asyncio_mode = auto
addopts = --verbose --cov=app
```

### Test Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.asyncio` - Async tests

## Docker Test Environment

### Start Test Environment

```bash
# Start test containers
docker-compose -f docker-compose.test.yml up -d

# Run tests in container
docker-compose -f docker-compose.test.yml exec backend pytest

# Stop test environment
docker-compose -f docker-compose.test.yml down -v
```

### Test Database

- Separate MongoDB instance for testing
- Port: 27018 (to avoid conflicts)
- Database: test_blog
- Credentials: test/test

## Coverage Reports

### Generate Coverage

```bash
cd backend
pytest --cov=app --cov-report=html
```

### View Coverage

```bash
# Open HTML report
open htmlcov/index.html

# Or view in terminal
pytest --cov=app --cov-report=term-missing
```

## Continuous Integration

### GitHub Actions (Example)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: ./run-tests.sh
```

## Writing Tests

### Unit Test Example

```python
def test_article_create_schema():
    """Test article creation schema"""
    article_data = {
        "title": "Test",
        "content": "Content",
        "board": "tech"
    }
    article = ArticleCreate(**article_data)
    assert article.title == "Test"
```

### Integration Test Example

```python
@pytest.mark.asyncio
async def test_article_workflow():
    """Test complete article workflow"""
    async with AsyncClient(app=app) as client:
        # Create
        response = await client.post("/api/v1/articles", json=data)
        assert response.status_code == 201

        # Read
        article_id = response.json()["data"]["id"]
        response = await client.get(f"/api/v1/articles/{article_id}")
        assert response.status_code == 200
```

## Best Practices

1. **Isolation**: Each test should be independent
2. **Cleanup**: Use fixtures for setup/teardown
3. **Mocking**: Mock external services
4. **Coverage**: Aim for >80% coverage
5. **Speed**: Keep tests fast
6. **Clarity**: Use descriptive test names
7. **Documentation**: Add docstrings to tests

## Troubleshooting

### Tests Fail to Connect to Database

```bash
# Check MongoDB is running
docker-compose -f docker-compose.test.yml ps

# Check logs
docker-compose -f docker-compose.test.yml logs mongodb-test
```

### Import Errors

```bash
# Install test dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov httpx
```

### Async Test Issues

```bash
# Ensure pytest-asyncio is installed
pip install pytest-asyncio

# Check pytest.ini has asyncio_mode = auto
```

## Test Data

### Fixtures

Create test fixtures in `conftest.py`:

```python
@pytest.fixture
async def test_user():
    """Create test user"""
    user = await create_user(...)
    yield user
    await user.delete()
```

### Mock Data

Use factories for consistent test data:

```python
def create_test_article(**kwargs):
    """Create test article with defaults"""
    defaults = {
        "title": "Test Article",
        "content": "Test content",
        "board": "tech"
    }
    defaults.update(kwargs)
    return ArticleCreate(**defaults)
```

## Performance Testing

```bash
# Run with timing
pytest --durations=10

# Profile tests
pytest --profile

# Parallel execution
pytest -n auto
```

## Maintenance

- Run tests before commits
- Update tests with code changes
- Review coverage regularly
- Keep test data minimal
- Clean up test database
