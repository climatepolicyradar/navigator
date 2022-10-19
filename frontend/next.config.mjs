/**
 * @type {import('next').NextConfig}
 */

import getRedirectsFromCsv from "./redirects/reader.mjs"
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
    ];

    return standardRedirects.concat(await getRedirectsFromCsv(REDIRECT_FILE));
  },
}

export default nextConfig
