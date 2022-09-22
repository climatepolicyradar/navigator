import React, { FC } from "react";
import Header from "@components/headers/LandingPage";
import Banner from "@components/banner/FullHeight";
import Summary from "@components/blocks/Summary";
import Partners from "@components/blocks/Partners";
import Footer from "@components/footer/Footer";

const LandingPage: FC = ({ children }) => {
  return (
    <>
      <Header />
      <main>
        <Banner />
        {children}
      </main>
      <Summary />
      <Partners />
      <Footer />
    </>
  );
};

export default LandingPage;
