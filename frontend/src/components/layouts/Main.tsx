import React, { ReactNode } from 'react';
import Head from 'next/head';
import Header from '../headers/Main';
import Banner from '../banner/Slim';
import FooterMain from '../footer/FooterMain';
import FooterLanding from '../footer/FooterLanding';

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
  <div className="h-full">
    <Head>
      <title>{title}</title>
      <meta charSet="utf-8" />
      <meta name="viewport" content="initial-scale=1.0, width=device-width" />
    </Head>
    <a className="sr-only" href="#main">
      Skip to content
    </a>
    <Header />
    <main className={`${screenHeight ? 'h-screen' : ''} flex flex-col`}>
      <Banner />
      {children}
    </main>
    {/* <FooterMain /> */}
    <FooterLanding />
  </div>
);

export default Layout;
