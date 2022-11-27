// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

import read from "../redirects/reader.mjs";
const REDIRECT_FILE = process.env.NEXT_REDIRECT_FILE || "default.csv";


// console.log("===== IN: next.config.mjs =====");
// console.log("process.env.THEME: ", process.env.THEME);
// console.log("process.env.API_URL: ", process.env.API_URL);
// console.log("process.env.ADOBE_API_KEY: ", process.env.ADOBE_API_KEY);
// console.log("===== OUT: next.config.mjs =====");

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

async function get_redirects() {
    let standardRedirects = process.env.THEME === "cclw" ? cclwRedirects : cprRedirects;
    standardRedirects.concat(await read(REDIRECT_FILE));

    let redirect_map = new Map<string, object>();
    standardRedirects.forEach(redirect => {
        redirect_map.set(redirect["source"], redirect)
    });

    return redirect_map
}

const redirect_map = await get_redirects();

// See "Matching Paths" below to learn more
export const config = {
    matcher: Array.from(redirect_map.keys())
}

// This function can be marked `async` if using `await` inside
export function middleware(request: NextRequest) {
    if (redirect_map.has(request.url)) {
        let redirect_detail = redirect_map.get(request.url);
        let status = redirect_detail['permanent'] ? 308 : 307;
        return NextResponse.redirect(new URL(redirect_detail['target'], request.url), status)
    }
}
