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
      green: colors.green,
      semiTransWhite: 'rgba(255, 255, 255, 0.85)',
      indigo: {
        100: '#f2f2f5',
        200: '#e4e6ea',
        300: '#c7ccd5',
        400: '#939bad',
        500: '#616c85',
        600: '#071e4a',
      },
      sky: '#ebf2ff',
      blue: {
        100: '#e8f3fe',
        200: '#d0e5fd',
        300: '#a4cdfb',
        400: '#7cb4fa',
        500: '#1f93ff',
      },
    },
    container: {
      center: true,
      padding: '1rem',
    },
    extend: {},
  },
  plugins: [],
};
