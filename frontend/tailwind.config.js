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
      lightgray: '#F9FAFB',
      offwhite: '#EFF3FB',
      indigo: {
        100: '#f2f2f5',
        200: '#e4e6ea',
        300: '#c7ccd5',
        400: '#939bad',
        500: '#616c85',
        600: '#071e4a',
        700: '#0A1C40',
      },
      sky: '#ebf2ff',
      blue: {
        100: '#e8f3fe',
        200: '#d0e5fd',
        300: '#a4cdfb',
        400: '#7cb4fa',
        500: '#1f93ff',
        600: '#006FD6',
      },
      bluegreen: {
        100: '#127D9D',
        200: '#285A76',
      },
      yellow: {
        100: '#fefaf1',
        200: '#fcf5e1',
        300: '#faeac3',
        400: '#f6e0a8',
        500: '#f1cb73',
      },
      purple: {
        100: '#f0edfe',
        200: '#e2dafc',
        300: '#c4b6f7',
        400: '#a993f5',
        500: '#8e73f1',
      },
    },
    container: {
      center: true,
      padding: '1rem',
    },
    extend: {
      spacing: {
        150: '150%',
      },
      boxShadow: {
        innerThin: 'inset 0 0 1px 0 rgb(0 0 0 / 0.5)',
      },
      fontSize: {
        h1: '48px',
        h2: '32px',
        h3: '24px',
        h4: '21px',
        h5: '18px',
        h6: '16px',
      },
    },
  },
  plugins: [require('@tailwindcss/forms'), require('tailwind-scrollbar')],
  variants: {
    scrollbar: ['rounded'],
  },
};
