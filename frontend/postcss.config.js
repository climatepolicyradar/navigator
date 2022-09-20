module.exports = {
  plugins: {
    tailwindcss: { config: `./tailwind.${process.env.NEXT_PUBLIC_THEME || "cpr"}.config.js` },
    autoprefixer: {},
  },
};
