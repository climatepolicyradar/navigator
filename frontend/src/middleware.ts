// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { get_redirects } from './redirects/redirects';
import { TRedirect } from '@types';


function get_map() {
  return get_redirects().reduce(
      (acc, item) => ( acc.set(item.source, item) ),
      new Map<string, TRedirect>()
  );
}

const redirect_map = get_map();

// This function can be marked `async` if using `await` inside
export function middleware(request: NextRequest) {
    const url = new URL(request.url); 
    const redirect_detail = redirect_map.get(url.pathname);
    if (redirect_detail) {
        console.log(`Found redirect: ${url.pathname} -> ${redirect_detail.destination}`);

        let status = redirect_detail['permanent'] ? 308 : 307;
        return NextResponse.redirect(new URL(redirect_detail['target'], request.url), status)
    }
}

