import "./i18n";
import { useEffect } from "react";
import Head from "next/head";
import Script from "next/script";
import { AppProps } from "next/app";
import { QueryClient, QueryClientProvider } from "react-query";
import { ReactQueryDevtools } from "react-query/devtools";
import "../styles/main.scss";
import "../styles/flag-icon.css";

import { CookieConsent } from "@components/cookies/CookieConsent";

const queryClient = new QueryClient();

declare global {
  interface Window {
    Cypress: any;
    queryClient: any;
  }
}

function MyApp({ Component, pageProps }: AppProps) {
  // For access inside Cypress:
  useEffect(() => {
    if (window?.Cypress) {
      window.queryClient = queryClient;
    }
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <Head>
        <title>Climate Policy Radar</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <Script
        src="https://www.googletagmanager.com/gtag/js?id=G-ZD1WWE49TL"
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){window.dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('consent', 'default', {
            'ad_storage': 'denied',
            'analytics_storage': 'denied',
          });
          gtag('config', 'G-ZD1WWE49TL');
        `}
      </Script>
      <Component {...pageProps} />
      <CookieConsent />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default MyApp;
