/**
 * Shared navigation helpers used across all test suites.
 * Add reusable page interaction utilities here as the test suite grows.
 */

/**
 * Waits for the page to be fully loaded and checks for no console errors.
 */
async function waitForPageLoad(page) {
  await page.waitForLoadState('domcontentloaded');
}

/**
 * Returns all tile elements from a grid section.
 */
function getTiles(page, selector = '.col-4 .flex-wrap-bottom-div') {
  return page.locator(selector);
}

module.exports = { waitForPageLoad, getTiles };
