module.exports = {
  plugins: {
    // tailwindcss: { config: `./tailwind.${process.env.NEXT_PUBLIC_THEME || "cclw"}.config.js` },
    tailwindcss: { config: `./tailwind.cclw.config.js` },
    autoprefixer: {},
  },
};
