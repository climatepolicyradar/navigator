import Head from 'next/head';
import { AppProps } from 'next/app';
import '../styles/main.scss';

function MyApp({ Component, pageProps }: AppProps) {


  // For later when using Cypress:
  // useEffect(() => {
  //   if (window?.Cypress) {
  //     window.store = store;
  //   }
  // }, [store])

  return (
    <>
      <Head>
        <title>Policy Search</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <Component {...pageProps} />
    </>
  )
}

export default MyApp