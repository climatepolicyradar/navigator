import React, { ReactNode } from "react";
import Head from "next/head";
import getSite from "@utils/getSite";
import getPageTitle from "@utils/getPageTitle";
import CPRMain from "@cpr/pages/landing-page";
import CCLWMain from "@cclw/pages/landing-page";

type TProps = {
  children?: ReactNode;
  title?: string;
};

const Layout = ({ children, title = "" }: TProps) => {
  const site = getSite();
  return (
    <div>
      <Head>
        <title>{`${getPageTitle()} | ${title}`}</title>
        <meta charSet="utf-8" />
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <a className="sr-only" href="#main">
        Skip to content
      </a>
      {site === "cpr" && <CPRMain>{children}</CPRMain>}
      {site === "cclw" && <CCLWMain>{children}</CCLWMain>}
    </div>
  );
};

export default Layout;
