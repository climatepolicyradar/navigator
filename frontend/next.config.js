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

const defaultRedirects = [
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
  ];
 

function get_redirects() {
    const REDIRECT_FILE = process.env.NEXT_REDIRECT_FILE || "default.json";
    const redirectsFromFile = require(`./src/redirects/${REDIRECT_FILE}`);
    let standardRedirects = process.env.THEME === "cclw" ? cclwRedirects : cprRedirects;
    return defaultRedirects
      .concat(standardRedirects)
      .concat(redirectsFromFile);
}

/**
 * @type {import('next').NextConfig}
 */
const nextConfig = {
  i18n: {
    locales: ["en", "fr"],
    defaultLocale: "en",
  },
  pageExtensions: ["tsx", "ts"],
  async redirects() {
    return  defaultRedirects
  },
};

module.exports = (phase) => {
  console.log("Starting at phase:", phase);
  return {
      ...nextConfig,
      async redirects() {
        return get_redirects();
      }
  }
};
