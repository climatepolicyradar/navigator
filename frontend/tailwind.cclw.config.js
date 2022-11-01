/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");

module.exports = {
  content: ["./src/components/**/*.{ts,tsx,js,jsx}", "./src/pages/**/*.{ts,tsx,js,jsx}", "./src/sites/**/*.{ts,tsx,js,jsx}"],
  theme: {
    colors: {
      transparent: "transparent",
      current: "currentColor",
      black: colors.black,
      white: colors.white,
      gray: colors.gray,
      red: colors.rose,
      green: colors.green,
      semiTransWhite: "rgba(255, 255, 255, 0.85)",
      overlayWhite: "rgba(217, 217, 217, 0.25)",
      offwhite: "#EFF3FB",
      lineBorder: "var(--color-lineBorder)",
      search: {
        dropdownBg: "#f2f2f5",
        itemHover: "#e4e6ea",
      },
      grey: {
        200: "#F9FAFB",
        400: "#E7E7EA",
        500: "#CFD0D7",
        700: "#6e6e6e",
      },
      indigo: {
        100: "#f2f2f5",
        200: "#e4e6ea",
        300: "#c7ccd5",
        400: "#2B2F49",
        500: "#2B2F49",
        600: "#2B2F49",
        700: "#2B2F49",
      },
      sky: "var(--color-sky)",
      primary: {
        400: "var(--color-primary-400)",
        700: "var(--color-primary-700)",
      },
      secondary: {
        500: "#393A5A",
        700: "#2B2F49",
      },
      blue: {
        100: "var(--color-blue-100)",
        200: "var(--color-blue-200)",
        300: "var(--color-blue-300)",
        400: "var(--color-blue-400)",
        500: "var(--color-blue-500)",
        600: "var(--color-blue-600)",
        700: "var(--color-blue-700)",
      },
      bluegreen: {
        100: "#127D9D",
        200: "#285A76",
      },
      yellow: {
        100: "#fefaf1",
        200: "#fcf5e1",
        300: "#faeac3",
        400: "#f6e0a8",
        500: "#f1cb73",
      },
      purple: {
        100: "#f0edfe",
        200: "#e2dafc",
        300: "#c4b6f7",
        400: "#a993f5",
        500: "#8e73f1",
      },
    },
    container: {
      center: true,
      padding: "1rem",
    },
    extend: {
      spacing: {
        150: "150%",
      },
      boxShadow: {
        innerThin: "inset 0 0 1px 0 rgb(0 0 0 / 0.5)",
      },
      fontSize: {
        h1: "48px",
        h2: "32px",
        h3: "24px",
        h4: "21px",
        h5: "18px",
        h6: "16px",
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("tailwind-scrollbar")],
  variants: {
    scrollbar: ["rounded"],
  },
};
