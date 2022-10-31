import "../../i18n";
import { useEffect } from "react";
import { AppProps } from "next/app";
import Head from "next/head";
import { QueryClient, QueryClientProvider } from "react-query";
import { ReactQueryDevtools } from "react-query/devtools";
import "../styles/flag-icon.css";
import "@cclw/styles/cclw.main.scss";

import { ThemeContext } from "@context/ThemeContext";
import useGetTheme from "@hooks/useGetTheme";
import { Loading } from "@components/blocks/Loading";

const queryClient = new QueryClient();

declare global {
  interface Window {
    Cypress: any;
    queryClient: any;
  }
}

function MyApp({ Component, pageProps }: AppProps) {
  const { status: themeStatus, theme } = useGetTheme();

  useEffect(() => {
    // For access inside Cypress:
    if (window?.Cypress) {
      window.queryClient = queryClient;
    }
  }, []);

  if (themeStatus != "success") return <Loading />;

  const favicon = theme === "cclw" ? "/cclw/images/favicon.png" : "/favicon.png";

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeContext.Provider value={theme}>
        <Head>
          <link rel="icon" href={favicon} />
          <style>{`
            :root { 
              --color-lineBorder:#bfc2d9;
              --color-primary-400:#ED3D48;
              --color-primary-700:#2B2F49;
              --color-indigo-400:#2B2F49;
              --color-indigo-500:#2B2F49;
              --color-indigo-600:#2B2F49;
              --color-indigo-700:#2B2F49;
              --color-sky:#ED3D48;
              --color-blue-100:#ED3D48;
              --color-blue-200:#ED3D48;
              --color-blue-300:#ED3D48;
              --color-blue-400:#ED3D48;
              --color-blue-500:#ED3D48;
              --color-blue-600:#ED3D48;
              --color-blue-700:#C9131E;
            }
          `}</style>
        </Head>
        <div id={theme}>
          <Component {...pageProps} />
        </div>
      </ThemeContext.Provider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default MyApp;
