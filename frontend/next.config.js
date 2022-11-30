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
 

/**
 * @type {import('next').NextConfig}
 */
const nextConfig = {
  i18n: {
    locales: ["en", "fr"],
    defaultLocale: "en",
  },
  pageExtensions: ["tsx", "ts"],
  redirects: async () => {
    return defaultRedirects;
  }
};

module.exports = nextConfig;