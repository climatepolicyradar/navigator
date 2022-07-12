import "./i18n";
import { useEffect } from 'react';
import Head from 'next/head';
import { AppProps } from 'next/app';
import '../styles/main.scss';
import '../styles/flag-icon.css';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { AuthProvider } from '../api/auth';

// Create a client
const queryClient = new QueryClient();

declare global {
  interface Window { Cypress: any; queryClient: any }
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
      <AuthProvider>
        <Head>
          <title>Policy Search</title>
          <meta
            name="viewport"
            content="initial-scale=1.0, width=device-width"
          />
        </Head>
        <Component {...pageProps} />
      </AuthProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default MyApp;
