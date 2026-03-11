// @ts-check
const { test, expect } = require('@playwright/test');
const { waitForPageLoad } = require('../../helpers/navigation');

/**
 * CWPD-14: Promo Videos page functional tests.
 * Phase 1: baseline tests for the existing page (pre-video-tiles).
 * Phase 2 tests (tile grid, video pages) will be added under CWPD-10 and CWPD-12.
 */
test.describe('Promo Videos page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/promo-videos/');
    await waitForPageLoad(page);
  });

  test('page loads successfully', async ({ page }) => {
    await expect(page).toHaveTitle(/Promo Videos/i);
  });

  test('page description text is visible', async ({ page }) => {
    const body = page.locator('body');
    await expect(body).toContainText('Produce a video');
  });

  test('footer legal text is visible', async ({ page }) => {
    const footer = page.locator('.footer-legal');
    await expect(footer).toBeVisible();
    await expect(footer).toContainText('Qeetoto Limited');
  });

  test('Contact Us CTA is present', async ({ page }) => {
    const cta = page.locator('.bottom-cta');
    await expect(cta).toBeVisible();
    await expect(cta.locator('a')).toBeVisible();
  });
});
