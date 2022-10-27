const getSite = process.env.NEXT_PUBLIC_THEME || "cpr";

console.log("-- CHEESE -- -- CHEESE -- -- CHEESE -- -- CHEESE -- -- CHEESE -- -- CHEESE -- -- CHEESE -- ");
console.log(`NEXT_PUBLIC_THEME ${process.env.NEXT_PUBLIC_THEME}`);
console.log(`NEXT_PUBLIC_API_URL ${process.env.NEXT_PUBLIC_API_URL}`);
console.log(`NEXT_PUBLIC_LOGIN_API_URL ${process.env.NEXT_PUBLIC_LOGIN_API_URL}`);
console.log("-- CHEESE -- -- CHEESE -- -- CHEESE -- -- CHEESE -- -- CHEESE -- -- CHEESE -- -- CHEESE -- ");



// for pages that are not in cclw's sitemap
const cclwRedirects = [
  { source: "/cookie-policy", destination: "/", permanent: true },
  { source: "/privacy", destination: "/", permanent: true },
  { source: "/terms", destination: "/", permanent: true },
];

// for pages that are not in cpr's sitemap
const cprRedirects = [
  { source: "/about", destination: "/", permanent: true },
  { source: "/acknowledgements", destination: "/", permanent: true },
  { source: "/contact", destination: "/", permanent: true },
  { source: "/terms-of-use", destination: "/", permanent: true },
];

/**
 * @type {import('next').NextConfig}
 */

import read from "./redirects/reader.mjs"
const REDIRECT_FILE = process.env.NEXT_REDIRECT_FILE || "default.csv"

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
    ].concat(getSite === "cpr" ? cprRedirects : cclwRedirects);;

    return standardRedirects.concat(await read(REDIRECT_FILE));
  },
  env: {
    NEXT_PUBLIC_THEME: process.env.NEXT_PUBLIC_THEME,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_LOGIN_API_URL: process.env.NEXT_PUBLIC_LOGIN_API_URL,
  }
};
