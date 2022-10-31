import React, { FC } from "react";
import Head from "next/head";
import CPRMain from "@cpr/layouts/main";
import CCLWMain from "@cclw/layouts/main";
import getPageTitle from "@utils/getPageTitle";

import { useContext } from "react";
import { ThemeContext } from "@context/ThemeContext";

type TProps = {
  title?: string;
  heading?: string;
  screenHeight?: boolean;
};

const Layout: FC<TProps> = ({ children, title = "", screenHeight = false }) => {
  const theme = useContext(ThemeContext);
  
  return (
    <div className="h-full flex flex-col">
      <Head>
        <title>{`${getPageTitle(theme)} | ${title}`}</title>
        <meta charSet="utf-8" />
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <a className="sr-only" href="#main">
        Skip to content
      </a>
      {theme === "cpr" && <CPRMain screenHeight={screenHeight}>{children}</CPRMain>}
      {theme === "cclw" && <CCLWMain>{children}</CCLWMain>}
    </div>
  );
};

export default Layout;
