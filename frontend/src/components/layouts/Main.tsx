import React, { ReactNode } from 'react';
import Head from 'next/head';
import Header from '../headers/Main';
import Banner from '../banner/Slim';
import Footer from '../footer/Footer';

type Props = {
  children?: ReactNode;
  title?: string;
  heading?: string;
  screenHeight?: boolean;
};

const Layout = ({
  children,
  title = 'This is the default title',
  heading = '',
  screenHeight = false,
}: Props) => (
  <div className="h-full flex flex-col">
    <Head>
      <title>{title}</title>
      <meta charSet="utf-8" />
      <meta name="viewport" content="initial-scale=1.0, width=device-width" />
    </Head>
    <a className="sr-only" href="#main">
      Skip to content
    </a>
    <Header />
    <main className={`${screenHeight ? 'h-screen' : ''} flex flex-col flex-1`}>
      <Banner />
      {children}
    </main>
    <Footer />
  </div>
);

export default Layout;
