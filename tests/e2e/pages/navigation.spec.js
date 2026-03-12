// @ts-check
const { test, expect } = require('@playwright/test');
const { waitForPageLoad } = require('../../helpers/navigation');

/**
 * CWPD-33: Top navigation functional tests.
 * Verifies all nav items are present and link to the correct pages.
 */
test.describe('Top navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await waitForPageLoad(page);
  });

  test('About Us nav item links to /about-us/', async ({ page }) => {
    await page.click('.primary-menu a[href="/about-us/"]');
    await waitForPageLoad(page);
    expect(page.url()).toContain('/about-us/');
  });

  test('Learn nav item is present and links to /promo-videos/', async ({ page }) => {
    const learnLink = page.locator('.primary-menu a[href="/promo-videos/"]');
    await expect(learnLink).toBeVisible();
    await expect(learnLink).toHaveText('Learn');
    await learnLink.click();
    await waitForPageLoad(page);
    expect(page.url()).toContain('/promo-videos/');
  });

  test('Services nav item links to /services/', async ({ page }) => {
    await page.click('.primary-menu a[href="/services/"]');
    await waitForPageLoad(page);
    expect(page.url()).toContain('/services/');
  });

  test('Learn appears between About Us and Services in nav', async ({ page }) => {
    const items = page.locator('.primary-menu .menu-item a');
    const texts = await items.allTextContents();
    const aboutIndex = texts.indexOf('About Us');
    const learnIndex = texts.indexOf('Learn');
    const servicesIndex = texts.indexOf('Services');
    expect(aboutIndex).toBeLessThan(learnIndex);
    expect(learnIndex).toBeLessThan(servicesIndex);
  });
});
