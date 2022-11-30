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

export function get_redirects(): Array<TRedirect> {
    const REDIRECT_FILE = process.env.NEXT_REDIRECT_FILE || "default.json";
    const redirectsFromFile = require(`./${REDIRECT_FILE}`);
    let standardRedirects = process.env.THEME === "cclw" ? cclwRedirects : cprRedirects;
    const reds = standardRedirects.concat(redirectsFromFile);
    console.log(`>>>>> GRD - Complete with ${reds.length}`)
    return reds;
}
