import { TRedirect } from "@types";

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

const theme = process.env.THEME;

function getRedirects(): Array<TRedirect> {
    const REDIRECT_FILE = process.env.NEXT_REDIRECT_FILE || "default.json";
    const redirectsFromFile = require(`./${REDIRECT_FILE}`);
    let redirects = redirectsFromFile;
    switch (theme)  {
        case "cclw": redirects.push.apply(redirects, cclwRedirects); break;
        case "cpr": redirects.push.apply(redirects, cprRedirects); break;
    }
    console.log(`Loaded ${redirects.length} redirects for ${theme}`);
    console.log(JSON.stringify(redirects, null, 4));
    return redirects;
}


function getRedirectsMap() {
  return getRedirects().reduce(
      (acc, item) => ( acc.set(item.source, item) ),
      new Map<string, TRedirect>()
  );
}

export default getRedirectsMap();
