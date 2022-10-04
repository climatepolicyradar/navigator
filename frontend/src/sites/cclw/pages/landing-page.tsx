import React, { FC } from "react";
import Main from "../layouts/main";

type TProps = {
  handleSearchInput: (term: string, filter?: string, filterValue?: string) => void;
  handleSearchChange: (type: string, value: any) => void;
  searchInput: string;
};

const LandingPage: FC<TProps> = ({ children }) => {
  return <Main>{children}</Main>;
};

export default LandingPage;
