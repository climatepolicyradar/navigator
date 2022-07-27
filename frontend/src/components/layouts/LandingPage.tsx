import React, { ReactNode } from "react";
import Head from "next/head";
import Header from "../headers/LandingPage";
import Banner from "../banner/FullHeight";
import Summary from "../blocks/Summary";
import Partners from "../blocks/Partners";
import Footer from "../footer/Footer";

type TProps = {
  children?: ReactNode;
  title?: string;
};

const Layout = ({ children, title = "" }: TProps) => (
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

    <Footer />
  </div>
);

export default Layout;
