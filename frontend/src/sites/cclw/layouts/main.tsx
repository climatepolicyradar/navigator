import React, { FC } from "react";
import Header from "@cclw/components/Header";
import Footer from "@cclw/components/Footer";

type TProps = {
  screenHeight?: boolean;
};

const Main: FC<TProps> = ({ screenHeight, children }) => (
  <>
    <Header />
    <main className={`${screenHeight ? "h-screen" : ""} flex flex-col flex-1 relative`}>
      {children}
    </main>
    <Footer />
  </>
);
export default Main;
