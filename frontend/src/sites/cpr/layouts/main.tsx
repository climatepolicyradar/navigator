import React, { FC, ReactNode } from "react";
import Header from "@components/headers/Main";
import Banner from "@components/banner/Main";
import Footer from "@components/footer/Footer";

type TProps = {
  screenHeight?: boolean;
  children?: ReactNode;
};

const Main: FC<TProps> = ({ screenHeight, children }) => (
  <>
    <Header />
    <main className={`${screenHeight ? "h-screen" : ""} flex flex-col flex-1`}>
      <Banner />
      {children}
    </main>
    <Footer />
  </>
);
export default Main;
