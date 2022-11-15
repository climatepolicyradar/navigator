module.exports = {
  plugins: {
    // tailwindcss: { config: `./tailwind.${process.env.THEME || "cclw"}.config.js` },
    tailwindcss: { config: `./tailwind.cclw.config.js` },
    autoprefixer: {},
  },
};
