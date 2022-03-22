import Head from 'next/head';
import { AppProps } from 'next/app';
import '../styles/main.scss';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { AuthProvider } from '../api/auth';

// Create a client
const queryClient = new QueryClient();

function MyApp({ Component, pageProps }: AppProps) {
  // For later when using Cypress:
  // useEffect(() => {
  //   if (window?.Cypress) {
  //     window.store = store;
  //   }
  // }, [store])

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
