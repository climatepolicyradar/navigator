const colors = require('tailwindcss/colors');

module.exports = {
  content: [
    './src/components/**/*.{ts,tsx,js,jsx}',
    './src/pages/**/*.{ts,tsx,js,jsx}',
  ],
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      black: colors.black,
      white: colors.white,
      gray: colors.gray,
      red: colors.rose,
    },
    container: {
      center: true,
      padding: '1rem',
    },
    extend: {},
  },
  plugins: [],
};
