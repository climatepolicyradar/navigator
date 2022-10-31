import React, { ReactNode, useContext } from "react";
import Head from "next/head";
import { ThemeContext } from "@context/ThemeContext";
import getPageTitle from "@utils/getPageTitle";

type TProps = {
  children?: ReactNode;
  title?: string;
};

const Layout = ({ children, title = "" }: TProps) => {
  const theme = useContext(ThemeContext);

  return (
    <div>
      <Head>
        <title>{`${getPageTitle(theme)} | ${title}`}</title>
        <meta charSet="utf-8" />
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <a className="sr-only" href="#main">
        Skip to content
      </a>
      {children}
    </div>
  );
};

export default Layout;
