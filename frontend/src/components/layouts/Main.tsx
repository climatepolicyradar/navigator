import React, { ReactNode } from 'react';
import Head from 'next/head';
import Header from '../headers/Main';
import Banner from '../banner/Slim';

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
    <main className="h-screen flex flex-col">
      <Banner />
      {children}
    </main>
    <footer className="mb-8">
      <hr />
    </footer>
  </div>
);

export default Layout;
