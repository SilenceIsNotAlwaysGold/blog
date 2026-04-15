# Testing Guide - Personal Blog System

This guide explains how to run all tests for the personal blog system.

---

## Prerequisites

1. **Services Running**
   ```bash
   docker-compose up -d
   ```

2. **Node.js and npm installed**
   ```bash
   node --version  # Should be v20+
   npm --version
   ```

3. **Playwright installed**
   ```bash
   npm install
   npx playwright install chromium
   ```

---

## Quick Start

### Run All Tests
```bash
# Run E2E tests
npx playwright test

# Run API tests
./tests/api-test.sh

# Run visual tests
npx playwright test visual-verification
```

---

## Detailed Testing

### 1. E2E Tests (Playwright)

**Run all E2E tests:**
```bash
npx playwright test
```

**Run specific test suite:**
```bash
# Tech Board tests only
npx playwright test --grep "Tech Board"

# Projects tests only
npx playwright test --grep "Projects"

# Navigation tests only
npx playwright test --grep "Navigation"
```

**Run with UI mode (interactive):**
```bash
npx playwright test --ui
```

**Run in headed mode (see browser):**
```bash
npx playwright test --headed
```

**Run specific test file:**
```bash
npx playwright test tests/e2e/blog-comprehensive.spec.js
```

**View test report:**
```bash
npx playwright show-report
```

---

### 2. API Tests (Backend)

**Run all API tests:**
```bash
./tests/api-test.sh
```

**Run with verbose output:**
```bash
bash -x ./tests/api-test.sh
```

**Test specific endpoint manually:**
```bash
# Articles
curl http://localhost:8001/api/v1/articles?board=tech&page=1&page_size=10

# Categories
curl http://localhost:8001/api/v1/categories?board=tech

# Projects
curl http://localhost:8001/api/v1/projects

# Search
curl -X POST "http://localhost:8001/api/v1/articles/search?keyword=Python&page=1&page_size=10"
```

---

### 3. Visual Tests

**Capture screenshots of all pages:**
```bash
npx playwright test visual-verification
```

**View screenshots:**
```bash
ls -lh test-results/screenshots/
```

**Open screenshot:**
```bash
# On Linux
xdg-open test-results/screenshots/tech-board-home.png

# On Mac
open test-results/screenshots/tech-board-home.png
```

---

## Test Configuration

### Playwright Configuration

Edit `playwright.config.js` to customize:

```javascript
module.exports = defineConfig({
  testDir: './tests/e2e',
  timeout: 60000,           // Test timeout
  workers: 1,               // Parallel workers
  retries: 0,               // Retry failed tests
  use: {
    baseURL: 'http://localhost:3001',
    headless: true,         // Run in headless mode
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
});
```

### API Test Configuration

Edit `tests/api-test.sh` to customize:

```bash
BASE_URL="http://localhost:8001"
API_PREFIX="/api/v1"
```

---

## Debugging Tests

### Debug E2E Tests

**Run with debug mode:**
```bash
npx playwright test --debug
```

**Run specific test with debug:**
```bash
npx playwright test --grep "Tech Board" --debug
```

**Inspect element selectors:**
```bash
npx playwright codegen http://localhost:3001
```

### Debug API Tests

**Add verbose output:**
```bash
# Add -v flag to curl commands in api-test.sh
curl -v http://localhost:8001/api/v1/articles
```

**Check backend logs:**
```bash
docker logs personal-blog-backend --tail 50
```

---

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Start services
        run: docker-compose up -d

      - name: Wait for services
        run: sleep 10

      - name: Install dependencies
        run: npm install

      - name: Install Playwright
        run: npx playwright install --with-deps chromium

      - name: Run E2E tests
        run: npx playwright test

      - name: Run API tests
        run: ./tests/api-test.sh

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-results/
```

---

## Test Maintenance

### Update Tests

When adding new features:

1. **Add E2E test** in `tests/e2e/blog-comprehensive.spec.js`
2. **Add API test** in `tests/api-test.sh`
3. **Add visual test** in `tests/e2e/visual-verification.spec.js`

### Update Selectors

If frontend changes break tests:

1. Use Playwright Inspector:
   ```bash
   npx playwright codegen http://localhost:3001
   ```

2. Update selectors in test files

3. Re-run tests to verify

---

## Common Issues

### Issue: Tests timeout

**Solution:**
```bash
# Increase timeout in playwright.config.js
timeout: 120000  // 2 minutes
```

### Issue: Services not running

**Solution:**
```bash
# Check service status
docker-compose ps

# Restart services
docker-compose restart

# Check logs
docker-compose logs
```

### Issue: Port already in use

**Solution:**
```bash
# Find process using port
lsof -i :3001
lsof -i :8001

# Kill process
kill -9 <PID>

# Or change ports in docker-compose.yml
```

### Issue: Playwright browser not installed

**Solution:**
```bash
npx playwright install chromium
```

---

## Test Reports

### View HTML Report

```bash
npx playwright show-report
```

### Generate Custom Report

```bash
# JSON report
npx playwright test --reporter=json

# JUnit report (for CI)
npx playwright test --reporter=junit

# Multiple reporters
npx playwright test --reporter=html,json,junit
```

---

## Performance Testing

### Measure Page Load Times

```javascript
test('measure page load time', async ({ page }) => {
  const start = Date.now();
  await page.goto('http://localhost:3001/tech');
  await page.waitForLoadState('networkidle');
  const loadTime = Date.now() - start;
  console.log(`Page loaded in ${loadTime}ms`);
  expect(loadTime).toBeLessThan(5000); // Should load in < 5s
});
```

---

## Best Practices

1. **Run tests before committing**
   ```bash
   npx playwright test && ./tests/api-test.sh
   ```

2. **Keep tests independent**
   - Each test should work standalone
   - Don't rely on test execution order

3. **Use meaningful test names**
   ```javascript
   test('should display 8 category cards on Tech Board', ...)
   ```

4. **Add waits for dynamic content**
   ```javascript
   await page.waitForLoadState('networkidle');
   await page.waitForTimeout(2000);
   ```

5. **Clean up after tests**
   - Reset database state if needed
   - Clear browser storage

---

## Resources

- [Playwright Documentation](https://playwright.dev)
- [Test Reports](./COMPREHENSIVE-TEST-REPORT-20260126.md)
- [Test Summary](./TEST-SUMMARY.md)
- [Test Artifacts](./TEST-ARTIFACTS-INDEX.md)

---

## Support

For issues or questions:
1. Check test reports in this directory
2. Review test execution logs
3. Examine screenshots in `test-results/screenshots/`
4. Check backend logs: `docker logs personal-blog-backend`

---

**Last Updated**: 2026-01-26
**Test Framework**: Playwright + Custom Scripts
**Test Coverage**: 100% of core features
