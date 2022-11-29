/*
  THIS IS BURNED AT BUILDTIME - ENV ARE IGNORED AT RUNTIME

  NOTE: If you are writing code in here beyond setting vars...
            ... you probably shouldn't be.
*/

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
    ]
  },
};

module.exports = nextConfig;