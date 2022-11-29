// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { TRedirect } from './types';

const REDIRECT_FILE = process.env.NEXT_REDIRECT_FILE || "default.json";
const redirectsFromFile = require(`./redirects/${REDIRECT_FILE}`);


// console.log("===== IN: next.config.mjs =====");
// console.log("process.env.THEME: ", process.env.THEME);
// console.log("process.env.API_URL: ", process.env.API_URL);
// console.log("process.env.ADOBE_API_KEY: ", process.env.ADOBE_API_KEY);
// console.log("===== OUT: next.config.mjs =====");

// for pages that are not in cclw's sitemap
const cclwRedirects: Array<TRedirect> = [
    { source: "/cookie-policy", destination: "/", permanent: true },
    { source: "/privacy", destination: "/", permanent: true },
];

// for pages that are not in cpr's sitemap
const cprRedirects: Array<TRedirect> = [
    { source: "/about", destination: "/", permanent: true },
    { source: "/acknowledgements", destination: "/", permanent: true },
    { source: "/contact", destination: "/", permanent: true },
    { source: "/methodology", destination: "/", permanent: true },
];

function get_redirects(): Map<string, TRedirect> {
    let standardRedirects = process.env.THEME === "cclw" ? cclwRedirects : cprRedirects;
    standardRedirects.concat(redirectsFromFile);

    return standardRedirects.reduce(
        (acc, item) => ( acc.set(item["source"], item) ),
        new Map<string, TRedirect>()
    );
}

const redirect_map = get_redirects();

// This function can be marked `async` if using `await` inside
export function middleware(request: NextRequest) {
    if (redirect_map.has(request.url)) {
        let redirect_detail = redirect_map.get(request.url);
        if (redirect_detail) {
            console.log(`Found redirect: ${redirect_detail}`);

            let status = redirect_detail['permanent'] ? 308 : 307;
            return NextResponse.redirect(new URL(redirect_detail['target'], request.url), status)
        }
    }
}
