// @ts-check
const { test, expect } = require('@playwright/test');
const { waitForPageLoad, getTiles } = require('../../helpers/navigation');

/**
 * CWPD-14: Services page functional tests.
 * Baseline tests for the existing services tile pattern —
 * these serve as the reference implementation that video tiles must match.
 */
test.describe('Services page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/services/');
    await waitForPageLoad(page);
  });

  test('page loads with correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/Services/i);
  });

  test('service tiles are visible', async ({ page }) => {
    const tiles = getTiles(page);
    await expect(tiles).toHaveCount(8); // 8 services currently configured
  });

  test('each tile has a title and summary', async ({ page }) => {
    const tiles = page.locator('.col-4 .flex-wrap-bottom-div');
    const count = await tiles.count();
    for (let i = 0; i < count; i++) {
      const tile = tiles.nth(i);
      await expect(tile.locator('h4')).toBeVisible();
      await expect(tile.locator('p')).toBeVisible();
    }
  });

  test('each tile has a clickable image link', async ({ page }) => {
    const links = page.locator('.col-4 .flex-wrap-bottom-div a');
    const count = await links.count();
    expect(count).toBeGreaterThan(0);
    for (let i = 0; i < count; i++) {
      await expect(links.nth(i)).toHaveAttribute('href', /.+/);
    }
  });

  test('clicking first tile navigates to a service page', async ({ page }) => {
    const firstLink = page.locator('.col-4 .flex-wrap-bottom-div a').first();
    await firstLink.click();
    await waitForPageLoad(page);
    expect(page.url()).not.toBe('http://localhost:4001/services/');
  });

  test('footer legal text is visible', async ({ page }) => {
    const footer = page.locator('.footer-legal');
    await expect(footer).toBeVisible();
    await expect(footer).toContainText('Qeetoto Limited');
  });
});
