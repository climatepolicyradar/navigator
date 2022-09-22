import React, { FC } from "react";
import Main from "../layouts/main";
import Banner from "@components/banner/FullHeight";

const LandingPage: FC = ({ children }) => {
  return (
    <Main>
      <Banner />
      {children}
    </Main>
  );
};

export default LandingPage;
