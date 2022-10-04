import React, { FC } from "react";
import Main from "../layouts/main";

const LandingPage: FC = ({ children }) => {
  return (
    <Main>
      {children}
    </Main>
  );
};

export default LandingPage;
