// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * Playwright configuration for ConsentWise functional tests.
 * Tests run against the local Jekyll dev server (http://localhost:4001).
 * See CONTRIBUTING.md for how to start the server before running tests.
 */
module.exports = defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  retries: 0,
  reporter: [['list'], ['html', { open: 'never', outputFolder: 'tests/reports' }]],
  use: {
    baseURL: 'http://localhost:4001',
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
