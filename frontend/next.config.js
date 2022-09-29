module.exports = {
  i18n: {
    locales: ["en", "fr"],
    defaultLocale: "en",
  },
  pageExtensions: ["tsx", "ts"],
  async redirects() {
    return [
      {
        source: '/auth/:id*',
        destination: '/',
        permanent: true,
      },
      {
        source: '/account',
        destination: '/',
        permanent: true,
      },
      {
        source: '/users/:id*',
        destination: '/',
        permanent: true,
      },
      {
        source: '/litigation/:id*',
        destination: '/',
        permanent: true,
      },
    ]
  },
};
