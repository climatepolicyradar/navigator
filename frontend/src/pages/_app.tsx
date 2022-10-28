import "../../i18n";
import { useEffect } from "react";
import { AppProps } from "next/app";
import { QueryClient, QueryClientProvider } from "react-query";
import { ReactQueryDevtools } from "react-query/devtools";
// import "../styles/main.scss";
import "../styles/flag-icon.css";

import "@cclw/styles/cclw.main.scss";

import { ThemeContext } from "@context/ThemeContext";
import useGetSite from "@hooks/useGetTheme";
import { Loading } from "@components/blocks/Loading";

const queryClient = new QueryClient();

declare global {
  interface Window {
    Cypress: any;
    queryClient: any;
  }
}

function MyApp({ Component, pageProps }: AppProps) {
  const { status: themeStatus, theme } = useGetSite();

  // For access inside Cypress:
  useEffect(() => {
    if (window?.Cypress) {
      window.queryClient = queryClient;
    }
  }, []);

  if (themeStatus != "success") return <Loading />;

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeContext.Provider value={theme}>
        <Component {...pageProps} />
      </ThemeContext.Provider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default MyApp;
