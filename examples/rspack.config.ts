// @ts-check

const { defineConfig } = require('@rspack/cli');

const config = defineConfig({
  entry: {
    main: './src/index.js',
  },
});
module.exports = config;