const getSite = process.env.NEXT_PUBLIC_THEME || "cpr";

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
        permanent: false, // will become a page eventually
      },
    ].concat(getSite === "cpr" ? cprRedirects : cclwRedirects);
  },
};
