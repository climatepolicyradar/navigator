const { defineConfig } = require('cypress');

// load the environment variables from the local .env file
require('dotenv').config();

module.exports = defineConfig({
  viewportWidth: 1000,
  viewportHeight: 700,
  chromeWebSecurity: false,
  e2e: {
    baseUrl: 'http://localhost:3000',
    // We've imported your old cypress plugins here.
    // You may want to clean this up later by importing these.
    setupNodeEvents(on, config) {
      // return require('./cypress/plugins/index.js')(on, config);
      config.env = config.env || {};
      config.env.LOGIN_NAME = process.env.LOGIN_NAME;
      config.env.LOGIN_PW = process.env.LOGIN_PW;
      config.env.API_HOST = process.env.API_HOST;
      return config;
    },
    specPattern: 'cypress/e2e/**/*.{js,jsx,ts,tsx}',
    excludeSpecPattern: [
      '**/1-getting-started/*.js',
      '**/2-advanced-examples/*.js',
    ],
  },
});
