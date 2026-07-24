// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * Playwright configuration for ConsentWise functional tests.
 * Tests run against the local Jekyll dev server (http://localhost:42005).
 * See CONTRIBUTING.md for how to start the server before running tests.
 */
module.exports = defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  retries: 0,
  reporter: [
    ['list'],
    ['html', { open: 'never', outputFolder: 'tests/reports/html' }],
    ['junit', { outputFile: 'tests/reports/junit/results.xml' }],
  ],
  use: {
    baseURL: 'http://localhost:42005',
    headless: true,
    screenshot: 'only-on-failure',
    video: 'off',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
