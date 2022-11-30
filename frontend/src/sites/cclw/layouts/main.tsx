import React, { FC, ReactNode } from "react";
import Header from "@cclw/components/Header";
import Footer from "@cclw/components/Footer";

type TProps = {
  children?: ReactNode;
};

const Main: FC<TProps> = ({ children }) => (
  <>
    <Header />
    <main className="flex flex-col flex-1">{children}</main>
    <Footer />
  </>
);
export default Main;
