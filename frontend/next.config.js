import getSite from "@utils/getSite";

// for pages that are not in cclw's sitemap
const cclwRedirects = [];

// for pages that are not in cpr's sitemap
const cprRedirects = [
  { source: "/about", destination: "/", permanent: true },
  { source: "/contact", destination: "/", permanent: true },
  { source: "/terms-of-use", destination: "/", permanent: true },
];

module.exports = {
  i18n: {
    locales: ["en", "fr"],
    defaultLocale: "en",
  },
  pageExtensions: ["tsx", "ts"],
  async redirects() {
    return [
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
        permanent: true,
      },
    ].concat(getSite() === "cpr" ? cprRedirects : cclwRedirects);
  },
};
