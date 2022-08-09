import React, { FC } from 'react';
import Head from 'next/head';
import Banner from '@components/banner/FullHeight';
import { Hero } from '@components/blocks/Hero';
import { pageTitle } from '@constants/title';

type TProps = {
  title?: string;
  height?: number;
};

const Layout: FC<TProps> = ({ children, title = '', height }) => (
  <div>
    <Head>
      <title>
        {pageTitle} | {title}
      </title>
      <meta charSet="utf-8" />
      <meta name="viewport" content="initial-scale=1.0, width=device-width" />
    </Head>
    <main>
      <Banner height={height} />
      <Hero height={height}>{children}</Hero>
    </main>
  </div>
);

export default Layout;
