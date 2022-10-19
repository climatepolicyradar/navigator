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

    return standardRedirects.concat(await read(REDIRECT_FILE));
  },
}

export default nextConfig
