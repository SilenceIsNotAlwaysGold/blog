/**
 * Visual Verification Test
 * Captures screenshots of all pages for visual inspection
 */

const { test } = require('@playwright/test');

const BASE_URL = 'http://localhost:3001';

test.describe('Visual Verification - All Pages', () => {

  test('capture Tech Board homepage', async ({ page }) => {
    await page.goto(`${BASE_URL}/tech`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test-results/screenshots/tech-board-home.png', fullPage: true });
    console.log('Screenshot saved: tech-board-home.png');
  });

  test('capture Tech Board with category filter', async ({ page }) => {
    await page.goto(`${BASE_URL}/tech`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    // Click first category
    const firstCategory = page.locator('[data-testid="category-card"], .category-card, .el-card').first();
    if (await firstCategory.count() > 0) {
      await firstCategory.click();
      await page.waitForTimeout(2000);
      await page.screenshot({ path: 'test-results/screenshots/tech-board-filtered.png', fullPage: true });
      console.log('Screenshot saved: tech-board-filtered.png');
    }
  });

  test('capture article detail page', async ({ page }) => {
    await page.goto(`${BASE_URL}/tech`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    // Click first article
    const firstArticle = page.locator('a[href*="/tech/"]').first();
    if (await firstArticle.count() > 0) {
      await firstArticle.click();
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000);
      await page.screenshot({ path: 'test-results/screenshots/article-detail.png', fullPage: true });
      console.log('Screenshot saved: article-detail.png');
    }
  });

  test('capture Projects page', async ({ page }) => {
    await page.goto(`${BASE_URL}/projects`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test-results/screenshots/projects-page.png', fullPage: true });
    console.log('Screenshot saved: projects-page.png');
  });

  test('capture Skills page', async ({ page }) => {
    await page.goto(`${BASE_URL}/skills`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test-results/screenshots/skills-page.png', fullPage: true });
    console.log('Screenshot saved: skills-page.png');
  });

  test('capture About page', async ({ page }) => {
    await page.goto(`${BASE_URL}/about`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test-results/screenshots/about-page.png', fullPage: true });
    console.log('Screenshot saved: about-page.png');
  });

  test('capture Life Board login redirect', async ({ page }) => {
    await page.goto(`${BASE_URL}/life`);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test-results/screenshots/life-board-login.png', fullPage: true });
    console.log('Screenshot saved: life-board-login.png');
  });
});
