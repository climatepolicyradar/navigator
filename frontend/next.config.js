/*
  THIS IS BURNED AT BUILDTIME - ENV ARE IGNORED AT RUNTIME
*/

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
    ]
  },
};

