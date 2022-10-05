import React, { FC } from "react";
import Head from "next/head";
import CPRMain from "@cpr/layouts/main";
import CCLWMain from "@cclw/layouts/main";
import getSite from "@utils/getSite";
import getPageTitle from "@utils/getPageTitle";

type TProps = {
  title?: string;
  heading?: string;
  screenHeight?: boolean;
};

const Layout: FC<TProps> = ({ children, title = "", screenHeight = false }) => {
  const site = getSite();
  return (
    <div className="h-full flex flex-col">
      <Head>
        <title>{`${getPageTitle()} | ${title}`}</title>
        <meta charSet="utf-8" />
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <a className="sr-only" href="#main">
        Skip to content
      </a>
      {site === "cpr" && <CPRMain screenHeight={screenHeight}>{children}</CPRMain>}
      {site === "cclw" && <CCLWMain>{children}</CCLWMain>}
    </div>
  );
};

export default Layout;
