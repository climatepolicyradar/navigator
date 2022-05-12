import React, { ReactNode } from 'react';
import Link from 'next/link';
import Head from 'next/head';
import Header from '../headers/LandingPage';
import Banner from '../banner/FullHeight';
import Summary from '../blocks/Summary';
import Partners from '../blocks/Partners';
import FooterLanding from '../footer/FooterLanding';

type Props = {
  children?: ReactNode;
  title?: string;
  heading: string;
};

const Layout = ({
  children,
  title = 'This is the default title',
  heading = '',
}: Props) => (
  <div>
    <Head>
      <title>{title}</title>
      <meta charSet="utf-8" />
      <meta name="viewport" content="initial-scale=1.0, width=device-width" />
    </Head>
    <a className="sr-only" href="#main">
      Skip to content
    </a>
    <Header />
    <main>
      <Banner />
      {children}
    </main>
    <Summary />
    <Partners />

    <FooterLanding />
  </div>
);

export default Layout;
