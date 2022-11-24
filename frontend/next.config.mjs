const getSite = process.env.THEME || "cpr";

console.log("===== IN: next.config.mjs =====");
console.log("process.env.THEME: ", process.env.THEME);
console.log("process.env.API_URL: ", process.env.API_URL);
console.log("process.env.ADOBE_API_KEY: ", process.env.ADOBE_API_KEY);
console.log("===== OUT: next.config.mjs =====");

// for pages that are not in cclw's sitemap
const cclwRedirects = [
  { source: "/cookie-policy", destination: "/", permanent: true },
  { source: "/privacy", destination: "/", permanent: true },
];

// for pages that are not in cpr's sitemap
const cprRedirects = [
  { source: "/about", destination: "/", permanent: true },
  { source: "/acknowledgements", destination: "/", permanent: true },
  { source: "/contact", destination: "/", permanent: true },
  { source: "/methodology", destination: "/", permanent: true },
];

/**
 * @type {import('next').NextConfig}
 */

import read from "./redirects/reader.mjs";
const REDIRECT_FILE = process.env.NEXT_REDIRECT_FILE || "default.csv";

const nextConfig = {
  i18n: {
    locales: ["en", "fr"],
    defaultLocale: "en",
  },
  pageExtensions: ["tsx", "ts"],
  async redirects() {
    const standardRedirects = [
      {
        source: "/auth/:id*",
        destination: "/",
        permanent: true,
      },
      {
        source: "/account",
        destination: "/",
        permanent: true,
      },
      {
        source: "/users/:id*",
        destination: "/",
        permanent: true,
      },
      {
        source: "/litigation/:id*",
        destination: "/",
        permanent: false, // will become a page eventually
      },
    ].concat(getSite === "cpr" ? cprRedirects : cclwRedirects);

    return standardRedirects.concat(await read(REDIRECT_FILE));
  },
};

export default nextConfig;
